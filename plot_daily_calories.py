import pandas as pd
import matplotlib.pyplot as plt

csv_path = "mfp_cleaned_output_with_weight.csv"
df = pd.read_csv(csv_path)
df["date"] = pd.to_datetime(df["date"], errors="coerce")

# Group by date and sum calories
daily = df.groupby("date")["calories"].sum().reset_index()

plt.figure(figsize=(10,5))
plt.plot(daily["date"], daily["calories"], marker="o")
plt.title("Daily Calorie Intake")
plt.xlabel("Date")
plt.ylabel("Calories")
plt.grid(True)
plt.tight_layout()
plt.savefig("visualizations/daily_calories.png")
plt.show()
