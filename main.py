import threading
from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.api.jobs import router as jobs_router, queue
from app.core.worker import run_worker
from app.core.database import create_db_and_tables

# Global event to signal the worker thread to stop gracefully
stop_event = threading.Event()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan context manager for the FastAPI application.
    Handles system startup (DB init, Worker start) and shutdown.
    """
    # --- Startup Phase ---

    # 1. Initialize the database and create tables if they don't exist
    create_db_and_tables()
    print("📁 Database and tables created!")

    # 2. Start the background worker thread
    # The worker runs in a separate thread but shares the same memory space (queue)
    worker_thread = threading.Thread(
        target=run_worker,
        args=(queue, stop_event),
        daemon=True
    )
    worker_thread.start()

    yield  # The application handles requests during this phase

    # --- Shutdown Phase ---
    print("🛑 Shutting down worker...")

    # Signal the worker to stop and wait for it to finish cleanly
    stop_event.set()
    worker_thread.join()


# Initialize FastAPI app
app = FastAPI(
    title="Distributed Task Queue",
    description="A robust async task queue system using FastAPI, SQLite, and threading.",
    version="1.0.0",
    lifespan=lifespan
)

# Register the API router
app.include_router(jobs_router)