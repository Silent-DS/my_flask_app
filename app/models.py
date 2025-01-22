from datetime import datetime, UTC
from app import db  # Import db from the app package

class MyTask(db.Model):
    __tablename__ = "my_task"  # Explicitly set the table name
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(100), nullable=False)
    created = db.Column(db.DateTime, default=lambda: datetime.now(UTC))  # Use timezone-aware datetime
    complete = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f"Task {self.id}"