import re
import json
from typing import Type

from langchain_core.messages import BaseMessage
from langchain_core.output_parsers import PydanticOutputParser
from langchain.output_parsers import RetryWithErrorOutputParser
from langgraph.graph import END, StateGraph
from langchain_anthropic import ChatAnthropic
from langchain.prompts import HumanMessagePromptTemplate, SystemMessagePromptTemplate


from .state import (
    AgentState,
    TranslationState,
    ReviewState,
    FormatState,
    QueryInfoState,
    FixedMalformedJsonState,
)

from .prompts import (
    output_format_instructions,
    translate_system_prompt,
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
        self.graph = self._build_graph()

    def create_llm_instance(self):
        return ChatAnthropic(
            model="claude-sonnet-4-20250514",
            temperature=0.0,
            max_tokens=20000,
            top_p=1.0,
        )

    def execute(
        self,
        input_query: str,
        target_language: str,
        is_json: bool = False,
        is_string: bool = False,
    ):

        return self.graph.invoke(
            {
                "original_input_query": input_query,
                "llm_input_query": input_query,
                "target_language": target_language,
                "is_json": is_json,
                "is_string": is_string,
                "translation_state": {
                    "current_translation": ({} if is_json else {} if is_string else ""),
                    "iteration": 0,
                },
            }
        )

    def shared_node_logic(
        self,
        state: AgentState,
        prompt: str,
        pydantic_object: Type[
            QueryInfoState | TranslationState | ReviewState | FormatState
        ],
        partials: dict = {},
    ) -> AgentState:
        """Shared node logic."""
        llm_input_query = state.llm_input_query

        parser = PydanticOutputParser(pydantic_object=pydantic_object)

        system = SystemMessagePromptTemplate.from_template(prompt)
        human = HumanMessagePromptTemplate.from_template("{llm_input_query}")

        format_structure = pydantic_object.model_json_schema()
        format_instructions = output_format_instructions(format_structure)

        prompt = (system + human).partial(
            format_instructions=format_instructions, **partials
        )

        # retry parser
        retry_parser = RetryWithErrorOutputParser.from_llm(parser=parser, llm=self.llm)

        # llm call
        llm_call = prompt | self.llm
        result = llm_call.invoke({"llm_input_query": llm_input_query})
        cleaned_content = self._parse_result(result)

        result = retry_parser.parse_with_prompt(
            cleaned_content, prompt.invoke(llm_input_query)
        )

        return result

    def fix_malformed_json(self, state: AgentState) -> AgentState:
        """Fix malformed JSON from the input query."""
        print("--------------------------------")
        print("Calling fix_malformed_json")
        print("--------------------------------")

        llm_input_query = (
            f"Fix the following malformed JSON: {state.original_input_query}"
        )

        state.llm_input_query = llm_input_query

        result: FixedMalformedJsonState = self.shared_node_logic(
            state,
            malformed_json_system_prompt(),
            FixedMalformedJsonState,
            {"issues": state.query_info.malformed_json_issues},
        )

        state.is_json = True
        state.is_string = False
        state.original_input_query = json.dumps(result.fixed_json_content)

        return state

    def query_assessment_node(self, state: AgentState) -> AgentState:
        """Assess the query info."""
        print("--------------------------------")
        print("Calling query_info_node")
        print("--------------------------------")

        llm_input_query = f"Assess the following content: {state.original_input_query}"
        state.llm_input_query = llm_input_query

        result: QueryInfoState = self.shared_node_logic(
            state,
            query_assessment_system_prompt(),
            QueryInfoState,
            {"is_string": state.is_string, "is_json": state.is_json},
        )

        state.query_info = result

        return state

    def translate_node(self, state: AgentState) -> AgentState:
        """Translate the text from English into a target language."""
        print("--------------------------------")
        print("Calling translate_node")
        print("--------------------------------")

        llm_input_query = f"Translate the following text into {state.target_language}: \n\n{state.original_input_query}"
        state.llm_input_query = llm_input_query
        initial_iteration = state.translation_state.iteration

        result: TranslationState = self.shared_node_logic(
            state,
            translate_system_prompt(),
            TranslationState,
            {
                "defective_keys": (
                    state.review_state.defective_keys if state.review_state else []
                ),
                "current_translation": (
                    state.translation_state.current_translation
                    if state.translation_state
                    else ""
                ),
            },
        )

        # reset the defective keys after each iteration
        if state.review_state and len(state.review_state.defective_keys):
            state.review_state.defective_keys = []

        state.translation_state = result

        state.translation_state.iteration = (
            max(initial_iteration, state.translation_state.iteration) + 1
        )

        return state

    def review_node(self, state: AgentState) -> AgentState:
        """Review the translation of a text from English into a target language."""
        print("--------------------------------")
        print("Calling review_node")
        print("--------------------------------")

        llm_input_query = f"""
        Review the following translation: \n{state.translation_state.current_translation} 
        The original text is: \n{state.original_input_query}
        The target language is: \n{state.target_language}
        The translation is in JSON format: \n{state.is_json}
        The translation is in string format: \n{state.is_string}
        """

        state.llm_input_query = llm_input_query

        # if maximum iterations reached, approve the translation
        if (
            state.translation_state
            and state.translation_state.iteration == 2
            and state.review_state
        ):
            state.review_state.review_decision = "APPROVE"
            state.review_state.review_reasoning = "Maximum iterations reached"

            return state

        # if not, review the translation
        result: ReviewState = self.shared_node_logic(
            state,
            review_system_prompt(),
            ReviewState,
            {
                "current_translation": state.translation_state.current_translation,
                "original_input_query": state.original_input_query,
            },
        )

        state.review_state = result

        return state

    def format_translation_node(self, state: AgentState) -> AgentState:
        """Format the translation of a text from English into a target language."""
        print("--------------------------------")
        print("Calling format_translation_node")
        print("--------------------------------")

        llm_input_query = f"Format the following translation: {state.translation_state.current_translation}"
        state.llm_input_query = llm_input_query

        result: FormatState = self.shared_node_logic(
            state,
            format_translation_system_prompt(),
            FormatState,
            {
                "input_query": state.original_input_query,
                "final_translation": state.translation_state.current_translation,
            },
        )

        state.format_state = result

        return state

    def review_router(self, state: AgentState):
        """LLM decides whether to redo translation or end."""
        decision = state.review_state.review_decision

        if decision == "REDO":
            return self.TRANSLATE_NODE

        elif decision == "END":
            return END

        else:
            return self.FORMAT_NODE

    def fix_malformed_json_router(self, state: AgentState):
        """LLM decides whether to filter out malformed JSON or end."""

        if state.query_info.is_malformed_json:
            return self.FIX_MALFORMED_JSON_NODE

        else:
            return self.TRANSLATE_NODE

    def _parse_result(self, result: BaseMessage) -> AgentState:
        """Parse the result of the LLM call."""
        cleaned_content = re.sub(
            r"<think>.*?</think>", "", result.content, flags=re.DOTALL
        ).strip()

        return cleaned_content

    def _build_graph(self) -> StateGraph:
        """Build the translation workflow graph."""
        builder = StateGraph(AgentState)

        # Add nodes
        builder.add_node(self.QUERY_ASSESSMENT_NODE, self.query_assessment_node)
        builder.add_node(self.TRANSLATE_NODE, self.translate_node)
        builder.add_node(self.FIX_MALFORMED_JSON_NODE, self.fix_malformed_json)
        builder.add_node(self.REVIEW_NODE, self.review_node)
        builder.add_node(self.FORMAT_NODE, self.format_translation_node)

        # Add edges
        builder.add_conditional_edges(
            self.QUERY_ASSESSMENT_NODE,
            self.fix_malformed_json_router,
            {
                self.FIX_MALFORMED_JSON_NODE: self.FIX_MALFORMED_JSON_NODE,
                self.TRANSLATE_NODE: self.TRANSLATE_NODE,
            },
        )

        builder.add_edge(self.FIX_MALFORMED_JSON_NODE, self.TRANSLATE_NODE)
        builder.add_edge(self.TRANSLATE_NODE, self.REVIEW_NODE)
        builder.add_edge(self.FORMAT_NODE, END)

        # # Add conditional edges
        builder.add_conditional_edges(
            self.REVIEW_NODE,
            self.review_router,
            {
                self.TRANSLATE_NODE: self.TRANSLATE_NODE,
                self.FORMAT_NODE: self.FORMAT_NODE,
                END: END,
            },
        )

        # Set entry point
        builder.set_entry_point(self.QUERY_ASSESSMENT_NODE)

        return builder.compile()


# Create a singleton instance
translator_graph = TranslatorGraph()
