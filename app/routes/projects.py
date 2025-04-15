# app/routes/projects.py

from flask import Blueprint, jsonify, request
from app import db
from app.models import Project
from datetime import datetime, date

projects_bp = Blueprint('projects', __name__, url_prefix='/api/projects')

# ✅ Create a new project
@projects_bp.route('/', methods=['POST'])
def create_project():
    data = request.get_json()

    if 'start_date' not in data or 'end_date' not in data:
        return jsonify({"error": "start_date and end_date are required"}), 400

    try:
        start_date = datetime.strptime(data['start_date'], "%Y-%m-%d").date()
        end_date = datetime.strptime(data['end_date'], "%Y-%m-%d").date()
    except ValueError:
        return jsonify({"error": "Invalid date format, expected YYYY-MM-DD"}), 400

    if not all(k in data for k in ('name', 'client_id', 'description')):
        return jsonify({"error": "Missing required fields: name, client_id, or description"}), 400

    project = Project(
        name=data['name'],
        client_id=data['client_id'],
        description=data['description'],
        start_date=start_date,
        end_date=end_date
    )
    
    db.session.add(project)
    db.session.commit()

    return jsonify({"id": project.id}), 201

# ✅ Get all projects
@projects_bp.route('/', methods=['GET'])
def get_projects():
    projects = Project.query.all()
    return jsonify([
        {
            "id": p.id,
            "name": p.name,
            "client_id": p.client_id,
            "description": p.description,
            "start_date": p.start_date.isoformat(),
            "end_date": p.end_date.isoformat()
        } for p in projects
    ]), 200

# ✅ Get a specific project by ID
@projects_bp.route('/<int:id>', methods=['GET'])
def get_project(id):
    project = Project.query.get_or_404(id)
    return jsonify({
        "id": project.id,
        "name": project.name,
        "client_id": project.client_id,
        "description": project.description,
        "start_date": project.start_date.isoformat(),
        "end_date": project.end_date.isoformat()
    }), 200

# ✅ Seed sample projects
@projects_bp.route('/seed', methods=['POST'])
def seed_projects():
    sample_projects = [
        Project(
            name='Alex Launch',
            description='Initial MVP rollout',
            client_id=1,
            start_date=date(2025, 4, 1),
            end_date=date(2025, 4, 30)
        ),
        Project(
            name='Metric Engine',
            description='Tracking & analytics core',
            client_id=1,
            start_date=date(2025, 5, 1),
            end_date=date(2025, 6, 30)
        )
    ]

    db.session.bulk_save_objects(sample_projects)
    db.session.commit()

    return jsonify({"message": "Sample projects seeded!"}), 201