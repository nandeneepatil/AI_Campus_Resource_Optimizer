import pandas as pd
from pathlib import Path

DATA_PATH = Path("data/raw/campus_resources.csv")


def analyze_resources():
    df = pd.read_csv(DATA_PATH)

    df["Utilization_%"] = (
        df["Students_Present"] / df["Room_Capacity"] * 100
    ).round(2)

    df["Electricity_Per_Student"] = (
        df["Electricity_kWh"] /
        df["Students_Present"].replace(0, 1)
    ).round(2)

    df["Status"] = "Efficient"

    df.loc[df["Utilization_%"] < 30, "Status"] = "Underutilized"
    df.loc[df["Utilization_%"] > 90, "Status"] = "Overcrowded"

    return df


if __name__ == "__main__":
    result = analyze_resources()

    print("\nAI Campus Resource Analysis")
    print("=" * 40)

    print(
        result[
            [
                "Building",
                "Room",
                "Utilization_%",
                "Electricity_kWh",
                "Status"
            ]
        ].to_string(index=False)
    )