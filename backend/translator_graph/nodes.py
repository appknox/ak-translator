import re

from typing import List, Sequence, Literal
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage
from langgraph.graph import END, MessageGraph

from translator_graph.chains import (
    translate_text_chain,
    review_translation_chain,
    redo_translate_decision_chain,
    format_translation_prompt,
)

TRANSLATE_NODE = "translate"
REVIEW_NODE = "review"
DECISION_NODE = "decision"
FORMAT_NODE = "format"
LAST_IDX = -1


def translate_node(state: Sequence[BaseMessage]):
    """Translate the text from English into a target language."""
    return translate_text_chain.invoke({"messages": state})


def review_node(state: Sequence[BaseMessage]) -> List[BaseMessage]:
    """Review the translation of a text from English into a target language."""
    res = review_translation_chain.invoke({"messages": state})
    return [HumanMessage(content=res.content)]


def decision_node(state: List[BaseMessage]) -> List[BaseMessage]:
    """LLM decides whether to redo translation or end."""

    translation_attempts = sum(
        1
        for msg in state
        if isinstance(msg, AIMessage) and "translation" in msg.content.lower()
    )

    context_content = f"Translation attempts so far: {translation_attempts}/3"
    context_message = HumanMessage(content=context_content)

    decision_response = redo_translate_decision_chain.invoke(
        {"messages": state + [context_message]}
    )

    decision_message = AIMessage(
        content=f"Decision: {decision_response.content.strip()}"
    )

    return [decision_message]


def format_translation_node(state: Sequence[BaseMessage]):
    """Format the translation of a text from English into a target language."""
    return format_translation_prompt.invoke({"messages": state})


def should_continue_or_format(state: List[BaseMessage]) -> Literal["translate", "end"]:
    """Route based on LLM decision."""
    last_message = state[LAST_IDX]

    if isinstance(last_message, AIMessage):
        content = last_message.content
        decision_redo_pattern = r"(?=.*Decision)(?=.*REDO)"
        match = re.search(decision_redo_pattern, content, re.IGNORECASE | re.DOTALL)

        if match:
            return TRANSLATE_NODE

    return FORMAT_NODE


builder = MessageGraph()

builder.add_node(TRANSLATE_NODE, translate_node)
builder.add_node(REVIEW_NODE, review_node)
builder.add_node(DECISION_NODE, decision_node)
builder.add_node(FORMAT_NODE, format_translation_node)

builder.set_entry_point(TRANSLATE_NODE)
builder.add_edge(TRANSLATE_NODE, REVIEW_NODE)
builder.add_edge(REVIEW_NODE, DECISION_NODE)

builder.add_conditional_edges(
    DECISION_NODE,
    should_continue_or_format,
    {FORMAT_NODE: FORMAT_NODE, TRANSLATE_NODE: TRANSLATE_NODE},
)

builder.add_edge(DECISION_NODE, FORMAT_NODE)
builder.add_edge(FORMAT_NODE, END)

translator_graph = builder.compile()
