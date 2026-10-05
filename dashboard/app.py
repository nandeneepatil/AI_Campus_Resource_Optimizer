import streamlit as st
import pandas as pd
import sys
from pathlib import Path

# Allow imports from project root
sys.path.append(str(Path(__file__).resolve().parent.parent))

from models.demand_predictor import predict_electricity
from agents.resource_analyzer import analyze_resources
from agents.recommendation_agent import generate_recommendations


# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="AI Campus Resource Optimizer",
    page_icon="🏫",
    layout="wide"
)

st.title("🏫 AI Campus Resource Optimizer")
st.write(
    "AI-powered campus resource utilization, prediction "
    "and intelligent recommendations."
)


# --------------------------------------------------
# LOAD DATA
# --------------------------------------------------

df = pd.read_csv("data/raw/campus_resources.csv")


# --------------------------------------------------
# RESOURCE ANALYSIS
# --------------------------------------------------

df["Utilization_%"] = (
    df["Students_Present"] /
    df["Room_Capacity"] * 100
).round(2)

df["Electricity_Per_Student"] = (
    df["Electricity_kWh"] /
    df["Students_Present"].replace(0, 1)
).round(2)

df["Status"] = "Efficient"

df.loc[
    df["Utilization_%"] < 30,
    "Status"
] = "Underutilized"

df.loc[
    df["Utilization_%"] > 90,
    "Status"
] = "Overcrowded"


# --------------------------------------------------
# KEY METRICS
# --------------------------------------------------

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Total Records",
    len(df)
)

col2.metric(
    "Average Utilization",
    f"{df['Utilization_%'].mean():.1f}%"
)

col3.metric(
    "Underutilized",
    (df["Status"] == "Underutilized").sum()
)

col4.metric(
    "Overcrowded",
    (df["Status"] == "Overcrowded").sum()
)


st.divider()


# --------------------------------------------------
# ROOM UTILIZATION
# --------------------------------------------------

st.subheader("📊 Room Utilization")

room_usage = (
    df.groupby("Room")["Utilization_%"]
    .mean()
    .sort_values(ascending=False)
)

st.bar_chart(room_usage)


# --------------------------------------------------
# RESOURCE CONSUMPTION
# --------------------------------------------------

st.subheader("⚡ Resource Consumption")

resource_data = df.groupby("Room")[
    ["Electricity_kWh", "Water_Liters"]
].mean()

st.bar_chart(resource_data)


# --------------------------------------------------
# AI ELECTRICITY PREDICTION
# --------------------------------------------------

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


if st.button("🔮 Predict Electricity Usage"):

    prediction = predict_electricity(
        students,
        hours,
        classes,
        capacity
    )

    st.success(
        f"🔋 Predicted Electricity Usage: {prediction} kWh"
    )


# --------------------------------------------------
# AI RECOMMENDATIONS
# --------------------------------------------------

st.subheader("💡 AI Recommendations")

analysis_df = analyze_resources()

recommendations = generate_recommendations(
    analysis_df
)

if recommendations:

    for recommendation in recommendations:
        st.info(
            f"🤖 {recommendation}"
        )

else:

    st.success(
        "✅ No major resource issues detected."
    )


# --------------------------------------------------
# RESOURCE STATUS TABLE
# --------------------------------------------------

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


# --------------------------------------------------
# SUMMARY
# --------------------------------------------------

st.subheader("📌 Campus Resource Summary")

total_electricity = df["Electricity_kWh"].sum()
total_water = df["Water_Liters"].sum()
average_utilization = df["Utilization_%"].mean()

s1, s2, s3 = st.columns(3)

s1.metric(
    "Total Electricity",
    f"{total_electricity:.0f} kWh"
)

s2.metric(
    "Total Water",
    f"{total_water:.0f} L"
)

s3.metric(
    "Average Utilization",
    f"{average_utilization:.1f}%"
)


st.divider()

st.success(
    "✅ AI Campus Resource Analysis Completed Successfully"
)