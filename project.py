import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load and clean dataset
data = pd.read_csv(r"C:\Users\prana\Desktop\project file python\healthcare_dataset.csv")

# Standardize text data
data["Name"] = data["Name"].str.title()
data["Medical Condition"] = data["Medical Condition"].str.title()
data["Hospital"] = data["Hospital"].str.title()

# Handle missing values
data.dropna(inplace=True)

# Convert date columns to datetime format
data["Date of Admission"] = pd.to_datetime(data["Date of Admission"], errors='coerce')
data["Discharge Date"] = pd.to_datetime(data["Discharge Date"], errors='coerce')

# Remove duplicates data
data.drop_duplicates(inplace=True)

# Reset index after cleaning
data.reset_index(drop=True, inplace=True)

# Ensure Billing Amount is numeric
data["Billing Amount"] = pd.to_numeric(data["Billing Amount"], errors='coerce')

# OBJECTIVE 1: Patient Record Summary
print(data.info())
print(data.describe())

# 1. Disease Prediction Heatmap by Age & Gender
# Visualize which diseases are more common for specific age groups and gender combinations.

# Create age bins
data['Age Group'] = pd.cut(data['Age'], bins=[0, 18, 35, 50, 65, 80, 100],
                         labels=['0-18', '19-35', '36-50', '51-65', '66-80', '81-100'])

# Group by Gender, Age Group, and Condition
pivot = data.pivot_table(index='Age Group', columns='Gender', values='Medical Condition', aggfunc=lambda x: x.mode()[0] if not x.mode().empty else None)

plt.figure(figsize=(8, 6))
sns.heatmap(pivot.fillna("N/A").astype(str).applymap(lambda x: len(x)), cmap="YlGnBu", annot=pivot, fmt='')
plt.title("Most Common Disease by Age Group and Gender")
plt.tight_layout()
plt.show()

# Assess treatment cost distribution
plt.figure(figsize=(8, 5))
sns.histplot(data['Billing Amount'], bins=30, kde=True, color='green')
plt.title("Distribution of Treatment Costs")
plt.xlabel("Billing Amount ($)")
plt.ylabel("Frequency")
plt.show()

# Visualize patient demographics
plt.figure(figsize=(8, 5))
gender_counts = data['Gender'].value_counts()
plt.pie(gender_counts, labels=gender_counts.index, autopct='%1.1f%%', colors=['lightblue', 'pink'], startangle=90, shadow=True)
plt.title("Patient Gender Distribution")
plt.show()

plt.figure(figsize=(8, 5))
sns.histplot(data['Age'], bins=20, kde=True, color='purple')
plt.title("Age Distribution of Patients")
plt.xlabel("Age")
plt.ylabel("Frequency")
plt.show()

# Analyze hospital efficiency based on readmission rates
hospital_counts = data['Hospital'].value_counts().head(10)
plt.figure(figsize=(8, 5))
sns.barplot(x=hospital_counts.index, y=hospital_counts.values, palette='Reds')
plt.xticks(rotation=45)
plt.title("Top 10 Hospitals by Admissions")
plt.ylabel("Number of Admissions")
plt.xlabel("Hospital")
plt.show()


data['Length of Stay'] = (data['Discharge Date'] - data['Date of Admission']).dt.days
data_corr = data[['Age', 'Billing Amount', 'Length of Stay']].corr()
plt.figure(figsize=(8, 5))
sns.heatmap(data_corr, annot=True, cmap="coolwarm", fmt=".2f", linewidths=0.5)
plt.title("Correlation Heatmap: Age, Billing Amount, Length of Stay")
plt.show()



# Calculate length of stay
data["Length of Stay"] = (data["Discharge Date"] - data["Date of Admission"]).dt.days

# Evaluate Average Length of Stay for Different Diseases
disease_stay = data.groupby("Medical Condition")["Length of Stay"].mean().sort_values(ascending=False).head(10)

plt.figure(figsize=(8, 5))
sns.barplot(x=disease_stay.index, y=disease_stay.values, palette='coolwarm')
plt.xticks(rotation=45)
plt.title("Average Length of Stay by Disease")
plt.xlabel("Disease")
plt.ylabel("Average Length of Stay (Days)")
plt.show()

# Generate a summary report
report = {
    "Total Patients": len(data),
    "Average Age": data['Age'].mean(),
    "Most Common Disease": data['Medical Condition'].mode()[0],
    "Average Treatment Cost": data['Billing Amount'].mean()
}

print("\nHealthcare Data Analysis Report:\n", report)

# Scatter plot: Impact of Length of Stay on Billing Amount
plt.figure(figsize=(8, 5))
sns.scatterplot(x=data["Length of Stay"], y=data["Billing Amount"], alpha=0.6, color='blue')
plt.title("Impact of Length of Stay on Billing Amount")
plt.xlabel("Length of Stay (days)")
plt.ylabel("Billing Amount ($)")
plt.grid(True)
plt.show()

#  Stacked Area Chart: Patient Record Processing (Admissions over time)
selected_conditions = ['Cancer', 'Diabetes', 'Obesity']
filtered = data[data['Medical Condition'].isin(selected_conditions)].copy()

# Step 2: Group by Month and Condition
filtered['Month'] = filtered['Date of Admission'].dt.to_period('M').dt.to_timestamp()
monthly_counts = filtered.groupby(['Month', 'Medical Condition']).size().unstack(fill_value=0)

# Step 3: Stacked area plot
plt.figure(figsize=(12, 6))
plt.stackplot(
    monthly_counts.index,
    [monthly_counts[cond] for cond in monthly_counts.columns],
    labels=monthly_counts.columns,
    alpha=0.8
)
plt.title("Monthly Admissions by Medical Condition (Stacked Area)")
plt.xlabel("Month")
plt.ylabel("Number of Admissions")
plt.legend(title="Condition", loc='upper left')
plt.xticks(rotation=45)
plt.tight_layout()
plt.grid(True)
plt.show()
