from flask import Flask, render_template, request, jsonify
from flask_cors import CORS, cross_origin
import pickle
import pandas as pd
import numpy as np
import os

app = Flask(__name__)
cors = CORS(app)
with open("RandomForestRegressorModel.pkl", "rb") as file:
    model = pickle.load(file, protocol=pickle.HIGHEST_PROTOCOL)

df = pd.read_csv("New_cleaned_data.csv")


@app.route("/", methods=["GET", "POST"])
def index():
    companies = sorted(df["brand"].unique())
    car_models = sorted(df["vehicle"].unique())
    transmission_type = df["transmission"].unique()
    year = sorted(df["model_year"].unique(), reverse=True)
    fuel_type = df["engine_type"].unique()
    vehicle_color = sorted(df["color"].unique())
    registrarion_city = sorted(df["registered_in"].unique())

    return render_template(
        "index.html",
        companies=companies,
        car_models=car_models,
        transmission_type=transmission_type,
        years=year,
        fuel_types=fuel_type,
        vehicle_colors=vehicle_color,
        registration_cities=registrarion_city,
    )


@app.route("/get_car_models", methods=["GET"])
@cross_origin()
def get_car_models():
    selected_company = request.args.get("company")

    # Add a print statement for debugging
    print("Selected Company:", selected_company)

    # Check if the selected company exists in the DataFrame
    if selected_company not in df["brand"].unique():
        print("Error: Selected company not found.")
        return jsonify([])

    # Filter car models based on the selected company
    filtered_models = df[df["brand"] == selected_company]["vehicle"].unique()

    return jsonify(filtered_models.tolist())


@app.route("/predict", methods=["POST"])
@cross_origin()
def predict():
    company = request.form.get("company")
    car_model = request.form.get("car_models")
    transmission_type = request.form.get("transmission_type")
    year = request.form.get("year")
    fuel_type = request.form.get("fuel_type")
    vehicle_color = request.form.get("vehicle_color")
    registration_city = request.form.get("registration_city")
    driven = request.form.get("kilo_driven")

    prediction = model.predict(
        pd.DataFrame(
            columns=[
                "model_year",
                "mileage",
                "registered_in",
                "color",
                "brand",
                "vehicle",
                "transmission",
                "engine_type",
            ],
            data=np.array(
                [
                    year,
                    driven,
                    registration_city,
                    vehicle_color,
                    company,
                    car_model,
                    transmission_type,
                    fuel_type,
                ]
            ).reshape(1, 8),
        )
    )

    print(prediction)

    return str(np.round(prediction[0], 2))


if __name__ == "__main__":
    app.run(debug=True)
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
