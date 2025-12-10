import json
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlmodel import Session, select
from app.models.job import Job
from app.core.queue import TaskQueue
from app.core.database import get_session

router = APIRouter()
queue = TaskQueue()

class JobRequest(BaseModel):
    """Schema for submitting a new job."""
    type: str
    payload: dict

@router.post("/jobs", summary="Submit a new job to the queue")
def submit_job(req: JobRequest, session: Session = Depends(get_session)):
    """
    Receives a job request, persists it in the database,
    and adds it to the in-memory task queue for processing by the Worker.
    """
    # Convert dict payload to JSON string for SQLite persistence
    payload_str = json.dumps(req.payload)

    # Create the Job object
    job = Job.create(req.type, payload_str)

    # Save to DB
    session.add(job)
    session.commit()
    session.refresh(job)

    # Enqueue for processing
    queue.enqueue(job)

    return job

@router.get("/jobs/{job_id}", summary="Get job status and results")
def get_job(job_id: str, session: Session = Depends(get_session)):
    """Retrieves the status and result of a specific job by its ID."""
    job = session.get(Job, job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    return job

@router.get("/jobs", summary="List all jobs")
def list_jobs(session: Session = Depends(get_session)):
    """Returns a list of all jobs stored in the database."""
    jobs = session.exec(select(Job)).all()
    return jobs