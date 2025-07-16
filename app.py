from flask import Flask, request, jsonify, render_template
import pandas as pd
import joblib
from flask_cors import CORS

app = Flask(__name__, static_folder='static')
CORS(app, supports_credentials=True, resources={r"/*": {"origins": "*"}}, methods=["GET", "POST", "OPTIONS"])
app.config['PROPAGATE_EXCEPTIONS'] = True

model = joblib.load('ml/team_risk_model.pkl')

@app.route('/')
def home():
    return render_template('index.html')

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

        X = df[['commits', 'messages', 'tickets_closed']]
        predictions = model.predict(X)
        df['at_risk'] = predictions

        result = df.to_dict(orient='records')
        return jsonify(result)

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
