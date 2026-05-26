from io import BytesIO

import pandas as pd
from flask import Blueprint, jsonify, request, send_file
from flask_jwt_extended import verify_jwt_in_request

from app.models.entities import WorkLog, User, Ticket
from app.utils.security import role_required


reports_bp = Blueprint('reports', __name__, url_prefix='/api/reports')


@reports_bp.get('/monthly')
@role_required('Manager', 'Admin')
def monthly_report():
    rows = (
        WorkLog.query.join(User, WorkLog.user_id == User.id)
        .join(Ticket, WorkLog.ticket_id == Ticket.id)
        .add_columns(User.full_name, Ticket.subject, WorkLog.work_date, WorkLog.hours_spent)
        .all()
    )
    payload = [
        {
            'employee_name': r.full_name,
            'ticket_details': r.subject,
            'work_date': str(r.work_date),
            'hours_logged': float(r.hours_spent),
        }
        for r in rows
    ]
    fmt = request.args.get('format', 'json')
    if fmt == 'csv':
        df = pd.DataFrame(payload)
        return df.to_csv(index=False), 200, {'Content-Type': 'text/csv'}
    if fmt == 'xlsx':
        df = pd.DataFrame(payload)
        stream = BytesIO()
        df.to_excel(stream, index=False)
        stream.seek(0)
        return send_file(stream, download_name='monthly_report.xlsx', as_attachment=True)
    return jsonify(payload)
