import re
from typing import Tuple
from services.ollama_service import ollama_service


class ValidationService:
    @staticmethod
    def validate_translation(
        original: str, translation: str, target_language: str
    ) -> Tuple[float, str]:
        """Validate translation and return accuracy score with explanation."""

        prompt = f"""You are a professional translator and translation validator. 
                  Evaluate the accuracy of this translation from English to {target_language}.

                  Original text: {original}
                  Translation: {translation}

                  Provide:
                  1. A score between 0 and 1 (where 1 is perfect)
                  2. A brief explanation of the score

                  Format your response exactly as:
                  Score: [number]
                  Explanation: [your explanation]
                """

        response = ollama_service.generate(prompt)

        try:
            # Extract score
            score_match = re.search(r"Score:\s*(0\.\d+|1\.0|1|0)", response)
            score = float(score_match.group(1)) if score_match else 0.5

            # Extract explanation
            explanation = (
                response.split("Explanation:", 1)[1].strip()
                if "Explanation:" in response
                else response
            )

            return score, explanation
        except (ValueError, IndexError, AttributeError) as e:
            return 0.5, f"Error parsing response: {str(e)}"


validation_service = ValidationService()
