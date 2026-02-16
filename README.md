# Datasheet Manager

A Django-based time tracking and todo workspace with a polished UI, Jalali date support, and exportable timesheets. The project combines:

- A focus timer for capturing work sessions
- Project and tag management
- A Kanban-style todo board with live updates (HTMX)
- Performance dashboards with charts
- CSV/Excel export for reports

## Features

- **Timer**: Start, pause, resume, reset, and save sessions against projects
- **Todo Board**: Create tasks, move between lanes, delete, and update without full page reloads
- **Performance**: Daily and monthly summaries with doughnut charts
- **Exports**: Filter by date, project, or tag and export as CSV/Excel
- **Themes**: Light and dark modes with a persistent toggle

## Tech Stack

- **Backend**: Django 5
- **UI**: Custom CSS + HTMX
- **Charts**: Chart.js
- **Dates**: Jalali date support

## Project Structure

- `datasheet/` Django project settings
- `timer/` Timer, exports, performance dashboard
- `todo/` Todo board app
- `static/` Static assets

## Setup (Local)

### 1) Create and activate a virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 2) Install dependencies

```bash
pip install -r requirements.txt
```

### 3) Configure environment

Create a `.env` file next to `manage.py`:

```env
DJANGO_SECRET_KEY=replace-me
DJANGO_DEBUG=True
DJANGO_ALLOWED_HOSTS=127.0.0.1,localhost
DJANGO_CSRF_TRUSTED_ORIGINS=
```

### 4) Run migrations

```bash
python3 manage.py migrate
```

### 5) Create admin user (optional)

```bash
python3 manage.py createsuperuser
```

### 6) Start the server

```bash
python3 manage.py runserver
```

Open: `http://127.0.0.1:8000/`

## Docker

### Build

```bash
docker build -t datasheet-manager .
```

### Run

```bash
docker run -p 8000:8000 \
  -e DJANGO_SECRET_KEY=replace-me \
  -e DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1 \
  datasheet-manager
```

Open: `http://127.0.0.1:8000/`

## Usage

### Timer

1. Start the timer
2. Add task details and choose a project
3. Save the session to store the record
4. Export records when needed

### Todo Board

1. Create tasks with optional due date and priority
2. Move items between Todo, Doing, and Done
3. Changes update without full page reload

### Performance

- View daily and monthly summaries
- Project breakdowns are visualized using charts

## Notes

- The todo due date uses `datetime-local` and prevents selecting past dates
- Static files are collected automatically when building the Docker image
- Production settings are driven by environment variables

## Environment Variables

- `DJANGO_SECRET_KEY` (required in production)
- `DJANGO_DEBUG` (True/False)
- `DJANGO_ALLOWED_HOSTS` (comma-separated)
- `DJANGO_CSRF_TRUSTED_ORIGINS` (comma-separated)
