import numpy as np
marks = np.array([35, 45, 67, 82, 91, 30, 76, 58])
print("All Marks:")
print(marks)
# Students who passed
passing = marks[marks >= 40]
print("\nPassing Marks:")
print(passing)

# Students who failed
failed = marks[marks < 40]
print("\nFailed Marks:")
print(failed)
# Students scoring above 75
high_scorers = marks[marks > 75]
print("\nMarks above 75:")
print(high_scorers)
# Students scoring between 60 and 80
medium_scorers = marks[(marks >= 60) & (marks <= 80)]
print("\nMarks between 60 and 80:")
print(medium_scorers)
# Number of passing students
passing_count = np.sum(marks >= 40)

print("\nNumber of Passing Students:")
print(passing_count)
# Number of failed students
failed_count = np.sum(marks < 40)
print("\nNumber of Failed Students:")
print(failed_count)


marks1 = np.array([35, 48, 52, 67, 74, 81, 89, 95])
# A. Students who scored above 80
# marks[marks > 80]
# B. Students who scored below 50
# marks[marks < 50]
# C. Students who scored between 50 and 80
# marks[(marks >= 50) & (marks <= 80)]

print(marks1[marks1 > 80])
print(marks1[marks1 < 80])
print(marks[(marks >= 50) & (marks <= 80)])

marks2 = np.array([35, 42, 67, 28, 91, 56, 39, 78])
# Ask:
# How many students passed?
#
# They should figure out:
# np.sum(marks >= 40)
# Then ask:
# How many students failed?
# np.sum(marks < 40)

print(np.sum(marks2 >= 40))
print(np.sum(marks2 < 40))

marks = np.array([25, 45, 58, 67, 72, 81, 94])

result = marks[(marks < 40) | (marks > 90)]
print(result)