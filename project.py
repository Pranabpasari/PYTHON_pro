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

# Remove duplicates
data.drop_duplicates(inplace=True)

# Reset index after cleaning
data.reset_index(drop=True, inplace=True)

# Ensure Billing Amount is numeric
data["Billing Amount"] = pd.to_numeric(data["Billing Amount"], errors='coerce')

# OBJECTIVE 1: Patient Record Summary
print(data.info())
print(data.describe())

# Identify the most common diseases
disease_counts = data['Medical Condition'].value_counts().head(10)
plt.figure(figsize=(8, 5))
sns.barplot(x=disease_counts.index, y=disease_counts.values, palette='Blues')
plt.xticks(rotation=45)
plt.title("Top 10 Most Common Diseases")
plt.ylabel("Number of Cases")
plt.xlabel("Disease")
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

# Line plot: Patient Record Processing (Admissions over time)
plt.figure(figsize=(8, 5))
data.groupby(data['Date of Admission'].dt.date).size().plot(kind='line', marker='o', color='blue')
plt.title("Patient Record Processing Over Time")
plt.xlabel("Date of Admission")
plt.ylabel("Number of Patients Admitted")
plt.xticks(rotation=45)
plt.grid(True)
plt.show()