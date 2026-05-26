# Ticket & Employee Work Log Management System

Flask + MySQL backend with a React (Vite) frontend for enterprise ticketing, team assignments, sub-ticketing, work logs, reminders, and manager reporting.

## Tech Stack
- Backend: Flask, SQLAlchemy, JWT
- Database: MySQL
- Frontend: React, Vite, Bootstrap
- Scheduler: APScheduler
- Exports: CSV, XLSX (Pandas/OpenPyXL)

## Features
- Role-based authentication (Admin, Manager, Employee)
- Ticket creation with priority, dates, assignment, and parent/child sub-ticket relation
- Ticket status workflow (New → Assigned → WIP → Completed → Closed/Reopened)
- Daily work logs with activity type and per-ticket hours
- Monthly summary calculations (target/completed/missing/overlogged)
- Automated reminders on 27th, 28th, and month-end for missing hours
- Manager-only monthly report endpoints with CSV/XLSX export
- React dashboard/pages for login, tickets, worklogs, reports

## Setup
### 1) Database
```bash
mysql -u root -p < schema.sql
```

### 2) Backend
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python run.py
```
Backend runs on `http://localhost:5000`.

### 3) Frontend (React)
```bash
cd frontend
npm install
npm run dev
```
Frontend runs on `http://localhost:5173` and proxies `/api` calls to Flask.

## API Endpoints
### Auth
- `POST /api/auth/register`
- `POST /api/auth/login`

### Tickets
- `POST /api/tickets` (Manager/Admin)
- `GET /api/tickets`
- `PATCH /api/tickets/<id>/status`

### Work Logs
- `POST /api/worklogs`
- `GET /api/worklogs/summary/monthly`

### Reports (Manager/Admin)
- `GET /api/reports/monthly?format=json|csv|xlsx`

## Default Activity Types
Design, Development, Testing, Hosting, Meeting, DB Development, Leave, Permission, IT Support,
Idle Hours, Misc Hours, Issue Fixes, Issue Fixes on Other Modules, Requirement Analysis & Planning,
Development Exceeded, Bug Fixes Testing, R&D.

## Project Structure
```
app/
  auth/
  tickets/
  worklogs/
  reports/
  notifications/
  models/
  utils/
frontend/
  src/
    components/
    context/
    pages/
    services/
```
