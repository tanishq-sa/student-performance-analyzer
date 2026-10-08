import numpy as np
import pandas as pd

class_A = np.array([70, 72, 75, 78, 80])
class_B = np.array([50, 65, 75, 90, 95])
print("Class A Average:", np.mean(class_A))
print("Class B Average:", np.mean(class_B))
print("\nClass A Standard Deviation:", np.std(class_A))
print("Class B Standard Deviation:", np.std(class_B))


csv = pd.read_csv("Numerical.csv")

array = np.array(csv["f1"])

print(array.mean())
print(array.std())