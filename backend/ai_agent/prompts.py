import json
import textwrap
from typing import Dict, Any


def output_format_instructions(model_json_schema: Dict[str, Any]):
    return json.dumps(model_json_schema["properties"])


def query_assessment_system_prompt():
    return textwrap.dedent(
        """
        You are a helpful assistant that tells if a string is a malformed JSON or not.
        A malformed JSON content is content that has key value pairs that are not properly formatted.
        Otherwise, the content is a string.

        \n\n
        Check if this content is a malformed JSON: \n\n{input_query}
        \n\n
        Your output should conform to the following format:
        {format_instructions}
        """
    )


def translate_system_prompt():
    return textwrap.dedent(
        """
            Translate the following text from English into {target_language}:
            \n\n
            {input_query}

            \n\n
            CRITICAL INFORMATION:
            Ensure that the context is preserved for each translated content.
            The content type should also be preserved.

            REQUIRED OUTPUT FORMAT:           
            {format_instructions}
        """
    )


def redo_translate_system_prompt():
    return textwrap.dedent(
        """
            Improve the following translation:
            \n\n
            {current_translation}

            Only focus on the issues below:
            {issues}
            \n\n
            
            After fixing the issues, return the newer translation content with the updated fixes.

            REQUIRED OUTPUT FORMAT:           
            {format_instructions}
        """
    )


def review_system_prompt():
    return textwrap.dedent(
        """
        Review the following translated translation and tell which issues are present in the translation.
        Be critical with the review. If it's a JSON object perform a value to value comparison with the original content.

        \n\n
        Translated Content: \n\n{current_translation}
        \n\n
        Original Content: \n\n{input_query}

        Then, output the issues in the following format provided below.

        \n\n

        Return APPROVE if the translation is good enough.
        Return REDO if the translation needs improvement or if you find any issues.

        \n\n
        REQUIRED OUTPUT FORMAT:           
        {format_instructions}
    """
    )


def malformed_json_system_prompt():
    return textwrap.dedent(
        """
        You are a helpful assistant that fixes malformed JSON.
        Fix the following malformed JSON: \n\n{input_query}
        \n\n
        The issues with the malformed JSON are: \n\n{issues}
        \n\n
        Your output should conform to the following format:
        {format_instructions}
        \n\n
    """
    )


def format_translation_system_prompt():
    return textwrap.dedent(
        """
            You are a professional content formatter.
            Your task is to ensure that the structure of the final translation matches the structure of the input query (that was initially provided).
            Format the final translation to be the same as the input query then return the formatted final translation.

            The INPUT QUERY is:
            {input_query}

            \n\n

            Final Translation:
            {translated_content}

            \n\n
            CRITICAL INFORMATION:
            Ensure that the context is preserved for each translated content.
            The content returned should always be the translated content ONLY properly formatted.

            REQUIRED OUTPUT FORMAT:
            {format_instructions}
        """
    )
