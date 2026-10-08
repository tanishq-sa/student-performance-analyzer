import pandas as pd
import matplotlib.pyplot as plt

print("=" * 50)
print("  Statistical Analysis on Dataset")
print("=" * 50)

data = {
    "Student": ["Amit", "Tanishq", "Nishita", "Rahul", "Priya", "Sneha", "Ashish", "Riya"],
    "Math": [78, 95, 88, 45, 92, 67, 55, 83],
    "Python": [85, 100, 90, 50, 89, 72, 60, 78],
    "DBMS": [72, 92, 85, 38, 95, 65, 48, 80],
    "AI": [90, 98, 92, 42, 91, 70, 58, 85],
}

df = pd.DataFrame(data)

print("\n--- Dataset ---")
print(df)

subjects = ["Math", "Python", "DBMS", "AI"]

print("\n--- Mean (Average) ---")
for subject in subjects:
    print(f"  {subject}: {df[subject].mean():.2f}")

print("\n--- Median ---")
for subject in subjects:
    print(f"  {subject}: {df[subject].median():.2f}")

print("\n--- Standard Deviation ---")
for subject in subjects:
    print(f"  {subject}: {df[subject].std():.2f}")

print("\n--- Summary Statistics ---")
print(df[subjects].describe())

df["Average"] = df[subjects].mean(axis=1)

print("\n--- Student Averages ---")
print(df[["Student", "Average"]])

fig, axes = plt.subplots(2, 2, figsize=(12, 10))

axes[0, 0].bar(df["Student"], df["Average"], color="steelblue")
axes[0, 0].set_title("Student Average Marks")
axes[0, 0].set_ylabel("Average")
axes[0, 0].tick_params(axis='x', rotation=45)

subject_means = [df[s].mean() for s in subjects]
axes[0, 1].bar(subjects, subject_means, color=["#FF6B6B", "#4ECDC4", "#45B7D1", "#96CEB4"])
axes[0, 1].set_title("Subject-wise Average")
axes[0, 1].set_ylabel("Average Marks")

axes[1, 0].boxplot([df[s] for s in subjects], labels=subjects)
axes[1, 0].set_title("Subject-wise Distribution (Box Plot)")
axes[1, 0].set_ylabel("Marks")

for subject in subjects:
    axes[1, 1].plot(df["Student"], df[subject], marker='o', label=subject)
axes[1, 1].set_title("Student Performance Across Subjects")
axes[1, 1].set_ylabel("Marks")
axes[1, 1].legend()
axes[1, 1].tick_params(axis='x', rotation=45)

plt.tight_layout()
plt.savefig("statistical_analysis.png")
plt.show()

print("\nVisualization saved as statistical_analysis.png")

print("\n" + "=" * 50)
print("  Demo Complete")
print("=" * 50)
