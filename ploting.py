# import matplotlib.pyplot as plt
# tests = [1, 2, 3, 4, 5]
# marks = [45, 55, 60, 72, 85]
# plt.plot(tests, marks, marker="o", label="Student Marks")
# plt.title("Student Performance Across Tests")
# plt.xlabel("Test Number")
# plt.ylabel("Marks")
# plt.legend()
# plt.grid(True)
# plt.show()


# import matplotlib.pyplot as plt
# students = ["Amit", "Priya", "Rahul", "Sneha", "Karan"]
# marks = [78, 92, 65, 85, 72]
# plt.bar(students, marks, label="Marks")
# plt.title("Student Marks Comparison")
# plt.xlabel("Students")
# plt.ylabel("Marks")
# plt.legend()
# plt.grid(axis="y", linestyle="--", alpha=0.5)
# plt.show()

# import matplotlib.pyplot as plt
# study_hours = [1, 2, 3, 4, 5, 6, 7, 8]
# marks = [35, 40, 50, 55, 65, 70, 80, 90]
# plt.scatter(study_hours, marks, label="Students")
# plt.title("Study Hours vs Examination Marks")
# plt.xlabel("Study Hours per Day")
# plt.ylabel("Marks")
# plt.legend()
# plt.grid(True)
# plt.show()

# import matplotlib.pyplot as plt
# marks = [
# 35, 42, 45, 48, 50, 52, 55, 58,
# 60, 62, 65, 68, 70, 72, 75, 78,
# 80, 82, 85, 90, 92, 95
# ]
# plt.hist(marks, bins=5, edgecolor="black")
# plt.title("Distribution of Student Marks")
# plt.xlabel("Marks")
# plt.ylabel("Number of Students")
# plt.grid(axis="y", alpha=0.5)
# plt.show()

# import matplotlib.pyplot as plt
# tests = [1, 2, 3, 4, 5]
# marks = [45, 55, 60, 72, 85]
# plt.plot(tests, marks, marker="o", label="Student Marks")
# plt.title("Student Performance Across Tests")
# plt.xlabel("Test Number")
# plt.ylabel("Marks")
# plt.legend()
# plt.show()


# import matplotlib.pyplot as plt
# students = ["Prihu", "Kailesh", "Priyanshi", "Sneha", "Karan"]
# marks = [78, 92, 65, 85, 72]
# plt.bar(students, marks, label="Marks")
# plt.title("Student Marks Comparison")
# plt.xlabel("Students")
# plt.ylabel("Marks")
# plt.legend()
# plt.grid(axis="y", linestyle="--", alpha=0.5)
# plt.show()


import numpy as np
import matplotlib.pyplot as plt

students = np.array([
"Sahil", "Nitya", "Nishita", "Sneha",
"Yash", "Tanishq", "Ashish", "Mayank"
])
marks = np.array([78, 90, 65, 85, 72, 88, 45, 80])
average = np.mean(marks)
print("Class Average:", average)
above_average = marks > average
print("\nStudents scoring above average:")
print(students[above_average])
print(marks[above_average])
plt.bar(students, marks, label="Student Marks")
plt.axhline(
y=average,
linestyle="--",
label=f"Class Average: {average:.2f}"
)
plt.title("Class Performance Analysis")
plt.xlabel("Students")
plt.ylabel("Marks")
plt.legend()
plt.grid(axis="y", alpha=0.5)
plt.show()