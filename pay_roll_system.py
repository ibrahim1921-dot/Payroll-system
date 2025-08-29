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
# Example usage

total_income = [SalariedEmployee("emp-name", 4, 10000), HourlyEmployee("emp-name", 5, 30, 50), CommissionedEmployee("emp-name", 6, 8000, 30000, 0.5)]
for income in total_income:
    print(f"Employee: {income.name}, ID: {income.id}, Monthly Pay: {income.calculate_pay():.2f}")

# Update the name of the first employee
total_income[0].name = "new-emp-name"
print(f"Updated Employee: {total_income[0].name}, ID: {total_income[0].id}, Monthly Pay: {total_income[0].calculate_pay():.2f}")

#Save to files
save_employees_to_json(total_income, "employees.json")
save_employees_to_csv(total_income, "employees.csv")
