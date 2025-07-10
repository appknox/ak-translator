from pydantic import BaseModel, Field
from typing import List, Optional, Literal, Union, Dict


class QueryInfoState(BaseModel):
    string_content_type: Optional[
        Literal[
            "sentence", "paragraph", "html", "code_block", "mixed", "malformed_json"
        ]
    ] = Field(
        description="If the input query is a string, this is the type of the string content. Should be one of the following: sentence, paragraph, html, code_block, mixed content, malformed_json",
    )

    is_malformed_json: bool = Field(
        description="Informs whether the input query is a malformed JSON. Only do this if the input query is a string",
    )

    json_keys_count: Optional[int] = Field(
        description="The number of keys in the JSON object if the input query is a JSON object. Only do this if the input query is a JSON object",
    )

    json_items_count: Optional[int] = Field(
        description="The number of items in the JSON list if the input query is a JSON list. Only do this if the input query is a JSON object",
    )

    malformed_json_issues: Optional[List[str]] = Field(
        description="The issues with the malformed JSON content if the input query is a malformed JSON. Only do this if the input query is a malformed JSON",
    )

    content_summary: str = Field(
        description="A short summary of the content type. Should be in English language",
    )


class TranslationState(BaseModel):
    current_translation: Union[str, dict, List[str], Dict[str, str]] = Field(
        description="The current translation of the input query",
    )

    iteration: int = Field(
        default=0,
        description="The iteration of the translation. Should be incremented by 1 after each translation",
    )


class ReviewState(BaseModel):
    review_decision: Literal["APPROVE", "REDO", "END", None] = Field(
        default=None,
        description="""
          Informs whether the translation should be redone. 
          - APPROVE if the translation is good enough
          - REDO if the translation needs improvement
          - END if the maximum attempts have been reached
          
          The decision should be made based on the review_reasoning and the review_translation_rating.
        """,
    )

    review_reasoning: str = Field(
        description="The reasoning for the review. Should be a short and concise explanation of the review. Always be in English language. Max character limit is 100.",
    )

    defective_keys: List[str] = Field(
        description="The keys that are defective in the translation if input query is a JSON object if available",
    )

    review_iteration: int = Field(
        default=0,
        description="The iteration of the review cycle. Should be incremented by 1 after each review",
    )

    review_translation_rating: int = Field(
        default=0,
        description="The rating of the translation review from 1 to 5. 1 is the worst and 5 is the best. This is the rating of the translation review, not the final translation",
    )


class FormatState(BaseModel):
    final_translation: Union[str, dict, List[str], Dict[str, str]] = Field(
        default="",
        description="The final translation of the input query. Formatted in the target language. It should point to the final translation of the input query",
    )

    final_translation_rating: int = Field(
        default=0,
        description="The rating of the final translation from 1 to 5. 1 is the worst and 5 is the best",
    )


class FixedMalformedJsonState(BaseModel):
    malformed_json_content: str = Field(
        description="The malformed JSON content that needs to be fixed",
    )

    fixed_json_content: Union[dict, List[str], Dict[str, str]] = Field(
        description="The fixed JSON content",
    )


class AgentState(BaseModel):
    original_input_query: Union[str, dict, List[str], Dict[str, str]] = ""
    llm_input_query: str = ""

    target_language: str = Field(
        description="The target language to translate the input query to",
    )

    is_json: bool = Field(
        description="Informs whether the input query is a JSON object",
    )

    is_string: bool = Field(
        description="Informs whether the input query is a string",
    )

    query_info: Optional[QueryInfoState] = None
    translation_state: Optional[TranslationState] = None
    review_state: Optional[ReviewState] = None
    format_state: Optional[FormatState] = None
