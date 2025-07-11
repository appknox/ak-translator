from pydantic import BaseModel, Field
from typing import List, Optional, Literal, Union, Dict


class QueryInfoState(BaseModel):
    string_content_type: Optional[Literal["string", "json", "malformed_json"]] = None
    next_action: Literal["fix_malformed_json", "end"] = "end"
    malformed_json_issues: Optional[List[str]] = []


class FixedMalformedJsonState(BaseModel):
    content_was_fixed: bool = Field(
        default=False,
        description="Whether the content was fixed",
    )

    malformed_json_content: str = Field(
        default="",
        description="The malformed JSON content that needs to be fixed",
    )

    fixed_json_content: Union[dict, List[str], Dict[str, str]] = Field(
        description="The fixed JSON content",
    )


class QueryAssessmentState(BaseModel):
    input_query: str = ""
    query_info: Optional[QueryInfoState] = None
    fixed_json_state: Optional[FixedMalformedJsonState] = None


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
        """,
    )

    review_reasoning: str = Field(
        description="""
          The reasoning for the review. 
          Should be a short and concise explanation of the review. 
          Always be in English language. 
          Max character limit is 100.
        """,
    )

    issues: List[str] = Field(
        description="The issues that are present in the translation",
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


class TranslationAgentState(BaseModel):
    input_query: Union[str, dict, List[str], Dict[str, str]] = ""

    target_language: str = Field(
        description="The target language to translate the input query to",
    )

    translation_state: Optional[TranslationState] = None
    review_state: Optional[ReviewState] = None
    format_state: Optional[FormatState] = None
