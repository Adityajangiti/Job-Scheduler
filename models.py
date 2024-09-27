from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Job(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    job_name = db.Column(db.String(100), nullable=False)
    db_type = db.Column(db.String(50), nullable=False)
    server = db.Column(db.String(100), nullable=False)
    database_name = db.Column(db.String(100), nullable=False)
    username = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    queries = db.Column(db.Text, nullable=False)
    output_file = db.Column(db.String(100), nullable=False)
    email_ids = db.Column(db.String(200), nullable=False)
    frequency = db.Column(db.Integer, nullable=False)
    start_date = db.Column(db.DateTime, nullable=False)
    end_date = db.Column(db.DateTime, nullable=False)

    def __repr__(self):
        return f'<Job {self.job_name}>'
