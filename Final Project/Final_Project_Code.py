# Groupmember 1 Responsibilities

import pandas as pd
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from pathlib import Path

sns.set(style="whitegrid")

def acronym_fixing(data_frame_column):
    """
    Fix common hospital/network acronyms by uppercasing them
    after using .title() on the string.
    """
    acronym_to_be_fixed = str(data_frame_column).title()

    acronyms = ["Nyc", "Nyu", "Nyp", "Mvhs", "Li", "Suny", "Upmc", "Wmc", "Sbh", "Mc"]

    for acronym in acronyms:
        acronym_to_be_fixed = acronym_to_be_fixed.replace(acronym, acronym.upper())

    return acronym_to_be_fixed

from IPython.display import display

# Setting the base paths
BASE = Path.cwd()
DATA = BASE / "data"

file_one_path = DATA / "New_York_State_Statewide_Hospital_Bed_Capacity.csv"
file_two_path = DATA / "New_York_State_Statewide_Weekly_COVID-19_Hospitalizations_and_Fatalities.csv"

# Reading the CSV files into DataFrames
df_hospital_bed_capacity = pd.read_csv(file_one_path)
df_weekly_covid19_hospitalizations_and_fatalities = pd.read_csv(file_two_path)

pd.set_option("display.max_columns", 20)
pd.set_option("display.width", 120)

print("Hospital Bed Capacity (first 5 rows):")
display(df_hospital_bed_capacity.head())

print("\nWeekly COVID-19 Hospitalizations and Fatalities (first 5 rows):")
display(df_weekly_covid19_hospitalizations_and_fatalities.head())

# Cleaning text columns in the Bed Capacity DataFrame
df_hospital_bed_capacity["Facility Name"] = df_hospital_bed_capacity["Facility Name"].str.title()
df_hospital_bed_capacity["Facility Name"] = df_hospital_bed_capacity["Facility Name"].str.replace(r"\s*\(\d+\)", "", regex=True)
df_hospital_bed_capacity["DOH Region"] = df_hospital_bed_capacity["DOH Region"].str.title()
df_hospital_bed_capacity["Facility County"] = df_hospital_bed_capacity["Facility County"].str.title()
df_hospital_bed_capacity["Facility Network"] = df_hospital_bed_capacity["Facility Network"].str.title()
df_hospital_bed_capacity["NY Forward Region"] = df_hospital_bed_capacity["NY Forward Region"].str.title()

# Cleaning text columns in the COVID-19 DataFrame
df_weekly_covid19_hospitalizations_and_fatalities["Facility Name"] = (df_weekly_covid19_hospitalizations_and_fatalities["Facility Name"].str.title())
df_weekly_covid19_hospitalizations_and_fatalities["DOH Region"] = (df_weekly_covid19_hospitalizations_and_fatalities["DOH Region"].str.title())
df_weekly_covid19_hospitalizations_and_fatalities["Facility County"] = (df_weekly_covid19_hospitalizations_and_fatalities["Facility County"].str.title())

# Converting the "As of Date" column to Python datetime objects
df_hospital_bed_capacity["As of Date"] = pd.to_datetime(df_hospital_bed_capacity["As of Date"])
df_weekly_covid19_hospitalizations_and_fatalities["As of Date"] = pd.to_datetime(df_weekly_covid19_hospitalizations_and_fatalities["As of Date"])

# Aggregating Bed Capacity Data to Weekly Frequency
agg_rules = {
    "Total Staffed Acute Care Beds": "mean",
    "Total Staffed Acute Care Beds Occupied": "mean",
    "Total Staffed Acute Care Beds Available": "mean",
    "Total Staffed ICU Beds": "mean",
    "Total Staffed ICU Beds Currently Occupied": "mean",
    "Total Staffed ICU Beds Currently Available": "mean",
    "Facility Network": "first",
    "NY Forward Region": "first"
}

