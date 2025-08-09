from flask import Flask, request, jsonify
from flasgger import Swagger
import joblib
import numpy as np

app = Flask(__name__)
swagger = Swagger(app)

# Load the trained model (make sure heart_disease_model.pkl is in the same folder)
model = joblib.load("heart_disease_model.pkl")

# Define the expected features and their order
FEATURES = [
    "age", "sex", "cp", "trestbps", "chol", "fbs", "restecg",
    "thalach", "exang", "oldpeak", "slope", "ca", "thal"
]

@app.route('/predict', methods=['POST'])
def predict():
    """
    Heart Disease Risk Prediction API
    ---
    tags:
      - Prediction
    parameters:
      - in: body
        name: patient_data
        required: true
        schema:
          type: object
          properties:
            age:
              type: number
              example: 54
            sex:
              type: integer
              example: 1
            cp:
              type: integer
              example: 0
            trestbps:
              type: number
              example: 130
            chol:
              type: number
              example: 250
            fbs:
              type: integer
              example: 0
            restecg:
              type: integer
              example: 1
            thalach:
              type: number
              example: 187
            exang:
              type: integer
              example: 0
            oldpeak:
              type: number
              example: 1.5
            slope:
              type: integer
              example: 2
            ca:
              type: integer
              example: 0
            thal:
              type: integer
              example: 2
          required:
            - age
            - sex
            - cp
            - trestbps
            - chol
            - fbs
            - restecg
            - thalach
            - exang
            - oldpeak
            - slope
            - ca
            - thal
    responses:
      200:
        description: Prediction results with risk and probability
        schema:
          type: object
          properties:
            heart_disease_risk:
              type: integer
              description: 0 (no risk) or 1 (risk)
            probability:
              type: number
              format: float
              description: Probability of the predicted class
            recommendation:
              type: string
              description: Medical recommendation based on risk
    """
    data = request.get_json(force=True)

    # Validate and extract features
    try:
        input_data = [data[feature] for feature in FEATURES]
    except KeyError as missing_feature:
        return jsonify({"error": f"Missing input parameter: {missing_feature}"}), 400

    # Convert input data to numpy array with type float32, handle conversion errors
    try:
        input_array = np.array(input_data, dtype=np.float32).reshape(1, -1)
    except ValueError as e:
        return jsonify({"error": f"Invalid input types: {str(e)}"}), 400

    # Predict class and probability
    try:
        prediction = model.predict(input_array)[0]
        probability = model.predict_proba(input_array)[0][prediction]
    except Exception as e:
        return jsonify({"error": f"Prediction error: {str(e)}"}), 500

    recommendation = (
        "Low risk of heart disease."
        if prediction == 0
        else "High risk of heart disease. Immediate medical consultation recommended."
    )

    return jsonify(
        heart_disease_risk=int(prediction),
        probability=round(float(probability), 4),
        recommendation=recommendation,
    )


if __name__ == "__main__":
    app.run(debug=True)
