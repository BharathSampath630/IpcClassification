# IPC Crime Classification System

An AI-powered legal assistant that takes crime complaint text (or images) as input and classifies them into the relevant Indian Penal Code (IPC) section, returning the section code, legal description, and punishment.

## What It Does

- User enters a crime complaint as **text** or uploads an **image** of a complaint
- The image is processed using **Tesseract OCR** to extract text
- The text is classified into one of **5 IPC crime categories** using a trained ML model
- The system returns the **predicted crime**, **IPC section code**, **legal description**, **punishment**, and a **confidence score**
- Users can submit **feedback** (correct/incorrect) on predictions
- After enough feedback is collected (default: 10), the model **automatically retrains** itself using the corrected data
- An **admin dashboard** shows system stats like total complaints, model accuracy, pending feedback, and allows manual retraining

## Crime Categories Covered

1. Cheating and dishonestly inducing delivery of property (fraud, scams, phishing)
2. Criminal breach of trust (misappropriation of entrusted funds)
3. Theft by clerk or servant of property in possession of master or employer
4. Theft in a building, tent or vessel
5. Theft with preparation for causing death, hurt, or restraint

## ML Models Used

Three model tiers were built, each improving on the previous:

1. **Logistic Regression** — baseline model using TF-IDF vectorization
2. **Random Forest** — uses legal keyword feature injection per crime category with confidence boosting
3. **Voting Ensemble** — combines Random Forest, Gradient Boosting, SVM, and Logistic Regression with soft voting. Uses advanced features like fraud pattern detection (banking, online, investment scams), financial amount extraction, and weighted legal keyword scoring

## Tech Stack

- **Frontend**: React 18, Vite 5, CSS (glassmorphism design)
- **Backend**: Flask 3.0, Python
- **Database**: MongoDB
- **ML**: scikit-learn (TF-IDF, RandomForest, GradientBoosting, SVM, LogisticRegression, VotingClassifier)
- **OCR**: Tesseract (via pytesseract + Pillow)
- **NLP**: NLTK, regex-based pattern matching

## Project Structure

```
IpcClassification/IpcDetection/
├── backend/
│   ├── app.py                      # Flask API with /predict and /upload endpoints
│   ├── model_service.py            # Tier 1 - Logistic Regression
│   ├── enhanced_model_service.py   # Tier 2 - Random Forest + keywords
│   ├── advanced_model_service.py   # Tier 3 - Voting Ensemble
│   ├── database_service.py         # MongoDB operations
│   ├── database_setup.py           # DB initialization and CSV data migration
│   ├── check_retrain_status.py     # Check auto-retrain progress
│   ├── admin_dashboard.html        # Admin monitoring page
│   ├── xo.py                       # Standalone model training + evaluation script
│   ├── a.py                        # CLI prediction tester
│   ├── *.pkl                       # Serialized models and vectorizers
│   └── requirements.txt            # Python dependencies
├── dataset/
│   ├── breach_of_trust.csv
│   ├── fraud.csv
│   ├── theft1.csv, theft2.csv, theft3.csv
│   └── ipc_sections.csv            # IPC section reference data
└── frontend/
    └── src/
        ├── App.jsx                  # Main UI component
        └── index.css                # Glassmorphism styles
```
## Research Publication
This project was published as a research paper at the **IEEE ICDSAAI 2025 Conference**.
