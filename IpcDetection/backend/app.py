from flask import Flask, request, jsonify
import joblib
import pandas as pd
from flask_cors import CORS

# Load the model and vectorizer
model = joblib.load('model.pkl')
vectorizer = joblib.load('tfidf_vectorizer.pkl')
ipc_data = pd.read_csv('ipc_sections.csv')


app = Flask(__name__)
CORS(app)


@app.route('/predict', methods=['POST'])
def predict():
    data = request.json
    complaint = data.get('complaint', '')

    if not complaint:
        return jsonify({"error": "Complaint text is required"}), 400

    # Vectorize the complaint
    X_vector = vectorizer.transform([complaint])
    predicted_category = model.predict(X_vector)[0]

    # Find matching IPC details
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

if __name__ == '__main__':
    app.run(debug=True)
