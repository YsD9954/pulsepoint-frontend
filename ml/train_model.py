import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix
import joblib
import os

# Load merged data
df = pd.read_csv("data/github_commits.csv")
messages = pd.read_csv("data/messages.csv")
tickets = pd.read_csv("data/tickets.csv")

# Merge all 3 files
df = pd.merge(df, messages, on="date")
df = pd.merge(df, tickets, on="date")

# Label: 1 = At-Risk, 0 = Stable
df['at_risk'] = ((df['commits'] < 4) & (df['messages'] < 10)).astype(int)

# Features and Target
X = df[['commits', 'messages', 'tickets_closed']]
y = df['at_risk']

print("🔎 Final dataframe shape:", df.shape)
print(df.head())

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Evaluation
y_pred = model.predict(X_test)
print("✅ Confusion Matrix:\n", confusion_matrix(y_test, y_pred))
print("\n✅ Classification Report:\n", classification_report(y_test, y_pred))

# Save model
os.makedirs("ml", exist_ok=True)
joblib.dump(model, "ml/team_risk_model.pkl")
print("✅ Model saved as 'team_risk_model.pkl'")
