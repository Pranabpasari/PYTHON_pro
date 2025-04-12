import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load and clean dataset
data = pd.read_csv(r"C:\Users\prana\Desktop\project file python\healthcare_dataset.csv")

# Standardize text and remove missing/duplicate entries
data = data.dropna().drop_duplicates()
data["Name"] = data["Name"].str.title()
data["Medical Condition"] = data["Medical Condition"].str.title()
data["Hospital"] = data["Hospital"].str.title()

# Convert date columns and billing to proper format
data["Date of Admission"] = pd.to_datetime(data["Date of Admission"], errors='coerce')
data["Discharge Date"] = pd.to_datetime(data["Discharge Date"], errors='coerce')
data["Billing Amount"] = pd.to_numeric(data["Billing Amount"], errors='coerce')

# Calculate length of stay and age group
data["Length of Stay"] = (data["Discharge Date"] - data["Date of Admission"]).dt.days
data["Age Group"] = pd.cut(data["Age"], bins=[0, 18, 35, 50, 65, 80, 100],
                           labels=['0-18', '19-35', '36-50', '51-65', '66-80', '81-100'])

# --- Objective 1: Patient Record Summary ---
print(data.info())
print(data.describe())

# Disease heatmap by age group and gender
pivot = data.pivot_table(index="Age Group", columns="Gender",
                         values="Medical Condition",
                         aggfunc=lambda x: x.mode()[0] if not x.mode().empty else None)

plt.figure(figsize=(8, 6))
sns.heatmap(pivot.fillna("").astype(str).applymap(len), cmap="YlGnBu", annot=pivot, fmt='')
plt.title("Most Common Disease by Age Group and Gender")
plt.tight_layout()
plt.show()

# Treatment cost distribution
sns.histplot(data["Billing Amount"], bins=30, kde=True, color="green")
plt.title("Distribution of Treatment Costs")
plt.xlabel("Billing Amount ($)")
plt.ylabel("Frequency")
plt.show()

# Gender distribution pie chart
gender_counts = data["Gender"].value_counts()
plt.pie(gender_counts, labels=gender_counts.index, autopct='%1.1f%%',
        colors=['lightblue', 'pink'], startangle=90, shadow=True)
plt.title("Patient Gender Distribution")
plt.show()

# Age distribution
sns.histplot(data["Age"], bins=20, kde=True, color="purple")
plt.title("Age Distribution of Patients")
plt.xlabel("Age")
plt.ylabel("Frequency")
plt.show()

# Top 10 hospitals by admission count (horizontal bar chart)
top_hospitals = data["Hospital"].value_counts().head(10)
sns.barplot(x=top_hospitals.values, y=top_hospitals.index, palette='Reds')
plt.title("Top 10 Hospitals by Admissions")
plt.xlabel("Admissions")
plt.ylabel("Hospital")
plt.tight_layout()
plt.show()


# Correlation heatmap: Age, Billing, Stay
corr = data[["Age", "Billing Amount", "Length of Stay"]].corr()
sns.heatmap(corr, annot=True, cmap="coolwarm", fmt=".2f")
plt.title("Correlation Heatmap")
plt.show()

# Average length of stay by disease (top 10)
avg_stay = data.groupby("Medical Condition")["Length of Stay"].mean().sort_values(ascending=False).head(10)
sns.barplot(x=avg_stay.index, y=avg_stay.values, palette="coolwarm")
plt.xticks(rotation=45)
plt.title("Average Length of Stay by Disease")
plt.ylabel("Average Stay (Days)")
plt.xlabel("Disease")
plt.show()

# Report Summary
report = {
    "Total Patients": len(data),
    "Average Age": round(data["Age"].mean(), 2),
    "Most Common Disease": data["Medical Condition"].mode()[0],
    "Average Treatment Cost": round(data["Billing Amount"].mean(), 2)
}
print("\nHealthcare Data Summary Report:\n", report)

# Stacked area chart for selected conditions over time
selected = data[data["Medical Condition"].isin(["Cancer", "Diabetes", "Obesity"])].copy()
selected["Month"] = selected["Date of Admission"].dt.to_period("M").dt.to_timestamp()
monthly = selected.groupby(["Month", "Medical Condition"]).size().unstack(fill_value=0)

plt.stackplot(monthly.index, [monthly[c] for c in monthly.columns], labels=monthly.columns, alpha=0.8)
plt.title("Monthly Admissions by Medical Condition")
plt.xlabel("Month")
plt.ylabel("Number of Admissions")
plt.legend(title="Condition")
plt.xticks(rotation=45)
plt.grid(True)
plt.tight_layout()
plt.show()

