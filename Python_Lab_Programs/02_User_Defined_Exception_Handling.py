class InvalidAgeError(Exception):

    def __init__(self, age, message="Age must be between 1 and 120"):
        self.age = age
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f"InvalidAgeError: {self.age} -> {self.message}"


class InvalidMarksError(Exception):

    def __init__(self, marks, message="Marks must be between 0 and 100"):
        self.marks = marks
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f"InvalidMarksError: {self.marks} -> {self.message}"


class WeakPasswordError(Exception):

    def __init__(self, message="Password is too weak"):
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f"WeakPasswordError: {self.message}"


def validate_age(age):
    if not isinstance(age, int):
        raise TypeError("Age must be an integer")
    if age < 1 or age > 120:
        raise InvalidAgeError(age)
    return True


def validate_marks(marks):
    if not isinstance(marks, (int, float)):
        raise TypeError("Marks must be a number")
    if marks < 0 or marks > 100:
        raise InvalidMarksError(marks)
    return True


def validate_password(password):
    if len(password) < 8:
        raise WeakPasswordError("Password must be at least 8 characters long")
    if not any(c.isupper() for c in password):
        raise WeakPasswordError("Password must contain at least 1 uppercase letter")
    if not any(c.islower() for c in password):
        raise WeakPasswordError("Password must contain at least 1 lowercase letter")
    if not any(c.isdigit() for c in password):
        raise WeakPasswordError("Password must contain at least 1 digit")
    if not any(c in '@$!%*?&' for c in password):
        raise WeakPasswordError("Password must contain at least 1 special character (@$!%*?&)")
    return True


if __name__ == "__main__":

    print("=" * 50)
    print("  User-Defined Exception Handling Demo")
    print("=" * 50)

    print("\n--- Test 1: Age Validation ---")
    test_ages = [20, -5, 150, "abc"]
    for age in test_ages:
        try:
            validate_age(age)
            print(f"  Age {age}: Valid")
        except InvalidAgeError as e:
            print(f"  {e}")
        except TypeError as e:
            print(f"  TypeError: {e}")

    print("\n--- Test 2: Marks Validation ---")
    test_marks = [85, -10, 110, 100, 0]
    for marks in test_marks:
        try:
            validate_marks(marks)
            print(f"  Marks {marks}: Valid")
        except InvalidMarksError as e:
            print(f"  {e}")
        except TypeError as e:
            print(f"  TypeError: {e}")

    print("\n--- Test 3: Password Validation ---")
    test_passwords = ["abc", "abcdefgh", "Abcdefgh", "Abcdefg1", "Admin@147"]
    for pwd in test_passwords:
        try:
            validate_password(pwd)
            print(f"  Password '{pwd}': Valid")
        except WeakPasswordError as e:
            print(f"  Password '{pwd}': {e}")

    print("\n--- Test 4: try-except-else-finally Block ---")
    try:
        age = int(input("  Enter your age: "))
        validate_age(age)
    except ValueError:
        print("  Error: Please enter a valid integer.")
    except InvalidAgeError as e:
        print(f"  {e}")
    else:
        print(f"  Age {age} is valid! Registration successful.")
    finally:
        print("  Validation process complete.")

    print("\n" + "=" * 50)
    print("  Demo Complete")
    print("=" * 50)
