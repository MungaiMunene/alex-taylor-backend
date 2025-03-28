from datetime import datetime
from app import db  # this line is key!

class Client(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    sector = db.Column(db.String(120))
    projects = db.relationship('Project', backref='client', lazy=True)

class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    client_id = db.Column(db.Integer, db.ForeignKey('client.id'), nullable=False)
    description = db.Column(db.Text)
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)

    # Relationships
    metrics = db.relationship('Metric', backref='project', lazy=True)
    reports = db.relationship('Report', backref='project', lazy=True)

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
    )  # Optional link to productivity driver

class Report(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    content = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'), nullable=False)

class ProductivityDriver(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    domain = db.Column(db.String(120), nullable=False)
    theme = db.Column(db.String(120), nullable=False)
    name = db.Column(db.String(200), nullable=False)
    unit = db.Column(db.String(50))
    description = db.Column(db.Text)

    def __repr__(self):
        return f"<Driver {self.name}>"
