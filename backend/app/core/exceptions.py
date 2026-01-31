"""Custom exceptions for the application"""

from fastapi import HTTPException, status


class MathNoteException(Exception):
    """Base exception for MathNote application"""

    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)


class VideoNotFoundError(MathNoteException):
    """Raised when video is not found"""

    pass


class VideoProcessingError(MathNoteException):
    """Raised when video processing fails"""

    pass


class StorageError(MathNoteException):
    """Raised when storage operation fails"""

    pass


class LLMError(MathNoteException):
    """Raised when LLM operation fails"""

    pass


class TaskNotFoundError(MathNoteException):
    """Raised when task is not found"""

    pass


# HTTP Exception factories
def video_not_found_exception(task_id: str) -> HTTPException:
    return HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Video with task_id '{task_id}' not found",
    )


def task_not_found_exception(task_id: str) -> HTTPException:
    return HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Task '{task_id}' not found",
    )


def processing_error_exception(message: str) -> HTTPException:
    return HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail=f"Processing error: {message}",
    )
