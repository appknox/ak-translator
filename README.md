# Translation Validation Service

A monorepo containing a React frontend and Python backend for translating and validating text using LLMs.

## Project Structure

- `frontend/` - Vite React application with Material UI
- `backend/` - Python FastAPI backend service
- `scripts/` - Project setup and management scripts

## Setup

1. Install dependencies:

   ```bash
   # Frontend
   cd frontend
   npm install

   # Backend
   cd backend
   pip install -r requirements.txt
   ```

2. Start development servers:

   ```bash
   # Frontend (in frontend directory)
   npm run dev

   # Backend (in backend directory)
   python -m uvicorn main:app --reload
   ```

## Features

- Text translation using Qwen LLM
- Translation validation service
- Support for various input formats:
  - Single string
  - Multiple strings (object)
  - Text with code blocks
- JSON output with translation results and accuracy metrics

## Tech Stack

### Frontend

- Vite
- React
- Material UI
- TypeScript

### Backend

- Python
- FastAPI
- Qwen LLM
