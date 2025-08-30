#This is a trial project that test my  knowledge on OOP in python

#importing abstract base class  module
from abc import ABC, abstractmethod
import json
import csv

#Abstract class
class Employee (ABC):
    def __init__(self, name, id):
        self.__name = name
        self.__id = id

    # Getter for name
    @property
    def name (self):
        return self.__name

    #Setter for name
    @name.setter
    def name (self, new_name):
        self.__name = new_name
        
    # Getter for ID
    @property
    def id (self):
        return self.__id

    # This method should be overridden in subclasses to calculate pay
    @abstractmethod
    def calculate_pay (self):
        pass

#salaried employee class (Inherits from the employee class, but its own attribute)
class SalariedEmployee(Employee):
    
    def __init__(self, name, id, monthly_salary):
        # Call the constructor of the parent class
        super().__init__(name, id)
        self.monthly_salary = monthly_salary
        
    #implement the calculatePay()
    def calculate_pay (self):
        
        if self.monthly_salary <= 0:
            raise ValueError("Monthly salary must be a positive number!")
        return self.monthly_salary
    
    def to_dict (self):
        return {
            "type": self.__class__.__name__,
            "name": self.name,
            "id": self.id,
            "monthly_salary": self.monthly_salary
        }

#Hourly employee class (Inherit from the employee class, but also add its own attributes)
class HourlyEmployee(Employee):
    WEEKLY_WORKING_HOURS = 40 #default value for weekly working hours
    OVER_TIME_RATE = 1.5 #default value for overtime rate
    WEEKS_IN_A_MONTH = 4 #default value for weeks in a month
    
    def __init__(self, name, id, hourly_rate, hours_worked):
        super().__init__(name, id)
        self.hourly_rate = hourly_rate
        self.hours_worked = hours_worked
        
    #implement the calculatePay()
    def calculate_pay (self):
        if self.hours_worked < 0:
            raise ValueError("Hours worked must be positive numbers!")
        if self.hourly_rate <= 0:
            raise ValueError("Hourly rate must be a positive number!")
        if self.hours_worked > self.WEEKLY_WORKING_HOURS:
            overtime_hours = self.hours_worked - self.WEEKLY_WORKING_HOURS
            weekly_pay = (self.WEEKLY_WORKING_HOURS * self.hourly_rate + self.OVER_TIME_RATE * self.hourly_rate * overtime_hours)
            monthly_pay = weekly_pay * self.WEEKS_IN_A_MONTH
            return monthly_pay
        else:
            weekly_pay = self.hours_worked * self.hourly_rate
            monthly_pay = weekly_pay * self.WEEKS_IN_A_MONTH
            return monthly_pay
        
    def to_dict (self):
        return {
            "type": self.__class__.__name__,
            "name": self.name,
            "id": self.id,
            "hourly_rate": self.hourly_rate,
            "hours_worked": self.hours_worked
        }

class CommissionedEmployee(Employee):
    def __init__(self, name, id, base_salary, sales_amount, commission_rate):
        super().__init__(name, id)
        self.base_salary = base_salary
        self.sales_amount = sales_amount
        self.commission_rate = commission_rate
        
    #implement the calculatePay()
    def calculate_pay (self):
        if self.base_salary < 0:
            raise ValueError("Base salary must be a positive number!")
        if self.sales_amount < 0:
            raise ValueError("Sales amount must be a positive number!")
        if not (0 <= self.commission_rate <= 1):
            raise ValueError("Commission rate must be between 0 and 1!")
        return self.base_salary + self.sales_amount * self.commission_rate
    
    def to_dict (self):
        return {
            "type": self.__class__.__name__,
            "name": self.name,
            "id": self.id,
            "base_salary": self.base_salary,
            "sales_amount": self.sales_amount,
            "commission_rate": self.commission_rate
        }
    
# Save employee data to a JSON file
def save_employees_to_json (employees, file_path="employees.json"):
    with open (file_path, "w", encoding="utf-8") as f:
        json.dump([e.to_dict() for e in employees], f, indent=2)

#Save employee data to a CSV file
def save_employees_to_csv(employees, file_path="employees.csv"):
    fieldnames = [
        "type", "name", "id",
        "monthly_salary", "hourly_rate", "hours_worked",
        "base_salary", "sales_amount", "commission_rate",
    ]
    with open(file_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for e in employees:
            row = {k: "" for k in fieldnames}
            row.update(e.to_dict())
            writer.writerow(row)

def _prompt_str(prompt):
    return input(prompt)

def _prompt_int(prompt, min_val=None, max_val=None):
    while True:
        try:
            value = int(input(prompt))
            if (min_val is not None and value < min_val) or (max_val is not None and value > max_val):
                raise ValueError
            return value
        except ValueError:
            print(f"Please enter a valid integer between {min_val} and {max_val}.")

def _prompt_float(prompt, min_val=None, max_val=None):
    while True:
        try:
            value = float(input(prompt))
            if (min_val is not None and value < min_val) or (max_val is not None and value > max_val):
                raise ValueError
            return value
        except ValueError:
            print(f"Please enter a valid number between {min_val} and {max_val}.")

def create_employee(etype):
    name = _prompt_str("Name: ")
    emp_id = _prompt_int("ID (integer): ", min_val=0)

    if etype == "salaried":
        monthly_salary = _prompt_float("Monthly salary: ", min_val=0.01)
        return SalariedEmployee(name, emp_id, monthly_salary)

    if etype == "hourly":
        hourly_rate = _prompt_float("Hourly rate: ", min_val=0.01)
        hours_worked = _prompt_float("Hours worked (per week): ", min_val=0.0)
        return HourlyEmployee(name, emp_id, hourly_rate, hours_worked)

    base_salary = _prompt_float("Base salary: ", min_val=0.0)
    sales_amount = _prompt_float("Sales amount: ", min_val=0.0)
    commission_rate = _prompt_float("Commission rate (0.0 - 1.0): ", min_val=0.0, max_val=1.0)
    return CommissionedEmployee(name, emp_id, base_salary, sales_amount, commission_rate)

# Create a list of employees for demonstration purposes
employees = [
    SalariedEmployee("Alice", 1, 5000),
    HourlyEmployee("Bob", 2, 20, 45),
    CommissionedEmployee("Charlie", 3, 3000, 20000, 0.1)
]

print("\nCalculated Monthly Pay:")
for e in employees:
    try:
        print(f"Employee: {e.name}, ID: {e.id}, Monthly Pay: {e.calculate_pay():.2f}")
    except Exception as ex:
        print(f"Error calculating pay for {e.name} (ID {e.id}): {ex}")

save_employees_to_json(employees, "employees.json")
save_employees_to_csv(employees, "employees.csv")
print('Saved to "employees.json" and "employees.csv".')
