from flask import Flask, request, render_template
from flask_cors import cross_origin
import pickle
import pandas as pd
import os

# 
app = Flask(__name__)

# Load model safely
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "flight_rf.pkl")
model = pickle.load(open(MODEL_PATH, "rb"))


@app.route("/")
@cross_origin()
def home():
    return render_template("home.html")


@app.route("/predict", methods=["POST"])
@cross_origin()
def predict():

    # Departure datetime
    date_dep = request.form["Dep_Time"]
    dep_time = pd.to_datetime(date_dep, format="%Y-%m-%dT%H:%M")

    journey_day = dep_time.day
    journey_month = dep_time.month
    dep_hour = dep_time.hour
    dep_min = dep_time.minute

    # Arrival datetime
    date_arr = request.form["Arrival_Time"]
    arr_time = pd.to_datetime(date_arr, format="%Y-%m-%dT%H:%M")

    arrival_hour = arr_time.hour
    arrival_min = arr_time.minute

    # Duration calculation (correct)
    duration = arr_time - dep_time
    duration_minutes = int(duration.total_seconds() / 60)
    Duration_hour = duration_minutes // 60
    Duration_mins = duration_minutes % 60

    # Stops
    Total_Stops = int(request.form["stops"])

    # Airline encoding
    airline = request.form["airline"]

    Airline_AirIndia = int(airline == "Air India")
    Airline_GoAir = int(airline == "GoAir")
    Airline_IndiGo = int(airline == "IndiGo")
    Airline_JetAirways = int(airline == "Jet Airways")
    Airline_MultipleCarriers = int(airline == "Multiple carriers")
    Airline_SpiceJet = int(airline == "SpiceJet")
    Airline_Vistara = int(airline == "Vistara")
    Airline_Other = int(airline not in [
        "Air India", "GoAir", "IndiGo", "Jet Airways",
        "Multiple carriers", "SpiceJet", "Vistara"
    ])

    # Source encoding
    source = request.form["Source"]
    Source_Delhi = int(source == "Delhi")
    Source_Kolkata = int(source == "Kolkata")
    Source_Mumbai = int(source == "Mumbai")
    Source_Chennai = int(source == "Chennai")

    # Destination encoding
    destination = request.form["Destination"]
    Destination_Cochin = int(destination == "Cochin")
    Destination_Delhi = int(destination == "Delhi")
    Destination_Hyderabad = int(destination == "Hyderabad")
    Destination_Kolkata = int(destination == "Kolkata")

    # Prediction
    prediction = model.predict([[
        Total_Stops,
        journey_day,
        journey_month,
        dep_hour,
        dep_min,
        arrival_hour,
        arrival_min,
        Duration_hour,
        Duration_mins,
        Airline_AirIndia,
        Airline_GoAir,
        Airline_IndiGo,
        Airline_JetAirways,
        Airline_MultipleCarriers,
        Airline_Other,
        Airline_SpiceJet,
        Airline_Vistara,
        Source_Chennai,
        Source_Kolkata,
        Source_Mumbai,
        # Destination_Cochin,
        Destination_Delhi,
        Destination_Hyderabad,
        Destination_Kolkata,
    ]])

    output = round(prediction[0], 2)

    return render_template(
        "home.html",
        prediction_text=f"Your Flight price is Rs. {output}"
    )


if __name__ == "__main__":
    app.run(debug=True)