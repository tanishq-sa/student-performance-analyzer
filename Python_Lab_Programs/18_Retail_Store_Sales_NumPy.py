import numpy as np

products = np.array(["Rice", "Milk", "Bread", "Soap"])
months = np.array(["January", "February", "March"])
sales = np.array([
    [12000, 15000, 18000],
    [20000, 22000, 24000],
    [8000, 9000, 10000],
    [10000, 12000, 14000]
])

print("Products:", products)
print("Months:", months)
print("Sales Figures (Rows: Products, Columns: Months):")
print(sales)
print("\nDimensions:", sales.ndim)
print("Shape:", sales.shape)
print("Number of Elements:", sales.size)

product_totals = np.sum(sales, axis=1)
month_totals = np.sum(sales, axis=0)
print("\nTotal Sales for Each Product:")
for i in range(len(products)):
    print(products[i], ":", product_totals[i])

print("\nTotal Sales for Each Month:")
for i in range(len(months)):
    print(months[i], ":", month_totals[i])

threshold = 40000
high_sales = product_totals > threshold
print("\nProducts with Total Sales Above", threshold, ":")
print(products[high_sales])
print(product_totals[high_sales])

print("\nFirst and Third Products:")
print(products[[0, 2]])
print(sales[[0, 2]])

order = np.argsort(product_totals)[::-1]
print("\nProduct-wise Total Sales in Descending Order:")
print(products[order])
print(product_totals[order])
print("Best-performing Product:", products[order[0]])

averages = np.mean(sales, axis=1)
print("\nAverage Monthly Sales for Each Product:")
for i in range(len(products)):
    print(products[i], ":", averages[i])
