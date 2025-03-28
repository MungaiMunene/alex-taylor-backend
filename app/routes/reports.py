from flask import Blueprint, jsonify, request
from app import db
from app.models import Report

reports_bp = Blueprint('reports', __name__, url_prefix='/reports')

@reports_bp.route('/', methods=['GET'])
def get_reports():
    reports = Report.query.all()
    return jsonify([{
        "id": r.id,
        "title": r.title,
        "content": r.content,
        "project_id": r.project_id
    } for r in reports])

@reports_bp.route('/<int:id>', methods=['GET'])
def get_report(id):
    r = Report.query.get_or_404(id)
    return jsonify({
        "id": r.id,
        "title": r.title,
        "content": r.content,
        "project_id": r.project_id
    })

@reports_bp.route('/', methods=['POST'])
def create_report():
    data = request.get_json()
    report = Report(
        title=data['title'],
        content=data.get('content'),
        project_id=data['project_id']
    )
    db.session.add(report)
    db.session.commit()
    return jsonify({"id": report.id}), 201

@reports_bp.route('/<int:id>', methods=['PUT'])
def update_report(id):
    report = Report.query.get_or_404(id)
    data = request.get_json()
    report.title = data.get('title', report.title)
    report.content = data.get('content', report.content)
    db.session.commit()
    return jsonify({"message": "Report updated"})

@reports_bp.route('/<int:id>', methods=['DELETE'])
def delete_report(id):
    report = Report.query.get_or_404(id)
    db.session.delete(report)
    db.session.commit()
    return jsonify({"message": "Report deleted"})