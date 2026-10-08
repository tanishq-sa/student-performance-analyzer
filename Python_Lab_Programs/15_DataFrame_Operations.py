import pandas as pd
import matplotlib.pyplot as plt

print("=" * 50)
print("  DataFrame Operations - Calculations & Sorting")
print("=" * 50)

data = {
    "Student": ["Amit", "Tanishq", "Nishita", "Rahul", "Priya", "Sneha", "Ashish", "Riya", "Karan", "Meera"],
    "Math": [78, 95, 88, 45, 92, 67, 55, 83, 70, 60],
    "Python": [85, 100, 90, 50, 89, 72, 60, 78, 75, 65],
    "DBMS": [72, 92, 85, 38, 95, 65, 48, 80, 68, 58],
    "AI": [90, 98, 92, 42, 91, 70, 58, 85, 73, 62],
    "Java": [80, 88, 82, 40, 87, 63, 52, 76, 71, 55],
}

df = pd.DataFrame(data)

subjects = ["Math", "Python", "DBMS", "AI", "Java"]

print("\n--- Dataset ---")
print(df)

print("\n--- Mean ---")
for s in subjects:
    print(f"  {s}: {df[s].mean():.2f}")

print("\n--- Median ---")
for s in subjects:
    print(f"  {s}: {df[s].median():.2f}")

print("\n--- Standard Deviation ---")
for s in subjects:
    print(f"  {s}: {df[s].std():.2f}")

print("\n--- Variance ---")
for s in subjects:
    print(f"  {s}: {df[s].var():.2f}")

print("\n--- Min and Max ---")
for s in subjects:
    print(f"  {s}: Min={df[s].min()}, Max={df[s].max()}")

print("\n--- Complete Statistics ---")
print(df[subjects].describe())

df["Average"] = df[subjects].mean(axis=1)
df["Total"] = df[subjects].sum(axis=1)
df["Result"] = df[subjects].apply(lambda row: "PASS" if all(row >= 40) else "FAIL", axis=1)

print("\n--- Results ---")
print(df[["Student", "Total", "Average", "Result"]])

fig, axes = plt.subplots(2, 3, figsize=(18, 12))

axes[0, 0].bar(df["Student"], df["Average"], color="steelblue")
axes[0, 0].axhline(y=df["Average"].mean(), color='red', linestyle='--', label='Class Average')
axes[0, 0].set_title("Student Average Marks")
axes[0, 0].set_ylabel("Average")
axes[0, 0].tick_params(axis='x', rotation=45)
axes[0, 0].legend()

subject_means = [df[s].mean() for s in subjects]
colors = ["#FF6B6B", "#4ECDC4", "#45B7D1", "#96CEB4", "#FFEAA7"]
axes[0, 1].bar(subjects, subject_means, color=colors)
axes[0, 1].set_title("Subject-wise Average")
axes[0, 1].set_ylabel("Average Marks")

axes[0, 2].boxplot([df[s] for s in subjects], labels=subjects)
axes[0, 2].set_title("Subject Distribution (Box Plot)")
axes[0, 2].set_ylabel("Marks")

for subject in subjects:
    axes[1, 0].plot(df["Student"], df[subject], marker='o', label=subject)
axes[1, 0].set_title("Performance Across Subjects")
axes[1, 0].set_ylabel("Marks")
axes[1, 0].legend(fontsize=8)
axes[1, 0].tick_params(axis='x', rotation=45)

subject_stds = [df[s].std() for s in subjects]
axes[1, 1].bar(subjects, subject_stds, color=colors)
axes[1, 1].set_title("Subject-wise Standard Deviation")
axes[1, 1].set_ylabel("Std Deviation")

pass_count = (df["Result"] == "PASS").sum()
fail_count = (df["Result"] == "FAIL").sum()
axes[1, 2].pie(
    [pass_count, fail_count],
    labels=["Pass", "Fail"],
    autopct='%1.1f%%',
    colors=["#4ECDC4", "#FF6B6B"]
)
axes[1, 2].set_title("Pass/Fail Distribution")

plt.tight_layout()
plt.savefig("statistical_analysis_visualizations.png")
plt.show()

print("\nVisualizations saved as statistical_analysis_visualizations.png")

print("\n" + "=" * 50)
print("  Demo Complete")
print("=" * 50)
