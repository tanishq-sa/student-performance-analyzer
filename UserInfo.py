import re
number = input("Enter Number: ")
result = re.findall(r"\d+[6-9]{10}", number)
if result:
    print("Valid Number")
else:
    print("Invalid Number")