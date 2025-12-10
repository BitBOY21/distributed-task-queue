from collections import deque
from threading import Lock
from typing import List, Optional
from app.models.job import Job

class TaskQueue:
    """
    A thread-safe FIFO (First-In-First-Out) queue implementation for managing Jobs.
    Uses a threading Lock to ensure safe access from multiple threads (API & Worker).
    """
    def __init__(self):
        self._queue = deque()
        self._lock = Lock()

    def enqueue(self, job: Job):
        """Adds a job to the end of the queue in a thread-safe manner."""
        with self._lock:
            self._queue.append(job)

    def dequeue(self) -> Optional[Job]:
        """
        Removes and returns the first job from the queue.
        Returns None if the queue is empty.
        """
        with self._lock:
            if not self._queue:
                return None
            return self._queue.popleft()

    def list_jobs(self) -> List[Job]:
        """Returns a snapshot list of all jobs currently in the queue."""
        with self._lock:
            return list(self._queue)