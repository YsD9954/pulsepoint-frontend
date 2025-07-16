from flask import Flask, request, jsonify
import pandas as pd
import joblib
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Allow all origins

model = joblib.load('ml/team_risk_model.pkl')

@app.route('/')
def home():
    return jsonify({'message': 'PulsePoint Backend is live ✅'})

@app.route('/predict', methods=['POST'])
def predict():
    if 'csv_file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400

    try:
        df = pd.read_csv(request.files['csv_file'])
        for col in ['commits', 'messages', 'tickets_closed']:
            if col not in df.columns:
                return jsonify({'error': f'Missing column: {col}'}), 400

        if 'date' in df.columns:
            df['date'] = df['date'].astype(str)

        df['at_risk'] = model.predict(df[['commits', 'messages', 'tickets_closed']])
        return jsonify(df.to_dict(orient='records'))

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
