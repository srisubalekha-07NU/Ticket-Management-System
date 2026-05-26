# Ticket & Employee Work Log Management System

Flask + MySQL enterprise-ready starter for ticketing, team assignments, sub-ticketing, work logs, reminders, and manager reporting.

## Tech Stack
- Backend: Flask, SQLAlchemy, JWT
- Database: MySQL
- Frontend: HTML, CSS, Bootstrap
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
- MVC-style modular structure + REST APIs

## Setup
1. Create DB and tables:
   ```bash
   mysql -u root -p < schema.sql
   ```
2. Install dependencies:
   ```bash
   python -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```
3. Set env vars (optional):
   - `DATABASE_URL=mysql+pymysql://root:password@localhost:3306/ticket_management`
   - `SECRET_KEY=...`
   - `JWT_SECRET_KEY=...`
   - `MONTHLY_TARGET_HOURS=168`
4. Run app:
   ```bash
   python run.py
   ```

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
  services/
  utils/
  templates/
  static/
```
