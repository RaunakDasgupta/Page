import os
from datetime import timedelta
from flask import Flask
from flask_jwt_extended import JWTManager, jwt_required
from dotenv import load_dotenv
from functions import login_user, refresh_token, protected_route

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

@app.route("/login", methods=["POST"])
def login():
    return login_user()

@app.route("/refresh", methods=["POST"])
@jwt_required(refresh=True)
def refresh():
    return refresh_token()

@app.route("/protected", methods=["GET"])
@jwt_required()
def protected():
    return protected_route()

if __name__ == "__main__":
    app.run(debug=True)
