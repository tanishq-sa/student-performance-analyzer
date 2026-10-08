import numpy as np

marks = np.array([10,20,30,40])

print(marks+5)

internal = np.array([1,2,3,4,5,6,7,8,9,10,11,12,13,14,15])
external = np.array([1,2,3,4,5,6,7,8,9,10,11,12,13,14,15])
print(internal + external)

print(marks - 2)
print(marks * 2)

print(np.sum(marks))
print(np.min(marks))
print(np.max(marks))
print(np.mean(marks))
print(np.median(marks))
print(np.std(marks))
print(np.var(marks))


