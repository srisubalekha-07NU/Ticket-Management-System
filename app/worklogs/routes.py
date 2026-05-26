from datetime import date

from flask import Blueprint, request, jsonify
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity
from sqlalchemy import func

from app.config import Config
from app.extensions import db
from app.models.entities import WorkLog


worklogs_bp = Blueprint('worklogs', __name__, url_prefix='/api/worklogs')


@worklogs_bp.post('')
def create_worklog():
    verify_jwt_in_request()
    data = request.get_json() or {}
    wl = WorkLog(
        ticket_id=data['ticket_id'],
        user_id=int(get_jwt_identity()),
        work_date=data['work_date'],
        hours_spent=data['hours_spent'],
        activity_id=data['activity_id'],
        comments=data.get('comments'),
    )
    db.session.add(wl)
    db.session.commit()
    return jsonify({'message': 'Work log created'}), 201


@worklogs_bp.get('/summary/monthly')
def monthly_summary():
    verify_jwt_in_request()
    user_id = int(request.args.get('user_id', get_jwt_identity()))
    current_month = date.today().month
    current_year = date.today().year
    total = db.session.query(func.coalesce(func.sum(WorkLog.hours_spent), 0)).filter(
        WorkLog.user_id == user_id,
        func.month(WorkLog.work_date) == current_month,
        func.year(WorkLog.work_date) == current_year,
    ).scalar()
    target = Config.MONTHLY_TARGET_HOURS
    return jsonify(
        {
            'target_hours': target,
            'completed_hours': float(total),
            'missing_hours': max(target - float(total), 0),
            'overlogged_hours': max(float(total) - target, 0),
        }
    )
