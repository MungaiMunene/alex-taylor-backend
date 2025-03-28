from flask import Blueprint, jsonify
from app.models import ProductivityDriver
from app import db

drivers_bp = Blueprint('drivers', __name__, url_prefix='/drivers')

@drivers_bp.route('/', methods=['GET'])
def get_all_drivers():
    drivers = ProductivityDriver.query.all()
    results = [{
        "id": d.id,
        "domain": d.domain,
        "theme": d.theme,
        "name": d.name,
        "unit": d.unit,
        "description": d.description
    } for d in drivers]

    return jsonify(results), 200