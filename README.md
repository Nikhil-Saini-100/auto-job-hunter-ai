# Auto Job Hunter AI

A production-grade autonomous AI job hunting and application platform.

## Features

- **Master Profile System**: Manage your master resume and preferences.
- **Automatic Job Discovery Engine**: Scans job boards for matching jobs.
- **Job Analyzer**: Uses AI to parse, score, and rank jobs based on relevance.
- **Resume Tailoring**: Generates ATS-friendly resumes for specific roles.
- **Cover Letter Engine**: Writes targeted cover letters automatically.
- **Autonomous Apply Engine**: Applies to roles with your permission.
- **Application Tracker**: Kanban board for application tracking.

## Technology Stack

- **Frontend**: Next.js, React, TailwindCSS, TypeScript
- **Backend**: FastAPI, Python, SQLAlchemy, Playwright, Celery
- **Database**: PostgreSQL (Docker) / SQLite (Local)

## Running Locally

### With Docker Compose
```bash
docker-compose up --build
```
- Frontend: http://localhost:3000
- Backend: http://localhost:8000
- API Docs: http://localhost:8000/docs
