import joblib

model = joblib.load("flight_rf.pkl")

print(type(model))
