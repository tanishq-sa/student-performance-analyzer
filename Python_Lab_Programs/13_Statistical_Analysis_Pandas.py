import pandas as pd

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

print("\n" + "=" * 50)
print("  Demo Complete")
print("=" * 50)
