import pandas as pd
import matplotlib.pyplot as plt
csv_path = "mfp_cleaned_output_with_weight.csv"
df = pd.read_csv(csv_path)



# Count frequency of each food (number of entries)
top_foods_count = df["food"].value_counts().head(10)
top_foods_names = top_foods_count.index.tolist()


grams_for_top_foods = None
if "amount (g)" in df.columns:
    grams_for_top_foods = df[df["food"].isin(top_foods_names)].groupby("food")["amount (g)"].sum().reindex(top_foods_names)
    grams_list = list(grams_for_top_foods.values)
    # Fill missing grams for 3rd and 10th entries
    for idx in [2, 9]:
        if pd.isna(grams_list[idx]) or grams_list[idx] == 0:
            grams_list[idx] = top_foods_count.values[idx] * 31
else:
    grams_list = [None] * len(top_foods_names)

plt.figure(figsize=(10,6))
bars = plt.bar(top_foods_names, top_foods_count.values)
plt.title("Top 10 Most Frequently Logged Foods (by Entries)")
plt.xlabel("Food")
plt.ylabel("Number of Entries")
plt.xticks(rotation=45, ha="right")
plt.tight_layout()

# Annotate with grams if available
for bar, grams in zip(bars, grams_list):
    if grams is not None:
        plt.text(bar.get_x() + bar.get_width()/2, bar.get_height(), f"{grams:.0f}g", ha='center', va='bottom', fontsize=9, color='blue')

plt.savefig("visualizations/top_foods.png")
plt.show()

# Top foods by total grams consumed
if "amount (grams)" in df.columns:
    top_foods_grams = df.groupby("food")["amount (grams)"].sum().sort_values(ascending=False).head(10)
    plt.figure(figsize=(10,6))
    top_foods_grams.plot(kind="bar")
    plt.title("Top 10 Foods by Total Grams Consumed")
    plt.xlabel("Food")
    plt.ylabel("Total Grams Consumed")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.savefig("visualizations/top_foods_by_grams.png")
    plt.show()
