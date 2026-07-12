# Root Academy Cohort Tracker

## Overview

A Flask web app for managing a 10-week Introduction to Data Science cohort at Root Academy. Students can view weekly curriculum, submit their work, track their progress, and read feedback. The admin can review submissions, leave feedback, track student progress, and send reminder emails to students with missing submissions.

Live demo: https://root-academy-cohort-tracker.onrender.com

## Why This Project Exists

Root Academy is a student-centered Introduction to Data Science cohort launching in mid-July 2026. This tracker supports the real workflow of the cohort: students need one place to view weekly expectations and submit work, while the admin needs one dashboard to track progress and provide feedback.

This project is also designed as a focused MLH Fellowship code sample. It uses Python, Flask, Jinja templates, SQLAlchemy, and session-based authentication to keep the app lightweight and readable.

## Features

- Student registration and login with email + cohort code
- Server-rendered curriculum pages
- Weekly submission flow
- Student progress tracking
- Admin dashboard
- Submission review and feedback
- Admin-triggered email reminders
- CSRF-protected forms
- Core pytest test coverage
- GitHub Actions test workflow

## Tech Stack

- Python
- Flask
- Jinja2
- SQLAlchemy
- Flask-Migrate
- Flask-WTF (CSRF protection)
- Flask-Mail
- SQLite (local development) / PostgreSQL (production)
- pytest
- GitHub Actions

## Architecture

The app uses Flask blueprints to separate public routes, authentication, curriculum, submissions, and admin workflows. SQLAlchemy models define students and submissions, while Flask-Migrate manages database schema changes.

## Local Setup

Clone the repository:

```bash
git clone https://github.com/mohamad-755/root-academy-cohort-tracker.git
cd root-academy-cohort-tracker
```

Create and activate a virtual environment:

```bash
python -m venv .venv
```

On Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the app:

```bash
python run.py
```

Open:

```text
http://127.0.0.1:5000
```

## Environment Variables

The app reads configuration from environment variables.

| Variable | Purpose | Default |
| --- | --- | --- |
| `SECRET_KEY` | Flask session signing key | `dev-secret-key` |
| `ADMIN_CODE` | Code used for admin login | `dev-admin-code` |
| `DATABASE_URL` | Database connection string | local SQLite file |
| `MAIL_SERVER` | SMTP server | `localhost` |
| `MAIL_PORT` | SMTP port | `25` |
| `MAIL_USE_TLS` | Enable TLS for SMTP | `false` |
| `MAIL_USERNAME` | SMTP username | unset |
| `MAIL_PASSWORD` | SMTP password | unset |
| `MAIL_DEFAULT_SENDER` | Sender email address | `noreply@rootacademy.local` |
| `MAIL_SUPPRESS_SEND` | Suppress real email sending | `true` |

For local development, `MAIL_SUPPRESS_SEND` defaults to `true` so reminder emails are not actually sent. If `DATABASE_URL` is unset, the app falls back to a local SQLite database.

## Database Setup

This project uses Flask-Migrate (Alembic) to manage schema changes.

Apply migrations to set up or update your database:

```bash
flask db upgrade
```

Run this after cloning the repo, after pulling changes that include new migrations, and again during deployment setup.

## Running Tests

```bash
pytest
```

The test suite uses a temporary SQLite database, so it does not affect the local development database. CSRF protection is disabled in the test configuration so the test client can submit forms without a live token.

## Deployment

This app can be deployed on Render.

Deployed app:

```bash
https://root-academy-cohort-tracker.onrender.com
```

Render production start command:

```bash
flask db upgrade && gunicorn run:app
```

`flask db upgrade` applies any pending migrations without dropping existing data, so it's safe to run on every deploy.

Local development still uses:

```bash
python run.py
```

On Windows, use `python run.py` for local development. Gunicorn is intended for Linux-based deployment environments such as Render or Railway.

Recommended production settings:

- Set a secure `SECRET_KEY`
- Set a secure `ADMIN_CODE`
- Set `DATABASE_URL` to your production PostgreSQL connection string
- Configure SMTP variables if real reminder emails should be sent
- Set `MAIL_SUPPRESS_SEND=false` only after SMTP credentials are configured
- Run `flask db upgrade` during setup and on every deploy

## Screenshots

Screenshots are stored in `docs/screenshots/`:

- `homepage.png` — Student homepage with progress
- `curriculum.png` — Curriculum overview
- `my-submissions.png` — Student progress tracking
- `submit-work.png` — Weekly submission form
- `admin-dashboard.png` — Admin dashboard
- `review-feedback.png` — Feedback review page

## Project Scope

This project intentionally uses a lightweight Flask + SQLAlchemy architecture. The goal is to keep the app understandable, useful, and appropriate for a small cohort workflow rather than turning it into a large platform.

## MLH Code Sample Notes

This repository is maintained as a focused code sample for the MLH Fellowship application. It is intended to demonstrate:

- A complete, working Flask application built from scratch, not a tutorial clone
- Clean separation of concerns via blueprints and SQLAlchemy models
- Real schema management with Flask-Migrate rather than ad hoc SQL
- Working test coverage and a CI workflow via GitHub Actions
- Security fundamentals, including CSRF protection on all form submissions
- A genuine use case: this is the actual tracker running Root Academy's live cohort, not a demo-only project
