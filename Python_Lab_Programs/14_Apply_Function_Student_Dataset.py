import pandas as pd

print("=" * 50)
print("  Demonstrate apply() Function on Student Dataset")
print("=" * 50)

data = {
    "Student": ["Amit", "Tanishq", "Nishita", "Rahul", "Priya", "Sneha", "Ashish", "Riya"],
    "Math": [78, 95, 88, 45, 92, 67, 55, 83],
    "Python": [85, 100, 90, 50, 89, 72, 60, 78],
    "DBMS": [72, 92, 85, 38, 95, 65, 48, 80],
    "AI": [90, 98, 92, 42, 91, 70, 58, 85],
    "Attendance": [91, 96, 78, 65, 88, 82, 70, 93],
}

df = pd.DataFrame(data)
subjects = ["Math", "Python", "DBMS", "AI"]

print("\n--- Original Dataset ---")
print(df)

print("\n--- 1. apply() to Calculate Average Marks (Row-wise) ---")
df["Average"] = df[subjects].apply(lambda row: row.mean(), axis=1)
print(df[["Student", "Average"]])


print("\n--- 2. apply() to Assign Grade ---")


def assign_grade(avg):
    if avg >= 90:
        return "A+"
    elif avg >= 80:
        return "A"
    elif avg >= 70:
        return "B"
    elif avg >= 60:
        return "C"
    elif avg >= 50:
        return "D"
    else:
        return "F"


df["Grade"] = df["Average"].apply(assign_grade)
print(df[["Student", "Average", "Grade"]])


print("\n--- 3. apply() to Determine Pass/Fail ---")


def check_result(row):
    for subject in subjects:
        if row[subject] < 40:
            return "FAIL"
    return "PASS"


df["Result"] = df.apply(check_result, axis=1)
print(df[["Student", "Result"]])


print("\n--- 4. apply() to Check Attendance Status ---")


def check_attendance(att):
    if att >= 85:
        return "Regular"
    elif att >= 75:
        return "Irregular"
    else:
        return "Detained"


df["Attendance_Status"] = df["Attendance"].apply(check_attendance)
print(df[["Student", "Attendance", "Attendance_Status"]])


print("\n--- 5. apply() to Add Bonus Marks ---")


def add_bonus(row):
    if row["Attendance"] > 85:
        return row["Average"] + 5
    return row["Average"]


df["Final_Marks"] = df.apply(add_bonus, axis=1)
print(df[["Student", "Average", "Attendance", "Final_Marks"]])


print("\n--- 6. apply() on Columns (Column-wise) ---")
print("Subject-wise Mean:")
print(df[subjects].apply(lambda col: col.mean()))

print("\nSubject-wise Max:")
print(df[subjects].apply(lambda col: col.max()))


print("\n--- 7. apply() to Find Topper in Each Subject ---")


def find_topper(col):
    idx = col.idxmax()
    return df.loc[idx, "Student"]


toppers = df[subjects].apply(find_topper)
print(toppers)


print("\n--- Final Dataset ---")
print(df)

print("\n" + "=" * 50)
print("  Demo Complete")
print("=" * 50)
