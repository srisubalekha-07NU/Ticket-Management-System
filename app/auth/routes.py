from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token

from app.extensions import db
from app.models.entities import User, Role


auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')


@auth_bp.post('/register')
def register():
    data = request.get_json() or {}
    role = Role.query.filter_by(name=data.get('role', 'Employee')).first()
    if not role:
        return jsonify({'error': 'Role not found'}), 400
    user = User(full_name=data['full_name'], email=data['email'], role=role)
    user.set_password(data['password'])
    db.session.add(user)
    db.session.commit()
    return jsonify({'message': 'User created'}), 201


@auth_bp.post('/login')
def login():
    data = request.get_json() or {}
    user = User.query.filter_by(email=data.get('email')).first()
    if not user or not user.check_password(data.get('password', '')):
        return jsonify({'error': 'Invalid credentials'}), 401
    token = create_access_token(identity=str(user.id), additional_claims={'role': user.role.name})
    return jsonify({'access_token': token, 'user': {'id': user.id, 'name': user.full_name, 'role': user.role.name}})
