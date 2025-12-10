# ⚡ Distributed Task Queue System

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?style=for-the-badge&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.95%2B-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-Enabled-2496ED?style=for-the-badge&logo=docker&logoColor=white)
![SQLModel](https://img.shields.io/badge/SQLModel-SQLite-orange?style=for-the-badge)

A robust, asynchronous task processing system built with **FastAPI**, **SQLModel**, and a generic **Background Worker**.

This project implements the **Producer-Consumer design pattern** to handle heavy background operations without blocking the main application thread. It is fully containerized using Docker and supports data persistence.

---

## 🏗️ System Architecture

The system decouples the **Producer** (API) from the **Consumer** (Worker) using a thread-safe queue and a persistent database state.

```mermaid
sequenceDiagram
    participant Client
    participant API as FastAPI Server
    participant DB as SQLite DB
    participant Queue as In-Memory Queue
    participant Worker as Background Worker

    Note over Client, API: 1. Submission Phase
    Client->>API: POST /jobs (Create Task)
    API->>DB: Save Job (Status: PENDING)
    API->>Queue: Push Job to Queue
    API-->>Client: Return Job ID (200 OK)
    
    Note right of Client: Client receives ID immediately (Non-blocking)

    Note over Queue, Worker: 2. Processing Phase
    loop Background Process
        Worker->>Queue: Dequeue Job
        Worker->>DB: Update Status (RUNNING)
        Worker->>Worker: Process Payload (Simulated Heavy Task)
        alt Success
            Worker->>DB: Update Status (DONE) + Result
        else Failure
            Worker->>DB: Update Status (FAILED) + Error Info
        end
    end
````

-----

## 🚀 Key Features

  * **Asynchronous Processing:** Non-blocking task submission. The API responds immediately while the worker processes data in the background.
  * **Persistence:** Uses **SQLite** (via SQLModel) to ensure job states (`PENDING`, `RUNNING`, `DONE`) survive server restarts.
  * **Thread Safety:** Implements `threading.Lock` mechanisms to prevent race conditions when accessing the shared queue.
  * **Dockerized:** Fully ready for production with **Docker** & **Docker Compose**.
  * **Robust Error Handling:** Captures worker failures and updates job status with error details in the database.

-----

## 🛠️ Tech Stack

  * **Backend Framework:** FastAPI
  * **Database & ORM:** SQLModel (SQLAlchemy wrapper) with SQLite
  * **Concurrency:** Python `threading` module (Daemon Threads)
  * **Containerization:** Docker & Docker Compose
  * **Validation:** Pydantic

-----

## 📦 How to Run

### Option 1: Using Docker (Recommended) 🐳

The easiest way to run the system is using Docker Compose. This ensures a consistent environment without installing Python dependencies locally.

1.  **Clone the repository:**

    ```bash
    git clone https://github.com/BitBOY21/distributed-task-queue.git
    cd distributed-task-queue
    ```

2.  **Run with Docker Compose:**

    ```bash
    docker-compose up --build
    ```

3.  **Access the API:**
    Open your browser at [http://localhost:8000/docs](https://www.google.com/search?q=http://localhost:8000/docs) to see the Swagger UI.

### Option 2: Local Development 🐍

If you prefer running it directly on your machine:

1.  **Install dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

2.  **Start the server:**

    ```bash
    uvicorn main:app --reload
    ```

-----

## 🔌 API Reference

You can test the API directly via the Swagger UI (`/docs`), or use `curl`.

### 1\. Submit a New Job

Create a task to be processed in the background.

**Request:** `POST /jobs`

```json
{
  "type": "email_processing",
  "payload": {
    "email": "user@example.com",
    "subject": "Welcome to the platform!"
  }
}
```

**Response:**

```json
{
  "id": "a1b2c3d4-e5f6-4a5b-...",
  "status": "PENDING",
  "type": "email_processing",
  "created_at": "2025-10-27T10:00:00"
}
```

### 2\. Check Job Status

Poll the status of a specific job using its ID.

**Request:** `GET /jobs/{job_id}`

**Response (After processing):**

```json
{
  "id": "a1b2c3d4-e5f6-4a5b-...",
  "status": "DONE",
  "result": "Processed successfully: {'email': 'user@example.com'}",
  "created_at": "2025-10-27T10:00:00"
}
```

-----

## 📂 Project Structure

```text
distributed-task-queue/
├── app/
│   ├── api/            # API Route handlers (Producer logic)
│   ├── core/           # Core logic (DB connection, Queue implementation, Worker)
│   └── models/         # SQLModel Database definitions (Job, JobStatus)
├── main.py             # Application entry point & Lifecycle manager
├── Dockerfile          # Docker build instructions
├── docker-compose.yml  # Container orchestration & Volume mapping
└── requirements.txt    # Python dependencies
```

-----

## 🔮 Future Improvements

To scale this system for a production environment with multiple servers, the following upgrades are planned:

  * **Redis / RabbitMQ:** Replace the in-memory `deque` with an external message broker to allow multiple worker instances across different machines.
  * **PostgreSQL:** Migrate from SQLite to PostgreSQL for better concurrency handling.
  * **WebSockets:** Implement real-time status updates to the client (push notification) instead of polling.

<!-- end list -->

```
```
