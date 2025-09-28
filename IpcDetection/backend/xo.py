
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, confusion_matrix
import seaborn as sns
import matplotlib.pyplot as plt

# Step 1: Load each CSV file
df_theft_death_or_hurt = pd.read_csv(r"theft1.csv")
df_theft_by_clerk = pd.read_csv(r"theft2.csv")
df_theft_in_building = pd.read_csv(r"theft3.csv")

# Step 2: Add a new column for the category
df_theft_death_or_hurt['Category'] = 'Theft, after preparation having been made for causing death, or hurt, or restraint or fear of death, or of hurt or of restraint, in order to the committing of such theft, or to retiring after committing it, or to retaining property taken by it'
df_theft_by_clerk['Category'] = 'Theft by clerk or servant of property in possession of master or employer'
df_theft_in_building['Category'] = 'Theft in a building, tent or vessel'

# Step 3: Combine all DataFrames
df_combined = pd.concat([df_theft_death_or_hurt, df_theft_by_clerk, df_theft_in_building])

# Step 4: Shuffle the DataFrame to mix up the order of complaints
df_combined = df_combined.sample(frac=1, random_state=42).reset_index(drop=True)

# Step 5: Save the combined DataFrame to a new CSV file (optional)
df_combined.to_csv('combined_complaints.csv', index=False)

# Step 6: Preprocess the data
X = df_combined['Complaint_Text']
y = df_combined['Category']

# Step 7: Vectorize the text
vectorizer = TfidfVectorizer(stop_words='english')
X_vectors = vectorizer.fit_transform(X)

# Step 8: Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X_vectors, y, test_size=0.2, random_state=42)

# Step 9: Train the model
model = LogisticRegression(max_iter=1000)
model.fit(X_train, y_train)

# Step 10: Predict and evaluate
y_pred = model.predict(X_test)
print(classification_report(y_test, y_pred))

# Confusion Matrix
conf_matrix = confusion_matrix(y_test, y_pred)

# Step 11: Plot confusion matrix using seaborn
plt.figure(figsize=(10, 7))
sns.heatmap(conf_matrix, annot=True, fmt='d', cmap='Blues', xticklabels=model.classes_, yticklabels=model.classes_)
plt.xlabel('Predicted')
plt.ylabel('True')
plt.title('Confusion Matrix')
plt.show()

# Plotting classification metrics
report = classification_report(y_test, y_pred, output_dict=True)
metrics_df = pd.DataFrame(report).transpose()

# Step 12: Plot bar chart of classification report metrics
metrics_df[['precision', 'recall', 'f1-score']].iloc[:-1].plot(kind='bar', figsize=(10, 6))
plt.title('Classification Report Metrics by Category')
plt.ylabel('Score')
plt.xlabel('Category')
plt.xticks(rotation=45, ha='right')
plt.legend(loc='lower right')
plt.tight_layout()
plt.show()

# Step 13: Save the trained model and vectorizer
import joblib
joblib.dump(model, 'model.pkl')
joblib.dump(vectorizer, 'tfidf_vectorizer.pkl')



