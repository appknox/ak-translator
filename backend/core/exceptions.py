class TranslationError(Exception):
    """Base exception for translation service errors."""

    def __init__(self, message: str = "An error occurred during translation"):
        self.message = message
        super().__init__(self.message)



class ValidationError(TranslationError):
    """Exception raised when input validation fails."""

    def __init__(self, message: str = "Input validation failed"):
        super().__init__(message)


class ConfigurationError(TranslationError):
    """Exception raised when there's a configuration-related error."""

    def __init__(self, message: str = "Configuration error occurred"):
        super().__init__(message)


class ModelNotFoundError(TranslationError):
    """Exception raised when the specified model is not found or not loaded."""

    def __init__(self, model_name: str):
        super().__init__(
            f"Model '{model_name}' not found or not loaded", status_code=404
        )
