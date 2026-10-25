# import numpy as np
# marks = np.array([78, 92, 65, 85, 72, 88, 55, 80])
# print("Student Marks:")
# print(marks)
# print("\nMean Marks:", np.mean(marks))
# print("Median Marks:", np.median(marks))
# print("Standard Deviation:", np.std(marks))
# print("Minimum Marks:", np.min(marks))
# print("Maximum Marks:", np.max(marks))
# print("Total Marks:", np.sum(marks))
# print("Number of Students:", marks.size)

import numpy as np
import matplotlib.pyplot as plt
students = np.array([
"Amit", "Priya", "Rahul", "Sneha",
"Karan", "Neha", "Arjun", "Pooja"
])
marks = np.array([78, 92, 65, 85, 72, 88, 55, 80])
# Calculate statistics

average = np.mean(marks)
median = np.median(marks)
print("Class Average:", average)
print("Median Marks:", median)
# Create bar chart
plt.bar(students, marks, label="Student Marks")
# Add average reference line
plt.axhline(
y=average,
linestyle="--",
label=f"Class Average: {average:.2f}"
)
plt.title("Student Performance Analysis")
plt.xlabel("Students")
plt.ylabel("Marks")
plt.legend()
plt.grid(axis="y", alpha=0.4)
plt.show()