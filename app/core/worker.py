import time
import json
from threading import Event
from sqlmodel import Session
from app.models.job import Job, JobStatus
from app.core.database import engine


def process_job(job: Job) -> str:
    """
    Simulates a heavy background task (CPU bound or I/O bound).
    In a real app, this would resize images, send emails, or train models.
    """
    print(f"👷 Worker: Starting job {job.id} ({job.type})")

    # Simulate work duration (5 seconds)
    time.sleep(5)

    # Deserialize payload from JSON string to dictionary if needed
    try:
        payload_data = json.loads(job.payload)
    except json.JSONDecodeError:
        payload_data = {}

    # Logic for specific job types
    if job.type == "error_test":
        raise Exception("Simulated Failure requested by user")

    return f"Processed successfully: {payload_data}"


def update_job_status(job_id, status: JobStatus, result: str = None):
    """
    Helper function to update the job status in the database safely.
    Uses a fresh session for each update to avoid thread-safety issues.
    """
    with Session(engine) as session:
        job = session.get(Job, job_id)
        if job:
            job.status = status
            if result:
                job.result = result
            session.add(job)
            session.commit()


def run_worker(queue, stop_event: Event):
    """
    The main loop for the background worker thread.
    Continuously polls the queue for new jobs and processes them.
    """
    print("🚀 Worker thread started...")

    while not stop_event.is_set():
        # Get next job from the thread-safe queue
        job = queue.dequeue()

        if not job:
            # Avoid busy-waiting if queue is empty
            time.sleep(1)
            continue

        # 1. Update status to RUNNING
        update_job_status(job.id, JobStatus.RUNNING)
        print(f"🔄 Job {job.id} is RUNNING")

        try:
            # 2. Execute the actual work
            result = process_job(job)

            # 3. Update status to DONE
            update_job_status(job.id, JobStatus.DONE, result)
            print(f"✅ Job {job.id} is DONE")

        except Exception as e:
            # 4. Handle failures gracefully
            update_job_status(job.id, JobStatus.FAILED, str(e))
            print(f"❌ Job {job.id} FAILED: {e}")