bed_capacity_weekly = df_hospital_bed_capacity.groupby(["Facility PFI", pd.Grouper(key="As of Date", freq="W-SAT")]).agg(agg_rules).reset_index()

# Merging the Aggregated Weekly Bed Data with the Weekly COVID Data
df_combined = pd.merge(bed_capacity_weekly, df_weekly_covid19_hospitalizations_and_fatalities, how="inner", on=["Facility PFI", "As of Date"])

# Previewing
print(f"Combined DataFrame Shape: {df_combined.shape}")
print("Columns:", df_combined.columns.tolist())
df_combined.head()

# Replacing string placeholders for missing values with NaN (including for dates)
missing_placeholders = ["null", "N/A", ""]
cols_to_clean = [
    "As of Date",
    "Facility Name",
    "DOH Region",
    "Facility County",
    "Facility Network",
    "NY Forward Region",
]

for col in cols_to_clean:
    df_combined[col] = df_combined[col].replace(missing_placeholders, np.nan)

# Using "Unknown" for missing values from textual columns
cat_cols = ["Facility Name", "DOH Region", "Facility County", "Facility Network", "NY Forward Region"]
for col in cat_cols:
    df_combined[col] = df_combined[col].fillna("Unknown")

# Keeping real dates, leaving missing values as NaT
df_combined["As of Date"] = pd.to_datetime(df_combined["As of Date"], errors="coerce")
df_combined = df_combined.sort_values(by="As of Date", ascending=True)

# Fixing capitalization and acronyms after handling missing values
df_combined["Facility Name"] = df_combined["Facility Name"].apply(acronym_fixing)
df_combined["Facility Name"] = df_combined["Facility Name"].str.replace(r"'S", r"'s", regex=True)
df_combined["Facility Network"] = df_combined["Facility Network"].apply(acronym_fixing)

# Replacing numerical columns with NaNs with the means of their respective columns
num_cols = [
    "Total Staffed Acute Care Beds",
    "Total Staffed Acute Care Beds Occupied",
    "Total Staffed ICU Beds",
    "Total Staffed ICU Beds Currently Occupied",
    "Total Staffed Acute Care Beds Available",
    "Total Staffed ICU Beds Currently Available",
    "Total New COVID-19 Admissions Reported",
    "COVID-19 Patients Expired",
]

for col in num_cols:
    df_combined[col] = pd.to_numeric(df_combined[col], errors="coerce")
    df_combined[col] = df_combined[col].fillna(df_combined[col].mean())
    df_combined[col] = df_combined[col].round().astype(int)

# Only removing rows where HOSPITAL CAPACITY is invalid (0 beds)
delete_rows_invalid_capacity = (
    (df_combined["Total Staffed Acute Care Beds"] == 0) |
    (df_combined["Total Staffed ICU Beds"] == 0)
)

df_combined = df_combined[~delete_rows_invalid_capacity].reset_index(drop=True)

# Sorting by date
df_combined = df_combined.sort_values(by="As of Date", ascending=True)

df_combined.head()

# Graphing data as a time-series plot
plt.figure(figsize=(15, 8))
plt.title("Time-Series of Bed Availability and COVID-19 Outcomes in NYS")
plt.xlabel("As of Date")
plt.ylabel("Count")

# Graphing data as a collection of bar graphs
plt.plot(df_combined["As of Date"], df_combined["Total Staffed Acute Care Beds Available"], label="Acute Care Beds Available")
plt.plot(df_combined["As of Date"], df_combined["Total Staffed ICU Beds Currently Available"], label="ICU Beds Available")
plt.plot(df_combined["As of Date"], df_combined["Total New COVID-19 Admissions Reported"], label="New COVID-19 Admissions")
plt.plot(df_combined["As of Date"], df_combined["COVID-19 Patients Expired"], label="COVID-19 Patients Expired")

plt.legend(loc="upper right")
plt.grid(True)
plt.tight_layout()
plt.ylim(0, 350)
plt.show()

