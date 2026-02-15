# FastAPI Simple Time Backend

This project implements a minimal backend service using FastAPI that returns the current server time. It is containerized using Docker for easy deployment.

## Project Structure

The project consists of the following files:
- [`main.py`](main.py): The FastAPI application logic.
- [`requirements.txt`](requirements.txt): Python dependencies.
- [`Dockerfile`](Dockerfile): Instructions for building the Docker image.
- [`README.md`](README.md): This file.

## Running Locally (Without Docker)

1.  **Install Dependencies:**
    Ensure Python and `pip` are installed. Then run:
    ```bash
    pip install -r requirements.txt
    ```

2.  **Run the Server:**
    ```bash
    uvicorn main:app --reload
    ```
    The service will be available at `http://127.0.0.1:8000`.

## Running with Docker

This is the recommended way to run the service.

1.  **Build the Docker Image:**
    Run this command from the project root:
    ```bash
    docker build -t fastapitime .
    ```

2.  **Run the Container:**
    ```bash
    docker run -d -p 8000:8000 --name time-service fastapitime
    ```

## API Endpoints

| Method | Path | Description |
| :--- | :--- | :--- |
| `GET` | `/` | Returns a status message. |
| `GET` | `/time` | Returns the current server time in ISO 8601 format. |

**Example Response for `/time`:**
```json
{
  "current_time": "2026-02-15T12:48:00.733123"
}
