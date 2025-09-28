import pandas as pd
import joblib

# Step 1: Load the trained model and vectorizer
model = joblib.load('model.pkl')
vectorizer = joblib.load('tfidf_vectorizer.pkl')

# Step 2: Load the IPC punishment CSV file
ipc_data = pd.read_csv(r"C:\Users\bhara\OneDrive\Documents\ipc\IpcDetection\backend\ipc_sections.csv")

# Step 3: Define a function to predict the crime category and retrieve IPC details
def get_ipc_details(complaint_text):
    # Vectorize the input complaint
    X_vector = vectorizer.transform([complaint_text])
    
    # Predict the category using the trained model
    predicted_category = model.predict(X_vector)[0]
    
    # Find the row in the ipc_data that matches the predicted offense
    matching_row = ipc_data[ipc_data['Offense'] == predicted_category]
    
    # If a match is found, print the IPC code, description, and punishment
    if not matching_row.empty:
        ipc_code = matching_row['Section'].values[0]
        punishment = matching_row['Punishment'].values[0]
        description = matching_row['Description'].values[0]
        
        print(f"Complaint: {complaint_text}")
        print()
        print(f"Predicted Crime: {predicted_category}")
        print()
        print(f"IPC Code: {ipc_code}")
        print()
        print(f"Description: {description}")
        print()
        print(f"Punishment: {punishment}")
    else:
        print(f"No IPC details found for the predicted crime: {predicted_category}")

# Step 4: Test the function with sample complaints
sample_complaints = [
    "I am writing to report a theft that occurred in our office building on the night of 12th September 2024. The thieves not only stole valuable equipment and documents but also prepared to cause severe harm to our staff if they were confronted. They were armed with weapons and threatened physical violence. The incident has caused significant distress and injury to one of our employees who is currently hospitalized. Immediate action is requested to apprehend the culprits and prevent further harm."
]

for complaint in sample_complaints:
    get_ipc_details(complaint)
    print("\n")
