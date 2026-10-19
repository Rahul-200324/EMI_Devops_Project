
from flask import Flask, render_template, request, jsonify, url_for
from config import Config
from extensions import db

# Initialize Flask application
app = Flask(__name__)
app.config.from_object(Config)

# Initialize database with Flask
db.init_app(app)

# Import models after app and db initialization.
# models.py must import db from extensions.py, NOT app.py.
from models import User


# -----------------------------------------
# Home / Login Page
# -----------------------------------------
@app.route("/")
@app.route("/login")
def login():
    return render_template("login.html")


# -----------------------------------------
# Signup Page
# -----------------------------------------
@app.route("/signup")
def signup():
    return render_template("signup.html")


# -----------------------------------------
# EMI Calculator Main Page
# -----------------------------------------
@app.route("/main")
def main():
    return render_template("main.html")


# -----------------------------------------
# Register User API
# -----------------------------------------
@app.route("/api/register", methods=["POST"])
def register_user():
    try:
        data = request.get_json(silent=True)

        if not data:
            return jsonify({
                "success": False,
                "message": "No valid JSON data received"
            }), 400

        name = str(data.get("name") or "").strip()
        email = str(data.get("email") or "").strip().lower()
        phone = str(data.get("phone") or "").strip()
        age_value = data.get("age")
        purpose = str(data.get("purpose") or "").strip()

        # Validate required fields
        if not name:
            return jsonify({
                "success": False,
                "message": "Name is required"
            }), 400

        if not email or "@" not in email:
            return jsonify({
                "success": False,
                "message": "Enter a valid email address"
            }), 400

        if len(phone) != 10 or not phone.isdigit():
            return jsonify({
                "success": False,
                "message": "Enter a valid 10-digit phone number"
            }), 400

        if age_value is None or str(age_value).strip() == "":
            return jsonify({
                "success": False,
                "message": "Age is required"
            }), 400

        try:
            age = int(age_value)
        except (ValueError, TypeError):
            return jsonify({
                "success": False,
                "message": "Age must be a valid whole number"
            }), 400

        if age < 18 or age > 100:
            return jsonify({
                "success": False,
                "message": "Age must be between 18 and 100"
            }), 400

        if not purpose:
            return jsonify({
                "success": False,
                "message": "Purpose is required"
            }), 400

        # Check whether the email is already registered
        existing_user = User.query.filter_by(email=email).first()

        if existing_user:
            return jsonify({
                "success": False,
                "message": "Email already registered"
            }), 409

        # Save user in database
        user = User(
            name=name,
            email=email,
            phone=phone,
            age=age,
            purpose=purpose
        )

        db.session.add(user)
        db.session.commit()

        return jsonify({
            "success": True,
            "message": "User registered successfully",
            "redirect": url_for("main")
        }), 201

    except Exception as e:
        db.session.rollback()
        app.logger.exception("Registration failed")

        return jsonify({
            "success": False,
            "message": "Something went wrong while saving user data"
        }), 500


# -----------------------------------------
# Get All Users (Testing / Admin)
# -----------------------------------------
@app.route("/api/users", methods=["GET"])
def get_users():
    try:
        users = User.query.order_by(User.created_at.desc()).all()

        user_list = []

        for user in users:
            user_list.append({
                "id": user.id,
                "name": user.name,
                "email": user.email,
                "phone": user.phone,
                "age": user.age,
                "purpose": user.purpose,
                "created_at": (
                    user.created_at.isoformat()
                    if user.created_at else None
                )
            })

        return jsonify({
            "success": True,
            "users": user_list
        }), 200

    except Exception:
        app.logger.exception("Unable to retrieve users")

        return jsonify({
            "success": False,
            "message": "Unable to retrieve users"
        }), 500


# -----------------------------------------
# Database Health Check
# -----------------------------------------
@app.route("/health", methods=["GET"])
def health():
    try:
        db.session.execute(db.text("SELECT 1"))

        return jsonify({
            "status": "healthy",
            "database": "connected"
        }), 200

    except Exception:
        db.session.rollback()
        app.logger.exception("Database health check failed")

        return jsonify({
            "status": "unhealthy",
            "database": "disconnected"
        }), 500


# -----------------------------------------
# Create Database Tables
# -----------------------------------------
with app.app_context():
    db.create_all()


# -----------------------------------------
# Run Application
# -----------------------------------------
if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5008,
        debug=True
    )
