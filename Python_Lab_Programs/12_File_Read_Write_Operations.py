import os
import xml.etree.ElementTree as ET

print("=" * 50)
print("  Read and Write Operations with Files")
print("=" * 50)

print("\n--- Text File Operations ---")

with open("sample.txt", "w") as f:
    f.write("Name: Tanishq Saini\n")
    f.write("Course: BCA\n")
    f.write("College: Christ University\n")

print("Written to sample.txt")

with open("sample.txt", "r") as f:
    content = f.read()
    print("Reading sample.txt:")
    print(content)

with open("sample.txt", "a") as f:
    f.write("Year: 2024\n")

print("Appended to sample.txt")

with open("sample.txt", "r") as f:
    lines = f.readlines()
    print("Reading line by line:")
    for i, line in enumerate(lines, 1):
        print(f"  Line {i}: {line.strip()}")

print("\n--- Binary File Operations ---")

import struct

student_record = struct.pack('20s i f', b'Tanishq', 20, 95.5)

with open("student.bin", "wb") as f:
    f.write(student_record)

print("Written binary data to student.bin")

with open("student.bin", "rb") as f:
    data = f.read()
    name, age, marks = struct.unpack('20s i f', data)
    print(f"  Name: {name.decode().strip(chr(0))}")
    print(f"  Age: {age}")
    print(f"  Marks: {marks:.1f}")

records = [
    struct.pack('20s i f', b'Tanishq', 20, 95.5),
    struct.pack('20s i f', b'Nishita', 21, 88.0),
    struct.pack('20s i f', b'Ashish', 22, 76.5),
]

with open("students.bin", "wb") as f:
    for record in records:
        f.write(record)

print("\nWritten multiple records to students.bin")

record_size = struct.calcsize('20s i f')
with open("students.bin", "rb") as f:
    print("Reading all binary records:")
    while True:
        data = f.read(record_size)
        if not data:
            break
        name, age, marks = struct.unpack('20s i f', data)
        print(f"  Name: {name.decode().strip(chr(0))}, Age: {age}, Marks: {marks:.1f}")

if os.path.exists("student.bin"):
    os.remove("student.bin")
if os.path.exists("students.bin"):
    os.remove("students.bin")

print("\n--- XML File Operations ---")

root = ET.Element("students")

student_data = [
    ("Tanishq", "tanishq@example.com", "BCA"),
    ("Nishita", "nishita@example.com", "BSc"),
    ("Ashish", "ashish@example.com", "MCA"),
]

for name, email, course in student_data:
    student = ET.SubElement(root, "student")
    student.set("name", name)

    email_elem = ET.SubElement(student, "email")
    email_elem.text = email

    course_elem = ET.SubElement(student, "course")
    course_elem.text = course

tree = ET.ElementTree(root)
tree.write("students.xml")
print("Written to students.xml")

tree = ET.parse("students.xml")
root = tree.getroot()

print("Reading students.xml:")
for student in root.findall("student"):
    name = student.get("name")
    email = student.find("email").text
    course = student.find("course").text
    print(f"  Name: {name}, Email: {email}, Course: {course}")

if os.path.exists("sample.txt"):
    os.remove("sample.txt")
if os.path.exists("students.xml"):
    os.remove("students.xml")

print("\n" + "=" * 50)
print("  Demo Complete")
print("=" * 50)
