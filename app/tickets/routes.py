from flask import Blueprint, request, jsonify
from flask_jwt_extended import get_jwt_identity, verify_jwt_in_request

from app.extensions import db
from app.models.entities import Ticket, TicketAssignment, Project
from app.utils.security import role_required


tickets_bp = Blueprint('tickets', __name__, url_prefix='/api/tickets')


@tickets_bp.post('')
@role_required('Manager', 'Admin')
def create_ticket():
    data = request.get_json() or {}
    project = Project.query.filter_by(name=data['project_name']).first()
    if not project:
        project = Project(name=data['project_name'])
        db.session.add(project)
        db.session.flush()

    ticket = Ticket(
        project_id=project.id,
        subject=data['subject'],
        description=data['description'],
        priority=data['priority'],
        estimated_hours=data['estimated_hours'],
        start_at=data['start_at'],
        end_at=data['end_at'],
        received_department=data['received_department'],
        created_by=int(get_jwt_identity()),
        status='Assigned' if data.get('assignments') else 'New',
    )
    db.session.add(ticket)
    db.session.flush()

    for assignment in data.get('assignments', []):
        db.session.add(TicketAssignment(
            ticket_id=ticket.id,
            team_id=assignment.get('team_id'),
            user_id=assignment.get('user_id'),
            assignment_type=assignment['assignment_type'],
        ))

    for sub in data.get('sub_tickets', []):
        db.session.add(Ticket(
            parent_ticket_id=ticket.id,
            project_id=project.id,
            subject=sub['subject'],
            description=sub.get('description', data['description']),
            priority=sub.get('priority', data['priority']),
            estimated_hours=sub.get('estimated_hours', data['estimated_hours']),
            start_at=data['start_at'],
            end_at=data['end_at'],
            received_department=data['received_department'],
            created_by=int(get_jwt_identity()),
            status='Assigned',
        ))

    db.session.commit()
    return jsonify({'message': 'Ticket created', 'ticket_id': ticket.id}), 201


@tickets_bp.patch('/<int:ticket_id>/status')
def update_status(ticket_id):
    verify_jwt_in_request()
    role = request.headers.get('X-Role')
    data = request.get_json() or {}
    ticket = Ticket.query.get_or_404(ticket_id)
    if role in {'Employee'} and data['status'] not in {'WIP', 'Completed'}:
        return jsonify({'error': 'Employee cannot set this status'}), 400
    ticket.status = data['status']
    db.session.commit()
    return jsonify({'message': 'Status updated'})


@tickets_bp.get('')
def list_tickets():
    verify_jwt_in_request()
    status = request.args.get('status')
    query = Ticket.query
    if status:
        query = query.filter_by(status=status)
    rows = query.order_by(Ticket.created_at.desc()).all()
    return jsonify([
        {
            'id': t.id,
            'subject': t.subject,
            'status': t.status,
            'priority': t.priority,
            'project': t.project.name,
            'parent_ticket_id': t.parent_ticket_id,
        }
        for t in rows
    ])
