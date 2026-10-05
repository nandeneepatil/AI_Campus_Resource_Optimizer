import pandas as pd


def generate_recommendations(df):
    recommendations = []

    for _, row in df.iterrows():

        if row["Utilization_%"] < 30:
            recommendations.append(
                f"{row['Room']}: Underutilized. "
                "Consider reallocating classes to this room."
            )

        elif row["Utilization_%"] > 90:
            recommendations.append(
                f"{row['Room']}: High utilization. "
                "Consider shifting some classes to another room."
            )

        elif row["Electricity_Per_Student"] > 1.5:
            recommendations.append(
                f"{row['Room']}: High electricity consumption per student. "
                "Consider checking energy usage."
            )

    return recommendations


if __name__ == "__main__":

    df = pd.read_csv("data/raw/campus_resources.csv")

    df["Utilization_%"] = (
        df["Students_Present"] /
        df["Room_Capacity"] * 100
    ).round(2)

    df["Electricity_Per_Student"] = (
        df["Electricity_kWh"] /
        df["Students_Present"].replace(0, 1)
    ).round(2)

    recommendations = generate_recommendations(df)

    print("\nAI Resource Recommendations")
    print("=" * 40)

    for recommendation in recommendations:
        print("•", recommendation)