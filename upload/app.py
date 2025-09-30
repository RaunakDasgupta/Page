import os
from flask import Flask, request
from dotenv import load_dotenv
from functions import upload_file

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

@app.route("/upload", methods=["POST"])
def upload():
    return upload_file()
    

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5002)
