from app import app, db

# Create the database tables
with app.app_context():
    db.create_all()

# Run the Flask app
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)