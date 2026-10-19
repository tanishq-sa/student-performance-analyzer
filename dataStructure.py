import numpy as np
student_dtype = [
("RollNo", "i4"),
("Name", "U20"),
("Marks", "i4"),
("Attendance", "f4")
]
students = np.array([
(101, "Amit", 78, 85.5),
(102, "Priya", 92, 90.0),
(103, "Rahul", 65, 75.5),
(104, "Sneha", 85, 88.0),
(105, "Karan", 72, 80.0)
], dtype=student_dtype)
print("Complete Student Data:")
print(students)
print("\nStudent Names:")
print(students["Name"])
print("\nStudent Marks:")
print(students["Marks"])
print("\nAverage Marks:")
print(np.mean(students["Marks"]))
high_scorers = students[students["Marks"] > 75]
print("\nStudents scoring above 75:")
print(high_scorers)
print("\nNames of High Scorers:")
print(high_scorers["Name"])
sorted_students = np.sort(students, order="Marks")
print("\nStudents sorted by Marks:")
print(sorted_students)