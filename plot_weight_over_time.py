import pandas as pd
import matplotlib.pyplot as plt

# Load data
csv_path = "data/mfp_cleaned_output_with_weight.csv"
df = pd.read_csv(csv_path)
df["date"] = pd.to_datetime(df["date"], errors="coerce")

# Drop rows without weight
df = df.dropna(subset=["weight (lbs)"])

# Plot
plt.figure(figsize=(10,5))
plt.plot(df["date"], df["weight (lbs)"], marker="o")
plt.title("Weight Over Time")
plt.xlabel("Date")
plt.ylabel("Weight (lbs)")
plt.grid(True)
plt.tight_layout()
plt.savefig("visualizations/weight_over_time.png")
plt.show()
