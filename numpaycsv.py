import pandas as pd
data = {
    "Students": ["Tanishq", "Nishita"],
    "Marks": [98, 78],
    "Attandance": [85, 90]
}

df = pd.DataFrame(data)
df.to_csv("students.csv")
print("CSV File Created")