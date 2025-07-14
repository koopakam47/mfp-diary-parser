import pandas as pd
from datetime import datetime

# === Paths for Codespaces environment ===
food_path = "mfp_cleaned_output.csv"
weight_path = "Fitdays-22287.csv"
output_path = "mfp_cleaned_output_with_weight.csv"

print("🚀 Merging food diary with weight data...")

# === Load food diary CSV ===
food_df = pd.read_csv(f"data/{food_path}")
food_df["date"] = pd.to_datetime(food_df["date"], format="%b %d, %Y")

# === Load weight data CSV ===
weight_df = pd.read_csv(f"data/{weight_path}")

# Extract the date from "Date" column (e.g., "13:12 Jul.14 2025" → "Jul.14 2025")
weight_df["Date"] = weight_df["Date"].str.extract(r"(\w+\.\d{1,2}\s\d{4})")[0]
weight_df["Date"] = pd.to_datetime(weight_df["Date"], format="%b.%d %Y")

# Keep only the latest weight per day
latest_weights = weight_df.sort_values("Date").drop_duplicates("Date", keep="last")
latest_weights = latest_weights[["Date", "Weight"]]
latest_weights.rename(columns={"Date": "date", "Weight": "weight (lbs)"}, inplace=True)

# Clean "weight (lbs)" column (remove 'lb' and convert to float)
latest_weights["weight (lbs)"] = latest_weights["weight (lbs)"].str.replace("lb", "", regex=False).astype(float)

# === Merge on date ===
merged_df = pd.merge(food_df, latest_weights, on="date", how="left")

# === Output to new CSV ===
merged_df.to_csv(f"data/{output_path}", index=False)
print(f"✅ Done! Output saved to: {output_path}")

