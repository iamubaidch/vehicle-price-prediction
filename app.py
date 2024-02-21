from flask import Flask, render_template, request, jsonify, g
from flask_cors import CORS, cross_origin
import pandas as pd
import numpy as np
import joblib
from keras.models import load_model

app = Flask(__name__)
cors = CORS(app)

# Load the model and preprocessing pipeline
model = load_model('mlp_model.h5')
preprocessing_pipeline = joblib.load('preprocessing_pipeline.pkl')
df = pd.read_csv("cleaned_data.csv")


@app.route("/", methods=["GET", "POST"])
def index():
    companies = sorted(df["brand"].unique())
    car_models = sorted(df["vehicle"].unique())
    transmission_type = df["transmission"].unique()
    year = sorted(df["model_year"].unique(), reverse=True)
    fuel_type = df["engine_type"].unique()
    vehicle_color = sorted(df["color"].unique())
    registration_city = sorted(df["registered_in"].unique())

    return render_template(
        "index.html",
        companies=companies,
        car_models=car_models,
        transmission_type=transmission_type,
        years=year,
        fuel_types=fuel_type,
        vehicle_colors=vehicle_color,
        registration_cities=registration_city,
    )


@app.route("/get_car_models", methods=["GET"])
def get_car_models():
    selected_company = request.args.get("company")
    if selected_company not in df["brand"].unique():
        return jsonify([])
    filtered_models = df[df["brand"] == selected_company]["vehicle"].unique()
    return jsonify(filtered_models.tolist())

@app.route("/predict", methods=["POST"])
def predict():
    # Extract form data
    company = request.form.get("company")
    car_model = request.form.get("car_models")
    transmission_type = request.form.get("transmission_type")
    year = request.form.get("year")
    fuel_type = request.form.get("fuel_type")
    vehicle_color = request.form.get("vehicle_color")
    registration_city = request.form.get("registration_city")
    driven = request.form.get("kilo_driven")

    # Create a DataFrame from the input data
    input_data = pd.DataFrame(
        data=np.array([year, driven, registration_city, vehicle_color, company, car_model, transmission_type, fuel_type]).reshape(1, 8),
        columns=["model_year", "mileage", "registered_in", "color", "brand", "vehicle", "transmission", "engine_type"]
    )

    # Preprocess the input data
    input_data_prepared = preprocessing_pipeline.transform(input_data)
    input_data_prepared = input_data_prepared.toarray() if hasattr(input_data_prepared, "toarray") else input_data_prepared

    # Make prediction
    prediction = model.predict(input_data_prepared)

    predicted_price = round(float(prediction[0][0]), 2)
    return f"PKR {predicted_price} (Lakhs)"

if __name__ == "__main__":
    app.run(debug=True)
