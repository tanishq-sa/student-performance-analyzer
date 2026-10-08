import pandas as pd
df = pd.read_csv("students.csv")


def checkAttadance(att):
    if att <= 80:
        return True
    return None

def addMakrs(marks):
    marks += 5
    return marks


df["Check"] = df["Attandance"].apply(checkAttadance)
print(df)

newdf = df[df["Check"] == True]
newdf.to_csv("students1.csv")


df["Bonus_marks"] = df["Marks"].apply(addMakrs)

print(df)

avgmarks = df["Bonus_marks"].mean()

newdf1 = df[df["Bonus_marks"] > avgmarks]

newdf1.to_csv("students3.csv")

df.to_csv("students2.csv")