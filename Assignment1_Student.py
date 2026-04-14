class Student:
    __slots__ = ['_name', '_grade', '_attendance', '_id']

    _id_counter = 0

    def __init__(self, name, grade, attendance):
        self._id = Student._id_counter
        Student._id_counter += 1

        self.name = name
        self.grade = grade
        self.attendance = attendance

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if not isinstance(value, str):
            raise TypeError("Name must be a string")
        if not value.strip():
            raise ValueError("Name must be non-empty")
        self._name = value    

    @property
    def grade(self):
        return self._grade

    @grade.setter
    def grade(self, value):
        if not isinstance(value, (int, float)):
            raise TypeError("Grade must be number")
        if not (0 <= value <= 100):
            raise ValueError("Grade must be 0–100")
        self._grade = float(value)

    @property
    def attendance(self):
        return self._attendance

    @attendance.setter
    def attendance(self, value):
        if not isinstance(value, (int, float)):
            raise TypeError("Attendance must be number")
        if not (0 <= value <= 100):
            raise ValueError("Attendance must be 0–100")
        self._attendance = float(value)

    @property
    def status(self):
        if self.grade >= 60 and self.attendance >= 75:
            return "Pass"
        elif self.grade >= 60:
            return "Fail (low attendance)"
        elif self.attendance >= 75:
            return "Fail (low grade)"
        else:
            return "Fail (low grade and attendance)"

    @property
    def id(self):
        return self._id

# s1 = Student("Alice", 85, 90)
# print(s1.status)   
# print(s1.id)       

# s2 = Student("Bob", 75, 60)
# print(s2.status)   
# print(s2.id)    

# s3 = Student("C", 50, 95)
# print(s3.status)   
# print(s3.id)

# s4 = Student("D", 45, 50)
# print(s4.status)   
# print(s4.id)

# # s4.grade = -1

# # s3.grade = "A"

# # s4.id = 5
# s4.x = 1



s1 = Student("Alice", 85, 90)
print(s1.status, s1.id)

s2 = Student("Bob", 75, 60)
print(s2.status, s2.id)

s3 = Student("C", 50, 95)
print(s3.status, s3.id)

s4 = Student("D", 45, 50)
print(s4.status, s4.id)




s = Student("Test", 80, 80)

try:
    s.grade = -1
except ValueError as e:
    print(e)

try:
    s.grade = "A"
except TypeError as e:
    print(e)

try:
    s.id = 5
except AttributeError as e:
    print(e)

try:
    s.x = 1
except AttributeError as e:
    print(e)


