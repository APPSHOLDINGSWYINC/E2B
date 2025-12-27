"""
E2B Error Handling Utilities

Provides standardized error handling, logging, and resolution
capabilities across all E2B components.
"""

import sys
import traceback
from typing import Optional, Dict, Any, Callable
from datetime import datetime
from enum import Enum


class ErrorSeverity(Enum):
    """Error severity levels."""

    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"


class E2BError(Exception):
    """Base exception for E2B errors."""

    def __init__(
        self,
        message: str,
        severity: ErrorSeverity = ErrorSeverity.ERROR,
        context: Optional[Dict[str, Any]] = None,
    ):
        super().__init__(message)
        self.message = message
        self.severity = severity
        self.context = context or {}
        self.timestamp = datetime.utcnow()

    def to_dict(self) -> Dict[str, Any]:
        """Convert error to dictionary format."""
        return {
            "message": self.message,
            "severity": self.severity.value,
            "context": self.context,
            "timestamp": self.timestamp.isoformat(),
            "type": self.__class__.__name__,
        }


class BuildError(E2BError):
    """Raised when build operations fail."""

    pass


class ValidationError(E2BError):
    """Raised when validation fails."""

    pass


class APIError(E2BError):
    """Raised when API operations fail."""

    pass


class EnvironmentError(E2BError):
    """Raised when environment configuration issues occur."""

    pass


class ErrorHandler:
    """Centralized error handler for E2B."""

    def __init__(self, verbose: bool = False, log_file: Optional[str] = None):
        self.verbose = verbose
        self.log_file = log_file
        self.error_count = 0
        self.warning_count = 0

    def log(self, message: str, severity: ErrorSeverity = ErrorSeverity.INFO) -> None:
        """Log a message with severity level."""
        timestamp = datetime.utcnow().isoformat()
        log_entry = f"[{timestamp}] [{severity.value}] {message}"

        if severity == ErrorSeverity.ERROR or severity == ErrorSeverity.CRITICAL:
            self.error_count += 1
        elif severity == ErrorSeverity.WARNING:
            self.warning_count += 1

        if self.verbose or severity in [ErrorSeverity.ERROR, ErrorSeverity.CRITICAL]:
            print(log_entry, file=sys.stderr if severity != ErrorSeverity.INFO else sys.stdout)

        if self.log_file:
            with open(self.log_file, "a") as f:
                f.write(log_entry + "\n")

    def handle_error(
        self,
        error: Exception,
        context: Optional[Dict[str, Any]] = None,
        recovery_action: Optional[Callable] = None,
    ) -> None:
        """Handle an error with optional recovery action."""
        error_info = {
            "type": type(error).__name__,
            "message": str(error),
            "context": context or {},
        }

        if self.verbose:
            error_info["traceback"] = traceback.format_exc()

        self.log(f"Error occurred: {error_info['message']}", ErrorSeverity.ERROR)

        if self.verbose and "traceback" in error_info:
            self.log(f"Traceback:\n{error_info['traceback']}", ErrorSeverity.DEBUG)

        if recovery_action:
            try:
                self.log("Attempting recovery action...", ErrorSeverity.INFO)
                recovery_action()
                self.log("Recovery successful", ErrorSeverity.INFO)
            except Exception as recovery_error:
                self.log(
                    f"Recovery failed: {str(recovery_error)}", ErrorSeverity.CRITICAL
                )

    def handle_validation_error(self, field: str, message: str) -> None:
        """Handle validation errors."""
        error = ValidationError(
            message=f"Validation failed for {field}: {message}",
            severity=ErrorSeverity.ERROR,
            context={"field": field},
        )
        self.handle_error(error)

    def handle_api_error(
        self, endpoint: str, status_code: int, message: str
    ) -> None:
        """Handle API errors."""
        error = APIError(
            message=f"API error at {endpoint}: {message}",
            severity=ErrorSeverity.ERROR,
            context={"endpoint": endpoint, "status_code": status_code},
        )
        self.handle_error(error)

    def get_summary(self) -> Dict[str, int]:
        """Get error and warning counts."""
        return {"errors": self.error_count, "warnings": self.warning_count}

    def reset_counters(self) -> None:
        """Reset error and warning counters."""
        self.error_count = 0
        self.warning_count = 0


def with_error_handling(
    error_handler: ErrorHandler, context: Optional[Dict[str, Any]] = None
):
    """Decorator for automatic error handling."""

    def decorator(func: Callable) -> Callable:
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except E2BError as e:
                error_handler.handle_error(e, context)
                raise
            except Exception as e:
                wrapped_error = E2BError(
                    message=f"Unexpected error in {func.__name__}: {str(e)}",
                    severity=ErrorSeverity.ERROR,
                    context=context,
                )
                error_handler.handle_error(wrapped_error, context)
                raise wrapped_error from e

        return wrapper

    return decorator


# Global error handler instance
_global_handler: Optional[ErrorHandler] = None


def get_error_handler(
    verbose: bool = False, log_file: Optional[str] = None
) -> ErrorHandler:
    """Get or create the global error handler."""
    global _global_handler
    if _global_handler is None:
        _global_handler = ErrorHandler(verbose=verbose, log_file=log_file)
    return _global_handler


# Example usage
if __name__ == "__main__":
    # Create an error handler
    handler = ErrorHandler(verbose=True)

    # Log messages at different severity levels
    handler.log("Starting process", ErrorSeverity.INFO)
    handler.log("Configuration loaded", ErrorSeverity.INFO)
    handler.log("Potential issue detected", ErrorSeverity.WARNING)

    # Handle different types of errors
    try:
        raise BuildError("Build failed due to missing dependencies")
    except BuildError as e:
        handler.handle_error(e, context={"component": "js-sdk"})

    try:
        raise ValidationError("Invalid API key format")
    except ValidationError as e:
        handler.handle_error(e, context={"field": "api_key"})

    # Get summary
    summary = handler.get_summary()
    print(f"\nError Summary: {summary}")
