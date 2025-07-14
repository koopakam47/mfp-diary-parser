import pdfplumber
import pandas as pd
import os
import re

print("🚀 Starting enhanced MyFitnessPal PDF cleanup with units and gram conversion...")

folder_path = "."
pdf_files = [f for f in os.listdir(folder_path) if f.endswith(".pdf")]
all_entries = []

# Regex: capture food name, amount, and all macros
pattern = re.compile(
    r"^(?P<food>.+?),\s(?P<amount>[\d.]+(?:\s\w+)+)\s(?P<calories>\d+)\s(?P<carbs>\d+)g\s(?P<fat>\d+)g\s(?P<protein>\d+)g\s(?P<cholest>\d+)mg\s(?P<sodium>\d+)mg\s(?P<sugar>\d+)g\s(?P<fiber>\d+)g$"
)

date_pattern = re.compile(r"^[A-Za-z]{3,9} \d{1,2}, \d{4}$")

def convert_amount_to_grams(amount_str):
    try:
        match = re.match(r"(?P<value>[\d.]+)\s?(?P<unit>[a-zA-Z]+)", amount_str)
        if not match:
            return None
        value = float(match.group("value"))
        unit = match.group("unit").lower()

        # Approximate conversion
        if unit in ["g", "gram", "grams"]:
            return value
        elif unit in ["ml", "milliliter", "milliliters"]:
            return value  # assume 1 ml ≈ 1 g
        elif unit in ["oz", "ounce", "ounces"]:
            return value * 28.35
        elif unit in ["lb", "pound", "pounds"]:
            return value * 453.592
        elif unit in ["tbsp", "tablespoon", "tablespoons"]:
            return value * 15
        elif unit in ["tsp", "teaspoon", "teaspoons"]:
            return value * 5
        elif unit in ["cup", "cups"]:
            return value * 240
        else:
            return None
    except:
        return None

for filename in pdf_files:
    file_path = os.path.join(folder_path, filename)
    print(f"\U0001F4C4 Processing: {filename}")
    with pdfplumber.open(file_path) as pdf:
        current_date = ""
        for page in pdf.pages:
            text = page.extract_text()
            if not text:
                continue


            lines = [line.strip() for line in text.split('\n') if line.strip()]
            merged_lines = []
            i = 0
            while i < len(lines):
                line = lines[i]
                # Section header or URL
                if date_pattern.match(line) or any(x in line for x in ["MyFitnessPal", "Printable Diary", "FOODS", "TOTALS", "English"]):
                    merged_lines.append(line)
                    i += 1
                    continue
                # Try to detect 3-line food entry: food, macros, amount
                if (i+2 < len(lines)
                    and re.match(r".+", lines[i])
                    and re.match(r"^\d+ \d+g \d+g \d+g", lines[i+1])
                    and re.match(r".*(gram|ml|oz|cup|tablespoon|teaspoon|container|bar|can|piece|muffin|cookie|slice|tortilla|g)$", lines[i+2], re.IGNORECASE)):
                    merged_lines.append(f"{lines[i]}, {lines[i+2]} {lines[i+1]}")
                    i += 3
                    continue
                # Try to detect 2-line food entry: food, macros
                if (i+1 < len(lines)
                    and re.match(r".+", lines[i])
                    and re.match(r"^\d+ \d+g \d+g \d+g", lines[i+1])):
                    merged_lines.append(f"{lines[i]} {lines[i+1]}")
                    i += 2
                    continue
                # Otherwise, just add the line
                merged_lines.append(line)
                i += 1

            for line in merged_lines:
                if date_pattern.match(line):
                    current_date = line
                    continue

                if any(x in line for x in ["MyFitnessPal", "Printable Diary", "FOODS", "TOTALS", "English"]):
                    continue

                match = pattern.match(line)
                if match:
                    entry = match.groupdict()
                    entry["date"] = current_date
                    entry["source_file"] = filename.replace(".pdf", "")
                    entry["amount (g)"] = convert_amount_to_grams(entry["amount"])

                    # Convert all macros to integers
                    for field in ["calories", "carbs", "fat", "protein", "cholest", "sodium", "sugar", "fiber"]:
                        entry[field] = int(entry[field])

                    all_entries.append(entry)
                else:
                    # Try a looser fallback regex for lines that don't match
                    fallback = re.match(r"^(?P<food>.+?),\s(?P<amount>[^,]+)\s(?P<calories>\d+)\s(?P<carbs>\d+)g\s(?P<fat>\d+)g\s(?P<protein>\d+)g", line)
                    if fallback:
                        entry = fallback.groupdict()
                        entry["date"] = current_date
                        entry["source_file"] = filename.replace(".pdf", "")
                        entry["amount (g)"] = convert_amount_to_grams(entry["amount"])
                        # Fill missing fields with None
                        for field in ["cholest", "sodium", "sugar", "fiber"]:
                            entry[field] = None
                        for field in ["calories", "carbs", "fat", "protein"]:
                            entry[field] = int(entry[field])
                        all_entries.append(entry)
                    else:
                        # Log skipped line for review
                        print(f"[SKIPPED] {filename}: '{line}'")

# Create DataFrame and rename columns with units
df = pd.DataFrame(all_entries)
df.rename(columns={
    "calories": "calories",
    "carbs": "carbs (grams)",
    "fat": "fat (grams)",
    "protein": "protein (grams)",
    "cholest": "cholesterol (mg)",
    "sodium": "sodium (mg)",
    "sugar": "sugar (grams)",
    "fiber": "fiber (grams)"
}, inplace=True)

# Reorder columns
df = df[[
    "date", "source_file", "food", "amount", "amount (g)",
    "calories", "carbs (grams)", "fat (grams)", "protein (grams)",
    "cholesterol (mg)", "sodium (mg)", "sugar (grams)", "fiber (grams)"
]]

# Save to CSV
output_path = os.path.join(folder_path, "mfp_cleaned_output.csv")
df.to_csv(f"data/{output_path}", index=False)

print(f"✅ Cleaned CSV created with units and gram conversion: {output_path}")
