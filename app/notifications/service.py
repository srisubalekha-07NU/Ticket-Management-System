from calendar import monthrange
from datetime import date

from app.extensions import db
from app.models.entities import User, WorkLog, Notification


def run_month_end_reminders(target_hours=168):
    today = date.today()
    last_day = monthrange(today.year, today.month)[1]
    if today.day not in {27, 28, last_day}:
        return

    employees = User.query.join(User.role).filter_by(name='Employee').all()
    for emp in employees:
        total = sum(
            float(w.hours_spent)
            for w in WorkLog.query.filter(
                WorkLog.user_id == emp.id,
                db.extract('month', WorkLog.work_date) == today.month,
                db.extract('year', WorkLog.work_date) == today.year,
            )
        )
        if total < target_hours:
            missing = target_hours - total
            db.session.add(Notification(user_id=emp.id, message=f'Missing {missing:.2f} hours in current month.'))
    db.session.commit()
