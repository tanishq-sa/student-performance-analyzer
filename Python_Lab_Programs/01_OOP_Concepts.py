from abc import ABC, abstractmethod


class Person(ABC):

    def __init__(self, name, age):
        self._name = name
        self.__age = age

    def get_age(self):
        return self.__age

    def set_age(self, age):
        if age > 0:
            self.__age = age
        else:
            print("Age must be positive.")

    @abstractmethod
    def display_role(self):
        pass

    def display_info(self):
        print(f"Name: {self._name}, Age: {self.__age}")


class Student(Person):

    def __init__(self, name, age, student_id, course):
        super().__init__(name, age)
        self.student_id = student_id
        self.course = course

    def display_role(self):
        print(f"{self._name} is a Student (ID: {self.student_id}, Course: {self.course})")

    def display_info(self):
        super().display_info()
        print(f"Student ID: {self.student_id}, Course: {self.course}")


class Teacher(Person):

    def __init__(self, name, age, subject, experience):
        super().__init__(name, age)
        self.subject = subject
        self.experience = experience

    def display_role(self):
        print(f"{self._name} is a Teacher (Subject: {self.subject}, Experience: {self.experience} years)")

    def display_info(self):
        super().display_info()
        print(f"Subject: {self.subject}, Experience: {self.experience} years")


def show_role(person):
    person.display_role()


if __name__ == "__main__":

    print("=" * 50)
    print("  Object Oriented Programming Concepts Demo")
    print("=" * 50)

    student1 = Student("Tanishq", 20, "BCA2024001", "BCA")
    student2 = Student("Nishita", 21, "BCA2024002", "BCA")
    teacher1 = Teacher("Dr. Sharma", 45, "Python", 15)

    print("\n--- Student 1 Info ---")
    student1.display_info()

    print("\n--- Student 2 Info ---")
    student2.display_info()

    print("\n--- Teacher Info ---")
    teacher1.display_info()

    print("\n--- Polymorphism Demo ---")
    people = [student1, student2, teacher1]
    for person in people:
        show_role(person)

    print("\n--- Encapsulation Demo ---")
    print(f"Student1 Age (via getter): {student1.get_age()}")
    student1.set_age(21)
    print(f"Student1 Age (after setter): {student1.get_age()}")
    student1.set_age(-5)

    print("\n" + "=" * 50)
    print("  Demo Complete")
    print("=" * 50)
