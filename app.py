import os
from datetime import timedelta
from flask import Flask, request, jsonify
from flask_jwt_extended import (
    JWTManager, create_access_token, create_refresh_token,
    jwt_required, get_jwt_identity
)
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

# Pull configs from env
app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY", "fallback-secret")
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(
    seconds=int(os.getenv("JWT_ACCESS_TOKEN_EXPIRES", 900))  # default 15 min
)
app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(
    seconds=int(os.getenv("JWT_REFRESH_TOKEN_EXPIRES", 2592000))  # default 30 days
)

jwt = JWTManager(app)

# Dummy user data
user_data = {
    "email":"test@example.com",
    "password": "password123"
}


@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"msg": "Missing email or password"}), 400

    if user_data["email"]!= email or user_data["password"]!= password:
        return jsonify({"msg": "Invalid email or password"}), 401

    # Generate tokens
    access_token = create_access_token(identity=email)
    refresh_token = create_refresh_token(identity=email)

    return jsonify({
        "access_token": access_token,
        "refresh_token": refresh_token
    }), 200


@app.route("/refresh", methods=["POST"])
@jwt_required(refresh=True)
def refresh():
    identity = get_jwt_identity()
    new_access_token = create_access_token(identity=identity)
    return jsonify({"access_token": new_access_token}), 200


@app.route("/protected", methods=["GET"])
@jwt_required()
def protected():
    identity = get_jwt_identity()
    return jsonify({"msg": f"Hello, {identity}. This is a protected route."}), 200


if __name__ == "__main__":
    app.run(debug=True)
