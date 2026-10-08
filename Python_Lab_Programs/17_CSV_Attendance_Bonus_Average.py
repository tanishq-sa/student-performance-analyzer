import pandas as pd
import random

print("=" * 50)
print("  CSV Operations - Attendance, Bonus & Average")
print("=" * 50)

print("\n--- Step 1: Creating students.csv with 30 records ---")

names = [
    "Amit", "Tanishq", "Nishita", "Rahul", "Priya",
    "Sneha", "Ashish", "Riya", "Karan", "Meera",
    "Rohan", "Anita", "Vikram", "Pooja", "Arjun",
    "Deepa", "Suresh", "Kavita", "Manish", "Neha",
    "Rajesh", "Sunita", "Arun", "Divya", "Pankaj",
    "Swati", "Nikhil", "Rekha", "Sanjay", "Anjali"
]

random.seed(42)

data = {
    "Student": names,
    "Marks": [random.randint(35, 100) for _ in range(30)],
    "Attendance": [random.randint(60, 100) for _ in range(30)],
}

df = pd.DataFrame(data)
df.to_csv("students.csv", index=False)

print(f"Created students.csv with {len(df)} records")
print(df.to_string(index=False))

print("\n" + "=" * 50)
print("--- Step 2: Students with Attendance Below 85% ---")

low_attendance_df = df[df["Attendance"] < 85]

print(f"\nFound {len(low_attendance_df)} students with attendance below 85%:")
print(low_attendance_df.to_string(index=False))

low_attendance_df.to_csv("students_low_attendance.csv", index=False)
print("\nSaved to students_low_attendance.csv")

print("\n" + "=" * 50)
print("--- Step 3: Bonus Marks for Attendance > 85% ---")

def add_bonus_marks(row):
    if row["Attendance"] > 85:
        return row["Marks"] + 5
    return row["Marks"]

df["Bonus_Marks"] = df.apply(add_bonus_marks, axis=1)

print("\nStudents with Bonus Marks (Attendance > 85% get +5):")
print(df[["Student", "Marks", "Attendance", "Bonus_Marks"]].to_string(index=False))

df.to_csv("students_bonus.csv", index=False)
print("\nSaved to students_bonus.csv")

print("\n" + "=" * 50)
print("--- Step 4: Students Above Average Marks ---")

average_marks = df["Marks"].mean()
print(f"\nAverage Marks: {average_marks:.2f}")

above_average_df = df[df["Marks"] > average_marks]

print(f"\nFound {len(above_average_df)} students above average:")
print(above_average_df[["Student", "Marks"]].to_string(index=False))

above_average_df.to_csv("average_marks.csv", index=False)
print("\nSaved to average_marks.csv")

print("\n" + "=" * 50)
print("  Summary of Files Created")
print("=" * 50)
print("  1. students.csv           - Original 30 student records")
print("  2. students_low_attendance.csv - Students with attendance < 85%")
print("  3. students_bonus.csv     - All students with Bonus_Marks column")
print("  4. average_marks.csv      - Students scoring above average marks")

print("\n" + "=" * 50)
print("  Demo Complete")
print("=" * 50)
