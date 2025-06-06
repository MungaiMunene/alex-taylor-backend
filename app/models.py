# app/models.py

from datetime import datetime
from app import db  # ✅ Important: use db from app/__init__.py

# --- Association Table for Many-to-Many between Contracts and Drivers ---
contract_driver_link = db.Table('contract_driver_link',
    db.Column('contract_id', db.Integer, db.ForeignKey('contracts.id'), primary_key=True),
    db.Column('driver_id', db.Integer, db.ForeignKey('productivity_driver.id'), primary_key=True)
)

# --- Client Model ---
class Client(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    sector = db.Column(db.String(120))
    projects = db.relationship('Project', backref='client', lazy=True)

# --- Project Model ---
class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    client_id = db.Column(db.Integer, db.ForeignKey('client.id'), nullable=False)
    description = db.Column(db.Text)
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)

    metrics = db.relationship('Metric', backref='project', lazy=True)
    reports = db.relationship('Report', backref='project', lazy=True)

# --- Metric Model ---
class Metric(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    category = db.Column(db.String(120))  # e.g., productivity / impact
    value = db.Column(db.Float)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    driver_id = db.Column(
        db.Integer,
        db.ForeignKey('productivity_driver.id', name='fk_metric_driver_id')
    )

# --- Report Model ---
class Report(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    content = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'), nullable=False)

# --- ProductivityDriver Model ---
class ProductivityDriver(db.Model):
    __tablename__ = 'productivity_driver'

    id = db.Column(db.Integer, primary_key=True)
    domain = db.Column(db.String(120), nullable=False)
    theme = db.Column(db.String(120), nullable=False)
    name = db.Column(db.String(200), nullable=False)
    unit = db.Column(db.String(50))
    description = db.Column(db.Text)

    def __repr__(self):
        return f"<Driver {self.name}>"

# --- Contract Model ---
class Contract(db.Model):
    __tablename__ = 'contracts'

    id = db.Column(db.Integer, primary_key=True)

    consultant_name = db.Column(db.String(100), nullable=False)
    consultant_contact = db.Column(db.String(150), nullable=False)
    project_name = db.Column(db.String(150), nullable=False)
    project_description = db.Column(db.Text, nullable=True)

    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    time_commitment_hours = db.Column(db.Integer)
    deliverable_milestones = db.Column(db.Text)

    payment_rate = db.Column(db.String(100))
    payment_schedule = db.Column(db.String(100))

    reporting_frequency = db.Column(db.String(50))
    reporting_format = db.Column(db.String(50))

    stakeholder_engagements = db.Column(db.String(200))
    stakeholder_reporting = db.Column(db.String(200))

    deliverable_ownership = db.Column(db.String(200))
    knowledge_transfer_required = db.Column(db.Boolean, default=True)

    confidentiality_terms = db.Column(db.Text)
    conflict_of_interest_required = db.Column(db.Boolean, default=False)

    non_performance_penalties = db.Column(db.String(200))
    termination_notice_days = db.Column(db.Integer, default=14)

    status = db.Column(db.String(20), default='Active')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    drivers = db.relationship('ProductivityDriver', secondary=contract_driver_link, backref='contracts')

    def serialize(self):
        return {
            "id": self.id,
            "consultant_name": self.consultant_name,
            "consultant_contact": self.consultant_contact,
            "project_name": self.project_name,
            "project_description": self.project_description,
            "start_date": str(self.start_date),
            "end_date": str(self.end_date),
            "time_commitment_hours": self.time_commitment_hours,
            "deliverable_milestones": self.deliverable_milestones,
            "payment_rate": self.payment_rate,
            "payment_schedule": self.payment_schedule,
            "reporting_frequency": self.reporting_frequency,
            "reporting_format": self.reporting_format,
            "stakeholder_engagements": self.stakeholder_engagements,
            "stakeholder_reporting": self.stakeholder_reporting,
            "deliverable_ownership": self.deliverable_ownership,
            "knowledge_transfer_required": self.knowledge_transfer_required,
            "confidentiality_terms": self.confidentiality_terms,
            "conflict_of_interest_required": self.conflict_of_interest_required,
            "non_performance_penalties": self.non_performance_penalties,
            "termination_notice_days": self.termination_notice_days,
            "status": self.status,
            "created_at": str(self.created_at)
        }

# --- Updated User Model ---
class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    role = db.Column(db.String(50), default="Admin")

    honors = db.Column(db.String(250))
    life_areas = db.Column(db.Text)
    life_priorities_2025 = db.Column(db.Text)
    life_priorities_2030 = db.Column(db.Text)
    preferred_interaction_style = db.Column(db.Text)
    daily_rhythm = db.Column(db.Text)
    long_term_integration = db.Column(db.Text)
    dynamic_growth_allowed = db.Column(db.Boolean, default=True)

    status = db.Column(db.String(20), default="Active")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "role": self.role,
            "honors": self.honors,
            "life_areas": self.life_areas,
            "life_priorities_2025": self.life_priorities_2025,
            "life_priorities_2030": self.life_priorities_2030,
            "preferred_interaction_style": self.preferred_interaction_style,
            "daily_rhythm": self.daily_rhythm,
            "long_term_integration": self.long_term_integration,
            "dynamic_growth_allowed": self.dynamic_growth_allowed,
            "status": self.status,
            "created_at": str(self.created_at)
        }