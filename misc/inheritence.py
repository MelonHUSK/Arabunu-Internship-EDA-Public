class Person:
  def __init__(self, fname, lname):
    self.firstname = fname
    self.lastname = lname

  def printname(self):
    print(self.firstname, self.lastname)

class Student(Person):
    def __init__(self, fname, lname, year):
        super().__init__(fname, lname)
        self.graduationYear = year

    def welcomeMessage(self):
      print("Welcome " + self.firstname + " " + self.lastname + " to the graduation year of", self.graduationYear, "!")

s1 = Student("John", "Doe", 2025)
s1.printname()
s1.welcomeMessage()