import os
import xml.etree.ElementTree as ET

root = ET.Element('student')
student_date = [
    ("tanishq", "tanishq@example.com"),
    ("nishita", "nishita@example.com"),
    ("ashish", "ashish@example.com"),
]

for name, email in student_date:
    student = ET.SubElement(root, 'student')
    student.set('name', name)

    emailint =ET.SubElement(student, 'email')
    emailint.text = email


tree = ET.ElementTree(root)
tree.write("test.xml")