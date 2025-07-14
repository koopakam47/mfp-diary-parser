import pandas as pd
import matplotlib.pyplot as plt
csv_path = "mfp_cleaned_output_with_weight.csv"
df = pd.read_csv(csv_path)
df["date"] = pd.to_datetime(df["date"], errors="coerce")

# Group by date and sum macros/nutrients
macro_cols = ["carbs (grams)", "fat (grams)", "protein (grams)"]
nutrient_cols = ["cholesterol (mg)", "sodium (mg)", "sugar (grams)", "fiber (grams)"]
daily_macros = df.groupby("date")[macro_cols].sum().reset_index()
daily_nutrients = df.groupby("date")[nutrient_cols].sum().reset_index()

# Macros plot
plt.figure(figsize=(12,7))
for col in macro_cols:
    plt.plot(daily_macros["date"], daily_macros[col], label=col)
plt.title("Daily Intake of Macros")
plt.xlabel("Date")
plt.ylabel("Grams")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig("visualizations/daily_macros.png")
plt.show()


# Plot each nutrient separately
for col in nutrient_cols:
    plt.figure(figsize=(10,5))
    plt.plot(daily_nutrients["date"], daily_nutrients[col], marker="o")
    plt.title(f"Daily Intake of {col}")
    plt.xlabel("Date")
    plt.ylabel("mg" if "mg" in col else "grams")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(f"visualizations/daily_{col.replace(' ', '_').replace('(', '').replace(')', '').replace('/', '_')}.png")
    plt.show()
