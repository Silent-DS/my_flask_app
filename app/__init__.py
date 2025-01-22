from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# Initialize Flask app
app = Flask(__name__)
app.secret_key = "supersecretkey"  # Required for flash messages

# Configure the SQLite database
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Initialize SQLAlchemy
db = SQLAlchemy(app)

# Import models after initializing db to avoid circular imports
from app.models import MyTask

# Import routes after initializing app and db to avoid circular imports
from app import routes