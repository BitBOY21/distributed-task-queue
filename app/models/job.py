from enum import Enum
from datetime import datetime
from uuid import UUID, uuid4
from typing import Optional
from sqlmodel import SQLModel, Field


class JobStatus(str, Enum):
    """Enum representing the possible states of a background job."""
    PENDING = "PENDING"
    RUNNING = "RUNNING"
    DONE = "DONE"
    FAILED = "FAILED"


class Job(SQLModel, table=True):
    """
    Database model representing a task in the system.
    """
    # Unique Identifier (Primary Key)
    id: UUID = Field(default_factory=uuid4, primary_key=True)

    # Type of the job (e.g., 'email', 'image_resize')
    type: str

    # Job input data.
    # Note: Stored as a JSON string because standard SQLite does not support native JSON types.
    payload: str

    # Current lifecycle state
    status: JobStatus = Field(default=JobStatus.PENDING)

    # Output result or error message (optional)
    result: Optional[str] = None

    # Creation timestamp
    created_at: datetime = Field(default_factory=datetime.utcnow)

    @staticmethod
    def create(job_type: str, payload_str: str) -> "Job":
        """Factory method to create a new pending job."""
        return Job(
            type=job_type,
            payload=payload_str,
            status=JobStatus.PENDING
        )