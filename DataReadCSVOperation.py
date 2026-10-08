import numpy as np
import pandas as pd

csv = pd.read_csv("Numerical.csv")

array = np.array(csv["f1"])

print(array)

print(np.max(array))
print(np.min(array))
print(np.median(array))
print(np.std(array))
print(np.sum(array))
print(np.var(array))
