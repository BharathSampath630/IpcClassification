import pytesseract
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

from flask import Flask, request, jsonify
import joblib
import pandas as pd
from flask_cors import CORS
from PIL import Image
import pytesseract
import os

# ------------------------------
# Load model, vectorizer, IPC data
# ------------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
model = joblib.load(os.path.join(BASE_DIR, 'model.pkl'))
vectorizer = joblib.load(os.path.join(BASE_DIR, 'tfidf_vectorizer.pkl'))
ipc_data = pd.read_csv(os.path.join(BASE_DIR, 'ipc_sections.csv'))

# ------------------------------
# Flask setup
# ------------------------------
app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = os.path.join(BASE_DIR, "uploads")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# ------------------------------
# Text input endpoint
# ------------------------------
@app.route('/predict', methods=['POST'])
def predict_text():
    data = request.json
    complaint = data.get('complaint', '')

    if not complaint:
        return jsonify({"error": "Complaint text is required"}), 400

    # Vectorize and predict
    X_vector = vectorizer.transform([complaint])
    predicted_category = model.predict(X_vector)[0]

    # Find IPC details
    matching_row = ipc_data[ipc_data['Offense'] == predicted_category]
    if not matching_row.empty:
        result = {
            "crime": predicted_category,
            "ipc_code": matching_row['Section'].values[0],
            "description": matching_row['Description'].values[0],
            "punishment": matching_row['Punishment'].values[0]
        }
    else:
        result = {
            "crime": predicted_category,
            "ipc_code": "N/A",
            "description": "No details available",
            "punishment": "N/A"
        }

    return jsonify(result)

# ------------------------------
# Image upload endpoint
# ------------------------------
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'image' not in request.files:
        return jsonify({"error": "No file part"}), 400
    
    file = request.files['image']
    if file.filename == "":
        return jsonify({"error": "No selected file"}), 400
    
    # Save uploaded file
    filepath = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(filepath)
    
    # Extract text using OCR
    img = Image.open(filepath)
    complaint_text = pytesseract.image_to_string(img)
    
    # Predict using same logic
    X_vector = vectorizer.transform([complaint_text])
    predicted_category = model.predict(X_vector)[0]

    matching_row = ipc_data[ipc_data['Offense'] == predicted_category]
    if not matching_row.empty:
        result = {
            "crime": predicted_category,
            "ipc_code": matching_row['Section'].values[0],
            "description": matching_row['Description'].values[0],
            "punishment": matching_row['Punishment'].values[0]
        }
    else:
        result = {
            "crime": predicted_category,
            "ipc_code": "N/A",
            "description": "No details available",
            "punishment": "N/A"
        }

    return jsonify({"text": complaint_text, "prediction": result})

# ------------------------------
# Run server
# ------------------------------
if __name__ == '__main__':
    app.run(debug=True, port=5000)
