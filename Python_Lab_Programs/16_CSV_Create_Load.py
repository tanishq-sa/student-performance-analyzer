import csv
import os

print("=" * 50)
print("  CSV File Operations")
print("=" * 50)

print("\n--- Creating CSV File ---")

header = ["Name", "Age", "Course", "Marks", "Email"]

students = [
    ["Tanishq", 20, "BCA", 95, "tanishq@example.com"],
    ["Nishita", 21, "BSc", 88, "nishita@example.com"],
    ["Ashish", 22, "MCA", 76, "ashish@example.com"],
    ["Rahul", 20, "BCA", 65, "rahul@example.com"],
    ["Priya", 21, "BSc", 92, "priya@example.com"],
]

with open("students.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(header)
    writer.writerows(students)

print("Created students.csv")

print("\n--- Reading CSV using csv.reader ---")

with open("students.csv", "r") as f:
    reader = csv.reader(f)
    for row in reader:
        print(f"  {row}")

print("\n--- Reading CSV using csv.DictReader ---")

with open("students.csv", "r") as f:
    reader = csv.DictReader(f)
    for row in reader:
        print(f"  {row['Name']} | Age: {row['Age']} | Course: {row['Course']} | Marks: {row['Marks']}")

print("\n--- Loading CSV into List of Dictionaries ---")

data = []
with open("students.csv", "r") as f:
    reader = csv.DictReader(f)
    for row in reader:
        data.append(row)

print(f"Loaded {len(data)} records into list.")
for record in data:
    print(f"  {record}")

print("\n--- Loading CSV into Dictionary of Lists ---")

columns = {}
with open("students.csv", "r") as f:
    reader = csv.DictReader(f)
    for row in reader:
        for key, value in row.items():
            if key not in columns:
                columns[key] = []
            columns[key].append(value)

print("Column-wise data:")
for col_name, values in columns.items():
    print(f"  {col_name}: {values}")

print("\n--- Filtering Data ---")

print("Students with Marks > 80:")
for record in data:
    if int(record['Marks']) > 80:
        print(f"  {record['Name']} - {record['Marks']}")

if os.path.exists("students.csv"):
    os.remove("students.csv")

print("\n" + "=" * 50)
print("  Demo Complete")
print("=" * 50)
