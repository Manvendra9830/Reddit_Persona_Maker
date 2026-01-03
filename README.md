
# Reddit Persona Generator

This project is an AI-powered tool that analyzes a Reddit user's public activity and automatically generates a detailed personality and behavioral profile.

## Monorepo Structure

This repository is a monorepo containing two independent projects:


-   `backend/`: A FastAPI application that exposes an API to generate user personas. It uses the Reddit API to scrape user data and a hosted LLM (Groq) to generate the persona.
-   `frontend/`: The frontend of the application, which will be built using Lovable and deployed on Vercel.

See the `README.md` in each directory for more details.
