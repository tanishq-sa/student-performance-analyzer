import pandas as pd

data = {
    "Students" : ["Amit", "Tanishq", "Nishita"],
    "Marks": [30, 100, 90],
    "Attendance": [81, 100, 75],
}

df = pd.DataFrame(data)
# print(df["Students"])
# print(df["Attendance"].mean())
# print(df["Marks"].max())
# new_df = df[["Students", "Marks"]]
# print(new_df)

print(df[["Students","Attendance"]])
print(df[df["Attendance"] > 80])
print(df[df["Attendance"] > 80])
print(df[df["Attendance"] > 85] & df[df["Marks"] > 75])
