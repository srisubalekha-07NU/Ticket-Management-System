from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

from app.extensions import db, login_manager


user_teams = db.Table(
    'user_teams',
    db.Column('user_id', db.Integer, db.ForeignKey('users.id'), primary_key=True),
    db.Column('team_id', db.Integer, db.ForeignKey('teams.id'), primary_key=True),
)


class TimestampMixin:
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class Role(db.Model, TimestampMixin):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), unique=True, nullable=False)


class User(UserMixin, db.Model, TimestampMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'), nullable=False)
    is_active_user = db.Column(db.Boolean, default=True)
    role = db.relationship('Role', backref='users')
    teams = db.relationship('Team', secondary=user_teams, backref='members')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class Team(db.Model, TimestampMixin):
    __tablename__ = 'teams'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)


class Project(db.Model, TimestampMixin):
    __tablename__ = 'projects'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), unique=True, nullable=False)


class Ticket(db.Model, TimestampMixin):
    __tablename__ = 'tickets'
    id = db.Column(db.Integer, primary_key=True)
    parent_ticket_id = db.Column(db.Integer, db.ForeignKey('tickets.id'))
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'), nullable=False)
    subject = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=False)
    priority = db.Column(db.Enum('Low', 'Medium', 'High', 'Critical', name='priority_enum'), nullable=False)
    estimated_hours = db.Column(db.Numeric(8, 2), nullable=False)
    start_at = db.Column(db.DateTime, nullable=False)
    end_at = db.Column(db.DateTime, nullable=False)
    received_department = db.Column(db.String(100), nullable=False)
    status = db.Column(
        db.Enum('New', 'Assigned', 'WIP', 'On Hold', 'Completed', 'Closed', 'Reopened', name='status_enum'),
        default='New',
        nullable=False,
    )
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    project = db.relationship('Project', backref='tickets')
    parent_ticket = db.relationship('Ticket', remote_side=[id], backref='sub_tickets')


class TicketAssignment(db.Model, TimestampMixin):
    __tablename__ = 'ticket_assignments'
    id = db.Column(db.Integer, primary_key=True)
    ticket_id = db.Column(db.Integer, db.ForeignKey('tickets.id'), nullable=False)
    team_id = db.Column(db.Integer, db.ForeignKey('teams.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    assignment_type = db.Column(db.Enum('TEAM', 'USER', name='assignment_type_enum'), nullable=False)


class Activity(db.Model):
    __tablename__ = 'activities'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)


class WorkLog(db.Model, TimestampMixin):
    __tablename__ = 'work_logs'
    id = db.Column(db.Integer, primary_key=True)
    ticket_id = db.Column(db.Integer, db.ForeignKey('tickets.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    work_date = db.Column(db.Date, nullable=False)
    hours_spent = db.Column(db.Numeric(5, 2), nullable=False)
    activity_id = db.Column(db.Integer, db.ForeignKey('activities.id'), nullable=False)
    comments = db.Column(db.Text)


class Notification(db.Model, TimestampMixin):
    __tablename__ = 'notifications'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    message = db.Column(db.Text, nullable=False)
    is_read = db.Column(db.Boolean, default=False)


class Attachment(db.Model, TimestampMixin):
    __tablename__ = 'attachments'
    id = db.Column(db.Integer, primary_key=True)
    ticket_id = db.Column(db.Integer, db.ForeignKey('tickets.id'), nullable=False)
    file_name = db.Column(db.String(255), nullable=False)
    file_path = db.Column(db.String(255), nullable=False)


class AuditLog(db.Model):
    __tablename__ = 'audit_logs'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    action = db.Column(db.String(255), nullable=False)
    metadata = db.Column(db.JSON)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
