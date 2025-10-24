from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib
import pandas as pd
import os

app = Flask(__name__)
CORS(app)  # ✅ allow requests from your React frontend

# ---------- Load Models ----------
try:
    meal_model = joblib.load("fitness_meal_model.pkl")
    workout_model = joblib.load("fitness_workout_model.pkl")
    yoga_model = joblib.load("yoga_model.pkl")
    interaction_model = joblib.load("interaction_model.pkl")
except Exception as e:
    print("⚠️ Model loading error:", e)



# ---------- Default Route ----------
@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "message": "✅ AI Health Assistant API Running",
        "routes": {
            "/predict_plan": "POST - Meal & Workout Plan",
            "/predict_yoga": "POST - Yoga & Meditation Plan",
            "/predict_interaction": "POST - Food–Medicine Interaction"
        }
    })


# ---------- Meal & Workout Suggestion ----------
@app.route("/predict_plan", methods=["POST"])
def predict_plan():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No input data"}), 400

        df = pd.DataFrame([data])
        df_encoded = pd.get_dummies(df)

        for col in meal_model.feature_names_in_:
            if col not in df_encoded.columns:
                df_encoded[col] = 0
        df_encoded = df_encoded[meal_model.feature_names_in_]

        meal_pred = meal_model.predict(df_encoded)[0]
        workout_pred = workout_model.predict(df_encoded)[0]

        return jsonify({
            "meal_suggestion": str(meal_pred),
            "workout_suggestion": str(workout_pred)
        })
    except Exception as e:
        return jsonify({"error": f"Prediction failed: {str(e)}"}), 500


# ---------- Yoga & Meditation Suggestion ----------
@app.route("/predict_yoga", methods=["POST"])
def predict_yoga():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No input data"}), 400

        df = pd.DataFrame([data])
        df_encoded = pd.get_dummies(df)

        for col in yoga_model.feature_names_in_:
            if col not in df_encoded.columns:
                df_encoded[col] = 0
        df_encoded = df_encoded[yoga_model.feature_names_in_]

        yoga_pred = yoga_model.predict(df_encoded)[0]
        return jsonify({"yoga_suggestion": str(yoga_pred)})
    except Exception as e:
        return jsonify({"error": f"Prediction failed: {str(e)}"}), 500


# ---------- Food–Medicine Interaction ----------
@app.route("/predict_interaction", methods=["POST"])
def predict_interaction():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No input data"}), 400

        df = pd.DataFrame([data])
        df_encoded = pd.get_dummies(df)

        for col in interaction_model.feature_names_in_:
            if col not in df_encoded.columns:
                df_encoded[col] = 0
        df_encoded = df_encoded[interaction_model.feature_names_in_]

        result = interaction_model.predict(df_encoded)[0]
        return jsonify({"interaction_result": str(result)})
    except Exception as e:
        return jsonify({"error": f"Prediction failed: {str(e)}"}), 500


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5001, debug=True)
