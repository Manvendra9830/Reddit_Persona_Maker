# Reddit Persona Generator

[![Frontend CI/CD](https://github.com/Manvendra9830/Reddit_Persona_Maker/actions/workflows/frontend-ci-cd.yml/badge.svg)](https://github.com/Manvendra9830/Reddit_Persona_Maker/actions/workflows/frontend-ci-cd.yml)
[![Backend CI/CD](https://github.com/Manvendra9830/Reddit_Persona_Maker/actions/workflows/backend-ci-cd.yml/badge.svg)](https://github.com/Manvendra9830/Reddit_Persona_Maker/actions/workflows/backend-ci-cd.yml)

This project is an AI-powered tool that analyzes a Reddit user's public activity and automatically generates a detailed personality and behavioral profile.

## Deployed Applications

*   **Frontend (Vercel):** [https://redditpersonamaker.vercel.app/](https://redditpersonamaker.vercel.app/)
*   **Backend (Render):** [https://reddit-persona-maker-new.onrender.com/docs](https://reddit-persona-maker-new.onrender.com/docs)

## Monorepo Structure

This repository is a monorepo containing two independent projects:

-   `backend/`: A FastAPI application that exposes an API to generate user personas.
-   `frontend/`: The frontend of the application, built with React and Vite.

## Tech Stack

### Frontend

*   **Framework:** React
*   **Build Tool:** Vite
*   **Language:** TypeScript
*   **Styling:** Tailwind CSS
*   **UI Components:** shadcn/ui

### Backend

*   **Framework:** FastAPI
*   **Reddit API Wrapper:** PRAW
*   **LLM:** Groq
*   **Server:** Uvicorn

## Running Locally

### Backend

To run the backend server, you must be in the **root** of the project directory.

1.  **Install dependencies:**
    ```bash
    pip install -r backend/requirements.txt
    ```

2.  **Run the server:**
    *   For local development with auto-reload:
        ```bash
        uvicorn backend.api:app --reload
        ```
    *   For production/stable mode:
        ```bash
        uvicorn backend.api:app
        ```

### Frontend

To run the frontend development server:

1.  **Navigate to the frontend directory:**
    ```bash
    cd frontend
    ```

2.  **Install dependencies:**
    ```bash
    npm install
    ```

3.  **Create a `.env` file:**
    Copy the `.env.example` to `.env` and make sure the `VITE_API_BASE_URL` is pointing to your local backend (e.g., `http://127.0.0.1:8000`).

4.  **Run the dev server:**
    ```bash
    npm run dev
    ```