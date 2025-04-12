import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Set visual style
sns.set(style="whitegrid", palette="pastel")

# Load and clean dataset
data = pd.read_csv(r"C:\Users\prana\Desktop\project file python\healthcare_dataset.csv")

# Standardize text data     
data["Name"] = data["Name"].str.title()
data["Medical Condition"] = data["Medical Condition"].str.title()
data["Hospital"] = data["Hospital"].str.title()

# Handle missing values and duplicates
data.dropna(inplace=True)
data.drop_duplicates(inplace=True)
data.reset_index(drop=True, inplace=True)

# Convert dates and numeric fields
data["Date of Admission"] = pd.to_datetime(data["Date of Admission"], errors='coerce')
data["Discharge Date"] = pd.to_datetime(data["Discharge Date"], errors='coerce')
data["Billing Amount"] = pd.to_numeric(data["Billing Amount"], errors='coerce')

# Compute Length of Stay
data["Length of Stay"] = (data["Discharge Date"] - data["Date of Admission"]).dt.days

# Remove rows with missing critical data
data.dropna(subset=["Length of Stay", "Billing Amount", "Age", "Gender"], inplace=True)

# Patient Record Summary
print(data.info())
print(data.describe())

# Disease Prediction Heatmap by Age & Gender
data['Age Group'] = pd.cut(data['Age'], bins=[0, 18, 35, 50, 65, 80, 100],
                           labels=['0-18', '19-35', '36-50', '51-65', '66-80', '81-100'])

pivot_disease = data.pivot_table(index='Age Group', columns='Gender',
                                 values='Medical Condition',
                                 aggfunc=lambda x: x.mode()[0] if not x.mode().empty else 'N/A',
                                 observed=False)

# Create a simple numerical matrix for heatmap (just the length of the string entries)
pivot_numeric = pivot_disease.apply(lambda x: x.astype(str).apply(len))  # Replaced applymap with apply

plt.figure(figsize=(10, 5))
sns.heatmap(pivot_numeric, annot=pivot_disease, fmt='', cmap='YlGnBu')
plt.title("Most Common Disease by Age Group and Gender")
plt.tight_layout()
plt.show()

# Patient Flow Over Time
data['Admission Month'] = data['Date of Admission'].dt.to_period("M")
monthly_counts = data['Admission Month'].value_counts().sort_index()

plt.figure(figsize=(10, 5))
monthly_counts.plot(kind='line', marker='o', color='teal')
plt.title('Patient Admissions Over Time')
plt.xlabel('Month')
plt.ylabel('Number of Admissions')
plt.grid(True)
plt.tight_layout()
plt.show()

# KDE Plot for Billing Amount
plt.figure(figsize=(10, 5))
sns.kdeplot(data["Billing Amount"].dropna(), color="teal", lw=3, bw_adjust=0.4, fill=True, alpha=0.3)
plt.title("Distribution of Treatment Costs", fontsize=18, fontweight='bold', color='darkblue')
plt.xlabel("Billing Amount ($)", fontsize=14, color='darkblue')
plt.ylabel("Density", fontsize=14, color='darkblue')
plt.xticks(fontsize=12, color='black')
plt.yticks(fontsize=12, color='black')
plt.show()

# Gender Distribution Pie Chart
plt.figure(figsize=(10, 5))
gender_counts = data["Gender"].value_counts()
plt.pie(gender_counts, labels=gender_counts.index, autopct='%1.1f%%',
        colors=['lightblue', 'pink'], startangle=90, shadow=True)
plt.title("Patient Gender Distribution")
plt.tight_layout()
plt.show()

# Age Distribution
plt.figure(figsize=(10, 5))
sns.histplot(data["Age"], bins=20, kde=True, color="purple")
plt.title("Age Distribution of Patients")
plt.xlabel("Age")
plt.ylabel("Frequency")
plt.tight_layout()
plt.show()

# Top 10 Hospitals by Admissions
top_hospitals = data["Hospital"].value_counts().head(10)
plt.figure(figsize=(10, 5))
sns.barplot(x=top_hospitals.values, y=top_hospitals.index, hue=top_hospitals.index, palette='Reds', legend=False)
plt.title("Top 10 Hospitals by Admissions")
plt.xlabel("Admissions")
plt.ylabel("Hospital")
plt.tight_layout()
plt.show()

# Correlation Heatmap: Age, Billing Amount, Length of Stay
plt.figure(figsize=(10, 5))
corr = data[["Age", "Billing Amount", "Length of Stay"]].corr()
sns.heatmap(corr, annot=True, cmap="coolwarm", fmt=".2f")
plt.title("Correlation Heatmap")
plt.tight_layout()
plt.show()

# Average Length of Stay by Disease (Top 10)
avg_stay = data.groupby("Medical Condition")["Length of Stay"].mean().sort_values(ascending=False).head(10)

plt.figure(figsize=(10, 5))
sns.barplot(x=avg_stay.index, y=avg_stay.values, hue=avg_stay.index, palette="coolwarm", legend=False)  # Fixed for palette warning
plt.xticks(rotation=45)
plt.title("Average Length of Stay by Disease")
plt.ylabel("Average Stay (Days)")
plt.xlabel("Disease")
plt.tight_layout()
plt.show()

# Report Summary
report = {
    "Total Patients": len(data),
    "Average Age": round(data["Age"].mean(), 2),
    "Most Common Disease": data["Medical Condition"].mode()[0],
    "Average Treatment Cost": round(data["Billing Amount"].mean(), 2)
}
print("\nHealthcare Data Summary Report:\n", report)
