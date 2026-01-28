from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from extractor import extract_from_file

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@app.route("/upload", methods=["POST"])
def upload_file():
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files["file"]
    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(file_path)

    extracted_data = extract_from_file(file_path)

    return jsonify(extracted_data)


if __name__ == "__main__":
    app.run(debug=True)
