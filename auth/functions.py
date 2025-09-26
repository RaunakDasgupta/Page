from flask import request, jsonify
from flask_jwt_extended import create_access_token, create_refresh_token, get_jwt_identity

# Dummy user data
user_data = {
    "email":"test@example.com",
    "password": "password123"
}

def login_user():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"msg": "Missing email or password"}), 400

    if user_data["email"] != email or user_data["password"] != password:
        return jsonify({"msg": "Invalid email or password"}), 401

    # Generate tokens
    access_token = create_access_token(identity=email)
    refresh_token = create_refresh_token(identity=email)

    return jsonify({
        "access_token": access_token,
        "refresh_token": refresh_token
    }), 200

def refresh_token():
    identity = get_jwt_identity()
    new_access_token = create_access_token(identity=identity)
    return jsonify({"access_token": new_access_token}), 200

def protected_route():
    identity = get_jwt_identity()
    return jsonify({"msg": f"Hello, {identity}. This is a protected route."}), 200
