# MyFitnessPal Diary Parser & Nutrition Dashboard

## Overview
This project is a comprehensive dashboard for tracking and analyzing my nutritional data from January 1, 2025 to July 14, 2025. During this period, I have meticulously tracked every single food I've consumed. By parsing food diary PDFs exported from MyFitnessPal, merging with weight and fitness data, and visualizing key metrics, I can gain actionable insights into my dietary habits and identify potential nutritional deficiencies.

## Purpose
The main goal of this dashboard is to help you:
- Monitor daily intake of calories, macros, and nutrients.
- Track weight changes over time.
- Identify frequently consumed foods and their nutritional impact.
- Detect patterns and deficiencies in your diet for improved health and fitness outcomes.

## Techniques Used
- **PDF Parsing:** Extracts food diary entries from MyFitnessPal PDF exports using `pdfplumber` and robust regex logic to handle multi-line and edge-case entries.
- **Data Cleaning:** Cleans and merges food diary data with weight logs using `pandas`, ensuring all relevant rows are included and missing values are handled.
- **Visualization:** Uses `matplotlib` to create clear, informative charts for calories, macros, nutrients, and top foods.
- **Automation:** Scripts are modular and can be run independently for each visualization or data processing step.

## Folder Structure
- `pdf/` — Contains all original MyFitnessPal diary PDFs.
- `data/` — Contains all processed CSV files, including cleaned diary and merged weight data.
- `visualizations/` — Contains all generated PNG charts for easy review.

## Visualizations & Summaries

### 1. Weight Over Time vs. Calorie Intake
![Weight Over Time](visualizations/weight_over_time.png)
- Weight loss has been consistent over time and cheat days have had little to no impact on consistent weight gain. Moderate to aggresive increase in calorie intake drives weight gain, while aggresive dieting leads to psychological and physical burnout and causes unplanned cheat days.

### 2. Daily Calorie Intake
![Daily Calorie Intake](visualizations/daily_calories.png)


### 3. Daily Macros
![Daily Macros](visualizations/daily_macros.png)
- Most spikes in macro intake are due to cheat days. Increased carb intake in July has lead to improved physical performance and feelings of satiety. I've faced difficulty in keeping my protein intake under 200 grams. Fats have been kept deliberately low to allow for more carb intake but I'm slowly increasing them to see how it effects physical performance.


### 4. Daily Nutrients
#### Cholesterol
![Daily Cholesterol](visualizations/daily_cholesterol_mg.png)
- Overall my cholesterol intake is a bit high (over 300 mg), but spikes are driven by cheat days.

#### Sodium
![Daily Sodium](visualizations/daily_sodium_mg.png)

- I often go over the 2300 mg recommendation, but I don't find this concerning as I rely on sodium as a source of electrolytes, and my blood pressure is in a very healthy range.

#### Sugar
![Daily Sugar](visualizations/daily_sugar_grams.png)
- My sugar intake is usually moderate, but it jumps after cheat days, desserts, or lots of fruit.

#### Fiber
![Daily Fiber](visualizations/daily_fiber_grams.png)
- Overall fiber intake is in a good spot.

### 5. Top Foods
![Top Foods](visualizations/top_foods.png)
- I see that lean proteins like chicken breast and protein powder, and staple carbs like rice and lentils, are my top foods. 

## How to Use
1. Place your MyFitnessPal diary PDFs in the `pdf/` folder.
2. Run `mfp_cleaner.py` to parse and clean the data.
3. Run `mfp_add_weight.py` to merge weight logs.
4. Use the visualization scripts (`plot_weight_over_time.py`, `plot_daily_calories.py`, `plot_daily_macros.py`, `plot_top_foods.py`) to generate charts in the `visualizations/` folder.

## Requirements
- Python 3.x
- `pdfplumber`, `pandas`, `matplotlib`

Install dependencies:
```bash
pip install pdfplumber pandas matplotlib
```

## Customization & Extensibility
- Easily add new visualizations or data sources by extending the provided scripts.
- All file paths are modular and update automatically with folder changes.

## License
This project is licensed under the MIT License. See the LICENSE file for details.

## Author
Andrew Kaminski

---

For questions or further customization, feel free to reach out!
