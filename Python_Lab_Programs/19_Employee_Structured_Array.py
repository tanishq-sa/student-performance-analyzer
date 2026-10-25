import numpy as np

print("=" * 65)
print("  WHY USE A STRUCTURED ARRAY FOR EMPLOYEE RECORDS?")
print("=" * 65)
print("""
Employee records contain fields of different data types:
  - EmployeeID  → integer
  - Name        → string (Unicode)
  - Department  → string (Unicode)
  - Salary      → float
  - Performance → integer

A regular NumPy array can store only ONE data type.  A structured
array defines named fields, each with its own dtype, so that
heterogeneous data (IDs, names, salaries) coexist in one record.

Benefits:
  1. Fields are accessed by name  →  employees["Salary"]
  2. Vectorised NumPy operations  →  fast mean, sort, filter
  3. Memory-efficient contiguous storage (like a C struct)
""")
print("=" * 65)

employee_dtype = [
    ("EmployeeID", "i4"),
    ("Name", "U20"),
    ("DepartmentCode", "U10"),
    ("Salary", "f8"),
    ("Performance", "i4")
]

employees = np.array([
    (101, "Amit", "HR", 45000, 78),
    (102, "Priya", "IT", 65000, 92),
    (103, "Rahul", "SALES", 50000, 85),
    (104, "Sneha", "IT", 70000, 95),
    (105, "Karan", "FINANCE", 48000, 80),
    (106, "Neha", "HR", 55000, 82)
], dtype=employee_dtype)

print("Complete Employee Records:")
print(employees)
print("\nEmployee Names:")
print(employees["Name"])
print("\nMonthly Salaries (Rs.):")
print(employees["Salary"])
print("\nPerformance Scores:")
print(employees["Performance"])

selected = employees[
    (employees["Salary"] > 50000) | (employees["Performance"] >= 85)
]
print("\nEmployees with Salary Above Rs. 50,000 OR Performance at Least 85:")
print(selected)

print("\nAverage Salary:", np.mean(employees["Salary"]))
print("Highest Salary:", np.max(employees["Salary"]))
print("Lowest Salary:", np.min(employees["Salary"]))

sorted_employees = np.sort(employees, order="Performance")[::-1]
print("\nEmployees in Descending Performance Order:")
print(sorted_employees)

print("\nEmployee Records at Positions 0, 2 and 5 (Fancy Indexing):")
print(employees[[0, 2, 5]])