plt.figure(figsize=(16, 6))
sns.barplot(x="As of Date", y="Total Staffed Acute Care Beds Available", data=df_combined, errorbar=None)
plt.title("Average Weekly Total Staffed Acute Care Beds Available")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

plt.figure(figsize=(16, 6))
sns.barplot(x="As of Date", y="Total Staffed ICU Beds Currently Available", data=df_combined, errorbar=None)
plt.title("Average Weekly Total Staffed ICU Beds Currently Available")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

plt.figure(figsize=(16, 6))
sns.barplot(x="As of Date", y="Total New COVID-19 Admissions Reported", data=df_combined, errorbar=None)
plt.title("Average Weekly Total New COVID-19 Admissions Reported")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

plt.figure(figsize=(16, 6))
sns.barplot(x="As of Date", y="COVID-19 Patients Expired", data=df_combined, errorbar=None)
plt.title("Average Weekly COVID-19 Patients Expired")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# Defining the output directory to be the "data" folder directly
OUTPUT_DIR = Path.cwd() / "data"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

output_path = OUTPUT_DIR / "DataFrame_Combined.csv"
df_combined.to_csv(output_path, index=False)

print(f"Saved combined, cleaned DataFrame to: {output_path}")

# Groupmember 2 Responsibilities

import sqlite3

# Creating a connection to a new SQLite database
conn = sqlite3.connect("hospital_covid_project.db")

# Loading our clean dataframe into SQL
df_combined.to_sql("weekly_data", conn, if_exists="replace", index=False)
print("Data successfully loaded into SQLite table 'weekly_data'.")

# Verifying with a SQL Query
query = """
SELECT
    "As of Date",
    "Facility Name",
    "Total Staffed Acute Care Beds Available",
    "Total Staffed ICU Beds Currently Available",
    "Total New COVID-19 Admissions Reported",
    "COVID-19 Patients Expired"
FROM weekly_data
WHERE "COVID-19 Patients Expired" > 0
ORDER BY "COVID-19 Patients Expired" DESC
LIMIT 5;
"""

# Executing the query and display the result
print("\nSample SQL Query Result (Top 5 Facilities with Fatalities):")
sql_result = pd.read_sql(query, conn)
display(sql_result)

# Closing the connection when done
conn.close()

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score

# Defining Features (X) and Target (y)
features = [
    "Total Staffed Acute Care Beds Available",
    "Total Staffed ICU Beds Currently Available",
    "Acute Care Occupancy Rate",
    "Total New COVID-19 Admissions Reported"
]
target = "COVID-19 Patients Expired"

X = df_combined[features]
y = df_combined[target]

# Spliting Data into Training and Testing Sets (80% Train, 20% Test)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Initializing and Training the Model
model = LinearRegression()
model.fit(X_train, y_train)

# Making Predictions
y_pred = model.predict(X_test)

# Evaluating the Model
rmse = np.sqrt(mean_squared_error(y_test, y_pred))
r2 = r2_score(y_test, y_pred)

print("--- Linear Regression Model Results ---")
print(f"Root Mean Squared Error (RMSE): {rmse:.2f}")
print(f"R² Score: {r2:.4f} (Closer to 1.0 means better fit)")
print("\nFeature Coefficients (Impact on Fatalities):")
for feature, coef in zip(features, model.coef_):
    print(f" - {feature}: {coef:.4f}")

# Visualizing Predictions vs Actuals
plt.figure(figsize=(10, 6))
plt.scatter(y_test, y_pred, alpha=0.5)
plt.plot([y.min(), y.max()], [y.min(), y.max()], 'r--', lw=2) # The "Perfect Prediction" line
plt.xlabel("Actual Fatalities")
plt.ylabel("Predicted Fatalities")
plt.title("Linear Regression: Actual vs. Predicted Fatalities")
plt.show()
