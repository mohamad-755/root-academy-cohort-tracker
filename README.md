# Root Academy Cohort Tracker

A Flask web app for managing a 10-week Introduction to Data Science cohort at Root Academy.

Students can view weekly curriculum, submit their work, track their progress, and read feedback. The admin can review submissions, leave feedback, track student progress, and send reminder emails to students with missing submissions.

## Why This Project Exists

Root Academy is a student-centered Introduction to Data Science cohort launching in mid-July 2026. This tracker supports the real workflow of the cohort: students need one place to view weekly expectations and submit work, while the admin needs one dashboard to track progress and provide feedback.

This project is also designed as a focused MLH Fellowship code sample. It uses Python, Flask, Jinja templates, SQLite, and session-based authentication to keep the app lightweight and readable.

## Features

- Student registration and login with email + cohort code
- Server-rendered curriculum pages
- Weekly submission flow
- Student progress tracking
- Admin dashboard
- Submission review and feedback
- Admin-triggered email reminders
- Core pytest test coverage
- GitHub Actions test workflow

## Tech Stack

- Python
- Flask
- Jinja2
- SQLite
- Flask-Mail
- pytest
- GitHub Actions

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

Initialize the database:

```bash
flask init-db
```

Run the app:

```bash
python run.py
```

Open:

```text
http://127.0.0.1:5000
```

## Configuration

The app reads configuration from environment variables.

| Variable | Purpose | Default |
| --- | --- | --- |
| `SECRET_KEY` | Flask session signing key | `dev-secret-key` |
| `ADMIN_CODE` | Code used for admin login | `dev-admin-code` |
| `MAIL_SERVER` | SMTP server | `localhost` |
| `MAIL_PORT` | SMTP port | `25` |
| `MAIL_USE_TLS` | Enable TLS for SMTP | `false` |
| `MAIL_USERNAME` | SMTP username | unset |
| `MAIL_PASSWORD` | SMTP password | unset |
| `MAIL_DEFAULT_SENDER` | Sender email address | `noreply@rootacademy.local` |
| `MAIL_SUPPRESS_SEND` | Suppress real email sending | `true` |

For local development, `MAIL_SUPPRESS_SEND` defaults to `true` so reminder emails are not actually sent.

## Running Tests

```bash
pytest
```

The test suite uses a temporary SQLite database, so it does not affect the local development database.

## Admin Access In Development

The default development admin code is:

```text
dev-admin-code
```

In production, set a real `ADMIN_CODE` environment variable.

## Deployment Notes

This app can be deployed on Render or Railway.

Production start command:

```bash
gunicorn run:app
```

Recommended production settings:

- Set a secure `SECRET_KEY`
- Set a secure `ADMIN_CODE`
- Configure SMTP variables if real reminder emails should be sent
- Set `MAIL_SUPPRESS_SEND=false` only after SMTP credentials are configured
- Run `flask init-db` during setup or before first use

Local development still uses:

```bash
python run.py
```

On Windows, use `python run.py` for local development. Gunicorn is intended for Linux-based deployment environments such as Render or Railway.## Deployment Notes

This app can be deployed on Render or Railway.

Production start command:

```bash
gunicorn run:app
```

Recommended production settings:

- Set a secure `SECRET_KEY`
- Set a secure `ADMIN_CODE`
- Configure SMTP variables if real reminder emails should be sent
- Set `MAIL_SUPPRESS_SEND=false` only after SMTP credentials are configured
- Run `flask init-db` during setup or before first use

Local development still uses:

```bash
python run.py
```

On Windows, use `python run.py` for local development. Gunicorn is intended for Linux-based deployment environments such as Render or Railway.

## Screenshots

Screenshots will be added after deployment.

Suggested screenshots:

- Student homepage with progress
- Curriculum overview
- Weekly submission form
- Admin dashboard
- Feedback review page

## Project Scope

This project intentionally uses a lightweight Flask + SQLite architecture. The goal is to keep the app understandable, useful, and appropriate for a small cohort workflow rather than turning it into a large platform.