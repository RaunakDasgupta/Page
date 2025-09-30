import pandas as pd
from flask import request, jsonify
from db.connection import get_db_connection

def upload_file():
    if 'file' not in request.files:
        return jsonify({"msg": "No file part"}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({"msg": "No selected file"}), 400
    if file:
        try:
            if file.filename.endswith('.csv'):
                df = pd.read_csv(file)
            elif file.filename.endswith(('.xls', '.xlsx')):
                df = pd.read_excel(file)
            else:
                return jsonify({"msg": "Unsupported file type"}), 400

            conn = get_db_connection()
            cur = conn.cursor()
            for index, row in df.iterrows():
                cur.execute(
                    "INSERT INTO user (name, email, department, position, salary) VALUES (%s, %s, %s, %s, %s)",
                    (row['name'], row['email'], row['department'], row['position'], row['salary'])
                )
            conn.commit()
            cur.close()
            conn.close()
            return jsonify({"msg": "File uploaded and data inserted successfully"}), 200
        except Exception as e:
            return jsonify({"msg": str(e)}), 500
