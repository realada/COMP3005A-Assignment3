from datetime import date
import db

db.restoreTable()
# db.addStudent("Test", "One", "testone@gmail.com", date(2026, 11, 15))

# students = db.getAllStudents()
# for student in students:
#     print(student)

# db.updateStudentEmail(4, "onetest@gmail.com")

# students = db.getAllStudents()
# print("\n")
# for student in students:
#     print(student)

#messagebox before delete
# db.deleteStudent(4)
# print("\n")
# students = db.getAllStudents()
# for student in students:
#     print(student)

db.close()