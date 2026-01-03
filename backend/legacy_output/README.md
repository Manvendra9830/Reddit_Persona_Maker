# Backend (FastAPI)

This directory contains the FastAPI backend for the Reddit Persona Generator.

## Running the Backend

To run the backend server, you must be in the **root** of the project directory, not this `backend` directory.

### Local Development (with auto-reload)

From the project root, run:

```bash
uvicorn backend.app.main:app --reload
```

### Production / Stable (no auto-reload)

From the project root, run:

```bash
uvicorn backend.app.main:app
```