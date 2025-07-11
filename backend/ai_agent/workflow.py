import re
from typing import Union

from langchain_core.messages import BaseMessage
from langchain_core.output_parsers import PydanticOutputParser
from langchain.output_parsers import RetryWithErrorOutputParser
from langgraph.graph import END, StateGraph
from langchain_google_genai import ChatGoogleGenerativeAI

from langchain.prompts import (
    ChatPromptTemplate,
)


from .state import (
    QueryInfoState,
    QueryAssessmentState,
    TranslationAgentState,
    TranslationState,
    ReviewState,
    FormatState,
    FixedMalformedJsonState,
)

from .prompts import (
    output_format_instructions,
    translate_system_prompt,
    redo_translate_system_prompt,
    review_system_prompt,
    format_translation_system_prompt,
    query_assessment_system_prompt,
    malformed_json_system_prompt,
)


class TranslatorGraph:
    # Node names
    QUERY_ASSESSMENT_NODE = "query_assessment"
    FIX_MALFORMED_JSON_NODE = "fix_malformed_json"
    TRANSLATE_NODE = "translate"
    REVIEW_NODE = "review"
    FORMAT_NODE = "format"
    LAST_IDX = -1

    def __init__(self):
        self.llm = self.create_llm_instance()
        self.query_assessment_graph = self._build_query_assessment_graph()
        self.graph = self._build_translation_graph()

    def create_llm_instance(self):
        return ChatGoogleGenerativeAI(
            model="gemini-2.5-flash",
            temperature=0,
            max_tokens=None,
            top_p=1.0,
        )

    def execute_query_assessment(self, input_query: str) -> QueryAssessmentState:
        print("--------------------------------")
        print("input_query")
        print(input_query)
        print("--------------------------------")

        return self.query_assessment_graph.invoke({"input_query": input_query})

    def execute_translation(
        self,
        input_query: str,
        target_language: str,
    ):

        return self.graph.invoke(
            {
                "input_query": input_query,
                "target_language": target_language,
                "translation_state": {
                    "current_translation": "",
                    "iteration": 0,
                },
            }
        )

    def shared_node_logic(
        self,
        state: TranslationAgentState,
        prompt: str,
        pydantic_object: Union[
            TranslationState,
            ReviewState,
            FormatState,
            FixedMalformedJsonState,
            QueryAssessmentState,
        ],
    ) -> TranslationAgentState:
        """Shared node logic."""
        parser = PydanticOutputParser(pydantic_object=pydantic_object)

        # retry parser
        retry_parser = RetryWithErrorOutputParser.from_llm(parser=parser, llm=self.llm)

        # llm call
        llm_call = prompt | self.llm
        result = llm_call.invoke({"input_query": state.input_query})
        cleaned_content = self._parse_result(result)

        result = retry_parser.parse_with_prompt(
            cleaned_content, prompt.invoke({"input_query": state.input_query})
        )

        return result

    def query_assessment_node(
        self, state: QueryAssessmentState
    ) -> QueryAssessmentState:
        """Assess the query info."""
        print("--------------------------------")
        print("Calling query_info_node")
        print("--------------------------------")

        input_query = state.input_query

        prompt = ChatPromptTemplate.from_template(
            template=query_assessment_system_prompt(),
            partial_variables={
                "input_query": input_query,
                "format_instructions": output_format_instructions(
                    QueryInfoState.model_json_schema()
                ),
            },
        )

        result = self.shared_node_logic(
            state=state,
            prompt=prompt,
            pydantic_object=QueryInfoState,
        )

        state.query_info = result

        return state

    def fix_malformed_json_node(
        self, state: QueryAssessmentState
    ) -> QueryAssessmentState:
        """Fix the malformed JSON."""
        print("--------------------------------")
        print("Calling fix_malformed_json_node")
        print("--------------------------------")

        prompt = ChatPromptTemplate.from_template(
            template=malformed_json_system_prompt(),
            partial_variables={
                "input_query": state.input_query,
                "issues": state.query_info.malformed_json_issues,
                "format_instructions": output_format_instructions(
                    FixedMalformedJsonState.model_json_schema()
                ),
            },
        )

        result = self.shared_node_logic(
            state=state,
            prompt=prompt,
            pydantic_object=FixedMalformedJsonState,
        )

        state.fixed_json_state = result

        return state

    def translate_node(self, state: TranslationAgentState) -> TranslationAgentState:
        """Translate the text from English into a target language."""
        print("--------------------------------")
        print("Calling translate_node")
        print("--------------------------------")

        should_redo_translation = (
            state.review_state
            and state.review_state.review_decision == "REDO"
            and state.review_state.issues
            and len(state.review_state.issues) > 0
        )

        initial_iteration = state.translation_state.iteration

        format_instructions = output_format_instructions(
            TranslationState.model_json_schema()
        )

        prompt = ChatPromptTemplate.from_template(
            template=(
                redo_translate_system_prompt()
                if should_redo_translation
                else translate_system_prompt()
            ),
            partial_variables=(
                {
                    "current_translation": state.translation_state.current_translation,
                    "issues": state.review_state.issues,
                    "format_instructions": format_instructions,
                }
                if should_redo_translation
                else {
                    "input_query": state.input_query,
                    "target_language": state.target_language,
                    "format_instructions": format_instructions,
                }
            ),
        )

        result = self.shared_node_logic(
            state=state,
            prompt=prompt,
            pydantic_object=TranslationState,
        )

        state.translation_state = result
        state.translation_state.iteration = initial_iteration + 1

        # reset review state
        if should_redo_translation:
            state.review_state.review_decision = None
            state.review_state.issues = []
            state.review_state.review_reasoning = ""
            state.review_state.review_translation_rating = 0

        return state

    def review_node(self, state: TranslationAgentState) -> TranslationAgentState:
        """Review the translation of a text from English into a target language."""
        print("--------------------------------")
        print("Calling review_node")
        print("--------------------------------")

        # if maximum number of iterations reached, end the workflow
        if (
            state.review_state
            and state.translation_state
            and state.translation_state.iteration == 2
        ):
            state.review_state.review_decision = "APPROVE"
            state.review_state.review_reasoning = "Maximum number of iterations reached"
            state.review_state.review_translation_rating = 0

            return state

        # if not maximum number of iterations reached, review the translation
        format_instructions = output_format_instructions(
            ReviewState.model_json_schema()
        )

        prompt = ChatPromptTemplate.from_template(
            template=review_system_prompt(),
            partial_variables=(
                {
                    "current_translation": state.translation_state.current_translation,
                    "input_query": state.input_query,
                    "format_instructions": format_instructions,
                }
            ),
        )

        result = self.shared_node_logic(
            state=state,
            prompt=prompt,
            pydantic_object=ReviewState,
        )

        state.review_state = result

        return state

    def format_translation_node(
        self, state: TranslationAgentState
    ) -> TranslationAgentState:
        """Format the translation of a text from English into a target language."""
        # if input query is a JSON object, do not format the translation
        current_translation = state.translation_state.current_translation

        if isinstance(current_translation, dict) or isinstance(
            current_translation, list
        ):
            state.format_state = FormatState(
                final_translation=current_translation,
                final_translation_rating=state.review_state.review_translation_rating,
            )

            return state

        # if input query is not a JSON object, format the translation
        format_instructions = output_format_instructions(
            FormatState.model_json_schema()
        )

        prompt = ChatPromptTemplate.from_template(
            template=format_translation_system_prompt(),
            partial_variables=(
                {
                    "translated_content": state.translation_state.current_translation,
                    "input_query": state.input_query,
                    "format_instructions": format_instructions,
                }
            ),
        )

        result = self.shared_node_logic(
            state=state,
            prompt=prompt,
            pydantic_object=FormatState,
        )

        state.format_state = result

        return state

    def review_router(self, state: TranslationAgentState):
        """LLM decides whether to redo translation or end."""
        decision = state.review_state.review_decision

        if decision == "REDO":
            return self.TRANSLATE_NODE

        elif decision == "APPROVE":
            return self.FORMAT_NODE

        else:
            return self.TRANSLATE_NODE

    def query_assessment_router(self, state: QueryAssessmentState):
        """LLM decides whether to filter out malformed JSON or end."""

        if state.query_info.string_content_type == "malformed_json":
            return self.FIX_MALFORMED_JSON_NODE

        else:
            return END

    def fix_malformed_json_router(self, state: QueryAssessmentState):
        """LLM decides whether to filter out malformed JSON or end."""

        if state.string_content_type == "malformed_json":
            return self.FIX_MALFORMED_JSON_NODE

        else:
            return END

    def _parse_result(
        self, result: BaseMessage
    ) -> Union[TranslationAgentState, QueryAssessmentState]:
        """Parse the result of the LLM call."""
        cleaned_content = re.sub(
            r"<think>.*?</think>", "", result.content, flags=re.DOTALL
        ).strip()

        return cleaned_content

    def _build_query_assessment_graph(self) -> StateGraph:
        """Build the query assessment workflow graph."""
        builder = StateGraph(QueryAssessmentState)

        builder.add_node(self.QUERY_ASSESSMENT_NODE, self.query_assessment_node)
        builder.add_node(self.FIX_MALFORMED_JSON_NODE, self.fix_malformed_json_node)

        builder.set_entry_point(self.QUERY_ASSESSMENT_NODE)

        builder.add_conditional_edges(
            self.QUERY_ASSESSMENT_NODE,
            self.query_assessment_router,
            {
                self.FIX_MALFORMED_JSON_NODE: self.FIX_MALFORMED_JSON_NODE,
                END: END,
            },
        )

        builder.add_edge(self.FIX_MALFORMED_JSON_NODE, END)

        return builder.compile()

    def _build_translation_graph(self) -> StateGraph:
        """Build the translation workflow graph."""
        builder = StateGraph(TranslationAgentState)

        # Add nodes
        builder.add_node(self.TRANSLATE_NODE, self.translate_node)
        builder.add_node(self.REVIEW_NODE, self.review_node)
        builder.add_node(self.FORMAT_NODE, self.format_translation_node)

        # Set entry point
        builder.set_entry_point(self.TRANSLATE_NODE)

        # Add edges
        builder.add_conditional_edges(
            self.REVIEW_NODE,
            self.review_router,
            {
                self.TRANSLATE_NODE: self.TRANSLATE_NODE,
                self.FORMAT_NODE: self.FORMAT_NODE,
            },
        )

        builder.add_edge(self.TRANSLATE_NODE, self.REVIEW_NODE)
        builder.add_edge(self.FORMAT_NODE, END)

        return builder.compile()


# Create a singleton instance
translator_graph = TranslatorGraph()
