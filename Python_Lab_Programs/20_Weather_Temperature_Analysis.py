import numpy as np
import matplotlib.pyplot as plt

days = np.array([
    1, 2, 3, 4, 5, 6, 7, 8, 9, 10,
    11, 12, 13, 14, 15, 16, 17, 18, 19, 20,
    21, 22, 23, 24, 25, 26, 27, 28, 29, 30
])
temperatures = np.array([
    24, 25, 23, 26, 25, 24, 27,
    28, 29, 27, 30, 28, 29, 31,
    30, 32, 31, 33, 30, 32, 34,
    31, 29, 28, 30, 27, 26, 28, 25, 24
])

print("Day Numbers:")
print(days)
print("\nDaily Temperatures (Celsius):")
print(temperatures)

average = np.mean(temperatures)
median = np.median(temperatures)
minimum = np.min(temperatures)
maximum = np.max(temperatures)
std = np.std(temperatures)
print("\nMean Temperature:", average)
print("Median Temperature:", median)
print("Minimum Temperature:", minimum)
print("Maximum Temperature:", maximum)
print("Standard Deviation:", std)

above_average = temperatures > average
print("\nDays with Temperature Above the Mean:")
print(days[above_average])
print(temperatures[above_average])

threshold = 25
below_threshold = temperatures < threshold
print("\nDays with Temperature Below", threshold, "Celsius:")
print(days[below_threshold])
print(temperatures[below_threshold])

print("\nTemperatures in Ascending Order:")
print(np.sort(temperatures))
print("\nTemperatures in Descending Order:")
print(np.sort(temperatures)[::-1])

groups = np.array(["Days 1-7", "Days 8-14", "Days 15-21", "Days 22-30"])
group_averages = np.array([
    np.mean(temperatures[0:7]),
    np.mean(temperatures[7:14]),
    np.mean(temperatures[14:21]),
    np.mean(temperatures[21:30])
])
print("\nAverage Temperature for Each Group:")
for i in range(len(groups)):
    print(groups[i], ":", group_averages[i])

plt.figure()
plt.plot(days, temperatures, marker="o", label="Daily Temperature")
plt.axhline(y=average, linestyle="--", label=f"Mean: {average:.2f} C")
plt.title("Daily Temperature Changes")
plt.xlabel("Day Number")
plt.ylabel("Temperature (Celsius)")
plt.legend()
plt.grid(True)

plt.figure()
plt.hist(temperatures, bins=6, edgecolor="black")
plt.title("Distribution of Daily Temperatures")
plt.xlabel("Temperature (Celsius)")
plt.ylabel("Number of Days")
plt.grid(axis="y", alpha=0.5)

plt.figure()
plt.bar(groups, group_averages, label="Average Temperature")
plt.title("Average Temperature by Group of Days")
plt.xlabel("Group of Days")
plt.ylabel("Average Temperature (Celsius)")
plt.legend()
plt.grid(axis="y", alpha=0.5)

plt.show()

print("\n" + "=" * 65)
print("  INTERPRETATION OF WEATHER ANALYSIS RESULTS")
print("=" * 65)

print(f"""
1. TEMPERATURE STATISTICS
   • The mean temperature over the 30 days is {average:.2f}°C with a
     standard deviation of {std:.2f}°C, indicating moderate day-to-day
     variability around the average.
   • The median ({median:.1f}°C) is close to the mean, suggesting the
     distribution is roughly symmetric without extreme skew.
   • Temperatures ranged from {minimum}°C (Day {days[np.argmin(temperatures)]}) to
     {maximum}°C (Day {days[np.argmax(temperatures)]}), a spread of {maximum - minimum}°C.

2. TEMPERATURE TREND
   • The line plot shows a clear upward trend from Days 1–21,
     where temperatures rise steadily from the low-to-mid 20s
     to a peak of {maximum}°C.
   • From Day 22 onward, temperatures decline back toward the
     mid-20s, creating an inverted-U (bell-shaped) trend over
     the month.

3. GROUP AVERAGES
   • Days  1–7  : {group_averages[0]:.2f}°C  (coolest week)
   • Days  8–14 : {group_averages[1]:.2f}°C  (warming phase)
   • Days 15–21 : {group_averages[2]:.2f}°C  (warmest week — peak period)
   • Days 22–30 : {group_averages[3]:.2f}°C  (cooling back down)
   The third group (Days 15–21) has the highest average, confirming
   that the warmest period occurred in the second half of the month
   before the decline.
""")
print("=" * 65)
