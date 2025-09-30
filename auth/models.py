from werkzeug.security import generate_password_hash, check_password_hash

class User:
    def __init__(self, name, email, department, position, salary, password):
        self.name = name
        self.email = email
        self.department = department
        self.position = position
        self.salary = salary
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
