"""
Aggregation is a week form of composition.
If you delete the container object contents objects can live without container object.
"""


class Salary:  # content
    def __init__(self, pay):
        self.pay = pay

    def get_total(self):
        return self.pay * 12


class Employee:
    def __init__(self, pay, bonus):
        self.pay = pay
        self.bonus = bonus

    def annual_salary(self):
        return f'Total annual salary + bonus: {str(self.pay.get_total() + self.bonus)}'


salary = Salary(100)
emp = Employee(salary, 10)
print(emp.annual_salary())