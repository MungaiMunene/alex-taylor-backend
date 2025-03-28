from flask import Blueprint, jsonify, request
from app import db
from app.models import Client

clients_bp = Blueprint('clients', __name__, url_prefix='/clients')

@clients_bp.route('/', methods=['GET'])
def get_clients():
    clients = Client.query.all()
    return jsonify([{"id": c.id, "name": c.name, "sector": c.sector} for c in clients])

@clients_bp.route('/<int:id>', methods=['GET'])
def get_client(id):
    client = Client.query.get_or_404(id)
    return jsonify({"id": client.id, "name": client.name, "sector": client.sector})

@clients_bp.route('/', methods=['POST'])
def create_client():
    data = request.get_json()
    client = Client(name=data['name'], sector=data.get('sector'))
    db.session.add(client)
    db.session.commit()
    return jsonify({"id": client.id, "name": client.name, "sector": client.sector}), 201

@clients_bp.route('/<int:id>', methods=['PUT'])
def update_client(id):
    client = Client.query.get_or_404(id)
    data = request.get_json()
    client.name = data.get('name', client.name)
    client.sector = data.get('sector', client.sector)
    db.session.commit()
    return jsonify({"id": client.id, "name": client.name, "sector": client.sector})

@clients_bp.route('/<int:id>', methods=['DELETE'])
def delete_client(id):
    client = Client.query.get_or_404(id)
    db.session.delete(client)
    db.session.commit()
    return jsonify({"message": "Client deleted"})