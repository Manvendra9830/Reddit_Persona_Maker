# Combined README

This file contains the content of all README.md files in the project.

---

## `README.md`

# Reddit Persona Generator

This project is an AI-powered tool that analyzes a Reddit user's public activity and automatically generates a detailed personality and behavioral profile.

## Monorepo Structure

This repository is a monorepo containing two independent projects:


-   `backend/`: A FastAPI application that exposes an API to generate user personas. It uses the Reddit API to scrape user data and a hosted LLM (Groq) to generate the persona.
-   `frontend/`: The frontend of the application, which will be built using Lovable and deployed on Vercel.

See the `README.md` in each directory for more details.

---

## `backend/README.md`

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
