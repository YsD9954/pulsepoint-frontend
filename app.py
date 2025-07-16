from flask import Flask, request, jsonify
import pandas as pd
import joblib
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Load model once
model = joblib.load('ml/team_risk_model.pkl')

@app.route('/')
def home():
    return jsonify({'message': 'PulsePoint Backend is live ✅'}), 200

@app.route('/predict', methods=['POST'])
def predict():
    try:
        if 'csv_file' not in request.files:
            return jsonify({'error': 'No file uploaded'}), 400

        file = request.files['csv_file']
        df = pd.read_csv(file)

        required_cols = ['commits', 'messages', 'tickets_closed']
        for col in required_cols:
            if col not in df.columns:
                return jsonify({'error': f'Missing column: {col}'}), 400

        if 'date' in df.columns:
            df['date'] = df['date'].astype(str)

        X = df[required_cols]
        df['at_risk'] = model.predict(X)

        return jsonify(df.to_dict(orient='records'))

    except Exception as e:
        print("🔥 Server error:", str(e))
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
