import streamlit as st
import pandas as pd
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

from models.demand_predictor import predict_electricity

st.set_page_config(
    page_title="AI Campus Resource Optimizer",
    page_icon="🏫",
    layout="wide"
)

st.title("🏫 AI Campus Resource Optimizer")
st.write("AI-powered campus resource utilization and efficiency analysis.")

# Load data
df = pd.read_csv("data/raw/campus_resources.csv")

# Calculate utilization
df["Utilization_%"] = (
    df["Students_Present"] / df["Room_Capacity"] * 100
).round(2)

# Classify rooms
df["Status"] = "Efficient"
df.loc[df["Utilization_%"] < 30, "Status"] = "Underutilized"
df.loc[df["Utilization_%"] > 90, "Status"] = "Overcrowded"

# KPIs
col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Records", len(df))
col2.metric("Average Utilization", f"{df['Utilization_%'].mean():.1f}%")
col3.metric("Underutilized", (df["Status"] == "Underutilized").sum())
col4.metric("Overcrowded", (df["Status"] == "Overcrowded").sum())

st.divider()

# Room utilization
st.subheader("📊 Room Utilization")

room_usage = (
    df.groupby("Room")["Utilization_%"]
    .mean()
    .sort_values(ascending=False)
)

st.bar_chart(room_usage)

# ML Prediction
st.subheader("🤖 AI Electricity Prediction")

c1, c2 = st.columns(2)

with c1:
    students = st.number_input(
        "Students Present",
        min_value=1,
        value=50
    )

    hours = st.number_input(
        "Hours Used",
        min_value=1,
        value=6
    )

with c2:
    classes = st.number_input(
        "Classes Scheduled",
        min_value=1,
        value=4
    )

    capacity = st.number_input(
        "Room Capacity",
        min_value=1,
        value=60
    )

if st.button("Predict Electricity Usage"):
    prediction = predict_electricity(
        students,
        hours,
        classes,
        capacity
    )

    st.success(
        f"🔋 Predicted Electricity Usage: {prediction} kWh"
    )

# Resource status
st.subheader("⚠️ Resource Status")

st.dataframe(
    df[
        [
            "Date",
            "Building",
            "Room",
            "Room_Capacity",
            "Students_Present",
            "Utilization_%",
            "Electricity_kWh",
            "Water_Liters",
            "Status"
        ]
    ],
    width="stretch"
)

# Recommendations
st.subheader("💡 AI Recommendations")

underused = df[df["Status"] == "Underutilized"]
overcrowded = df[df["Status"] == "Overcrowded"]

if not underused.empty:
    st.warning(
        f"{len(underused)} records show low utilization. "
        "Consider reallocating classes to these rooms."
    )

if not overcrowded.empty:
    st.error(
        f"{len(overcrowded)} records show high utilization. "
        "Consider moving some classes to available rooms."
    )

st.success("Resource analysis completed successfully.")