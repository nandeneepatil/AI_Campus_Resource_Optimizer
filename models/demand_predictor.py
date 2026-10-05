import pandas as pd
from sklearn.ensemble import RandomForestRegressor

# Load dataset
df = pd.read_csv("data/raw/campus_resources.csv")

# Features
features = [
    "Students_Present",
    "Hours_Used",
    "Classes_Scheduled",
    "Room_Capacity"
]

X = df[features]

# Target
y = df["Electricity_kWh"]

# Train Random Forest model
model = RandomForestRegressor(
    n_estimators=100,
    random_state=42
)

model.fit(X, y)


def predict_electricity(
    students,
    hours,
    classes,
    capacity
):
    # Create input with the same feature names used during training
    input_data = pd.DataFrame(
        [[students, hours, classes, capacity]],
        columns=features
    )

    prediction = model.predict(input_data)

    return round(prediction[0], 2)


# Test prediction
if __name__ == "__main__":
    result = predict_electricity(
        students=50,
        hours=6,
        classes=4,
        capacity=60
    )

    print("Predicted Electricity Usage:", result, "kWh")
