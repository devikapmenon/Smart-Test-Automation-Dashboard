from datetime import datetime
from app import db

class TestRun(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    run_id = db.Column(db.String(64), unique=True, nullable=False)
    test_suite = db.Column(db.String(100), default='Default Suite')
    status = db.Column(db.String(20), default='running')  # running/passed/failed
    start_time = db.Column(db.DateTime, default=datetime.utcnow)
    end_time = db.Column(db.DateTime)
    duration = db.Column(db.Float)  # in seconds
    total_tests = db.Column(db.Integer, default=0)
    passed_tests = db.Column(db.Integer, default=0)
    failed_tests = db.Column(db.Integer, default=0)
    
    def to_dict(self):
        return {
            'id': self.id,
            'run_id': self.run_id,
            'test_suite': self.test_suite,
            'status': self.status,
            'start_time': self.start_time.isoformat() if self.start_time else None,
            'end_time': self.end_time.isoformat() if self.end_time else None,
            'duration': self.duration,
            'total_tests': self.total_tests,
            'passed_tests': self.passed_tests,
            'failed_tests': self.failed_tests
        }

class TestCase(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    test_run_id = db.Column(db.Integer, db.ForeignKey('test_run.id'), nullable=False)
    name = db.Column(db.String(200), nullable=False)
    status = db.Column(db.String(20), nullable=False)
    duration = db.Column(db.Float)
    error_message = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'test_run_id': self.test_run_id,
            'name': self.name,
            'status': self.status,
            'duration': self.duration,
            'error_message': self.error_message,
            'timestamp': self.timestamp.isoformat() if self.timestamp else None
        }