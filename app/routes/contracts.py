# routes/contracts.py

from flask import Blueprint, request, jsonify
from app import db
from app.models import Contract  # Import the Contract model
from datetime import datetime  # 👈🏾 IMPORTANT: Import datetime

contracts_bp = Blueprint('contracts', __name__, url_prefix='/api/contracts')

@contracts_bp.route('/', methods=['POST'])
def create_contract():
    data = request.get_json()

    # 👇🏾 Parse start_date and end_date correctly into date objects
    start_date = datetime.strptime(data['start_date'], "%Y-%m-%d").date()
    end_date = datetime.strptime(data['end_date'], "%Y-%m-%d").date()

    new_contract = Contract(
        consultant_name=data['consultant_name'],
        consultant_contact=data['consultant_contact'],
        project_name=data['project_name'],
        project_description=data.get('project_description', ''),

        start_date=start_date,  # 👈🏾 USE the parsed date
        end_date=end_date,      # 👈🏾 USE the parsed date
        time_commitment_hours=data.get('time_commitment_hours'),

        deliverable_milestones=data.get('deliverable_milestones', ''),
        payment_rate=data.get('payment_rate', ''),
        payment_schedule=data.get('payment_schedule', ''),

        reporting_frequency=data.get('reporting_frequency', ''),
        reporting_format=data.get('reporting_format', ''),

        stakeholder_engagements=data.get('stakeholder_engagements', ''),
        stakeholder_reporting=data.get('stakeholder_reporting', ''),

        deliverable_ownership=data.get('deliverable_ownership', ''),
        knowledge_transfer_required=data.get('knowledge_transfer_required', True),

        confidentiality_terms=data.get('confidentiality_terms', ''),
        conflict_of_interest_required=data.get('conflict_of_interest_required', False),

        non_performance_penalties=data.get('non_performance_penalties', ''),
        termination_notice_days=data.get('termination_notice_days', 14),

        status='Active'
    )

    db.session.add(new_contract)
    db.session.commit()

    return jsonify(new_contract.serialize()), 201

@contracts_bp.route('/', methods=['GET'])
def get_contracts():
    contracts = Contract.query.all()
    return jsonify([c.serialize() for c in contracts])