import numpy as np
marks = np.array([45, 67, 82, 91, 56, 73])
print("All Marks:")
print(marks)
print("\nElement at index 2:")
print(marks[2])
print("\nElements at indexes 0, 2 and 5:")
print(marks[[0, 2, 5]])

students = np.array([
"Amit",
"Priya",
"Rahul",
"Sneha",
"Karan"
])
marks = np.array([78, 92, 65, 85, 74])
selected_students = students[[0, 2, 4]]
selected_marks = marks[[0, 2, 4]]
print("Selected Students:")
print(selected_students)
print("\nTheir Marks:")
print(selected_marks)

marks = np.array([
[78, 82, 75],
[92, 88, 90],
[65, 70, 68],
[85, 80, 88]
])
print("Complete Dataset:")
print(marks)
print("\nRows 0, 2 and 3:")
print(marks[[0, 2, 3]])