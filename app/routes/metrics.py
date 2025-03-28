from flask import Blueprint, jsonify, request
from app import db
from app.models import Metric

metrics_bp = Blueprint('metrics', __name__, url_prefix='/metrics')


@metrics_bp.route('/', methods=['GET'])
def get_metrics():
    query = Metric.query

    # Apply optional filters from query params
    driver_id = request.args.get('driver_id')
    project_id = request.args.get('project_id')

    if driver_id:
        query = query.filter_by(driver_id=driver_id)
    if project_id:
        query = query.filter_by(project_id=project_id)

    metrics = query.all()
    return jsonify([{
        "id": m.id,
        "name": m.name,
        "category": m.category,
        "value": m.value,
        "project_id": m.project_id,
        "driver_id": m.driver_id,
        "timestamp": m.timestamp.isoformat()
    } for m in metrics])


@metrics_bp.route('/<int:id>', methods=['GET'])
def get_metric(id):
    m = Metric.query.get_or_404(id)
    return jsonify({
        "id": m.id,
        "name": m.name,
        "category": m.category,
        "value": m.value,
        "project_id": m.project_id,
        "driver_id": m.driver_id,
        "timestamp": m.timestamp.isoformat()
    })


@metrics_bp.route('/', methods=['POST'])
def create_metric():
    data = request.get_json()
    metric = Metric(
        name=data['name'],
        category=data.get('category'),
        value=data['value'],
        project_id=data['project_id'],
        driver_id=data.get('driver_id')
    )
    db.session.add(metric)
    db.session.commit()
    return jsonify({"id": metric.id}), 201


@metrics_bp.route('/<int:id>', methods=['PUT'])
def update_metric(id):
    metric = Metric.query.get_or_404(id)
    data = request.get_json()
    metric.name = data.get('name', metric.name)
    metric.category = data.get('category', metric.category)
    metric.value = data.get('value', metric.value)
    metric.driver_id = data.get('driver_id', metric.driver_id)
    db.session.commit()
    return jsonify({"message": "Metric updated"})


@metrics_bp.route('/<int:id>', methods=['DELETE'])
def delete_metric(id):
    metric = Metric.query.get_or_404(id)
    db.session.delete(metric)
    db.session.commit()
    return jsonify({"message": "Metric deleted"})