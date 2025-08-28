#This is a trial project that test my  knowledge on OOP in python

#importing abstract base class  module
from abc import ABC, abstractmethod

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
    def ID (self):
        return self.__id

    # This method should be overridden in subclasses to calculate pay
    @abstractmethod
    def calculatePay (self):
        pass

#salaried employee class (Inherits from the employee class, but its own attribute)
class SalariedEmployee(Employee):
    
    def __init__(self, name, ID, monthlySalary):
        # Call the constructor of the parent class
        super().__init__(name, ID)
        self.monthlySalary = monthlySalary
        
    #implement the calculatePay()
    def calculatePay (self):
        
        if self.monthlySalary <= 0:
            raise ValueError("Monthly salary must be a positive number!")
        return self.monthlySalary

#Hourly employee class (Inherit from the employee class, but also add its own attributes)
class HourlyEmployee(Employee):
    WEEKLY_WORKING_HOURS = 40 #default value for weekly working hours
    OVER_TIME_RATE = 1.5 #default value for overtime rate
    
    def __init__(self, name, ID, hourlyRate, hoursWorked):
        super().__init__(name, ID)
        self.hourlyRate = hourlyRate
        self.hoursWorked = hoursWorked
        
    #implement the calculatePay()
    def calculatePay (self):
        if self.hoursWorked < 0 or self.hourlyRate < 0:
            raise ValueError("Hours worked and hourly rate must be positive numbers!")
        if self.hoursWorked > self.WEEKLY_WORKING_HOURS:
            weekly_pay = (self.WEEKLY_WORKING_HOURS * self.hourlyRate) + self.OVER_TIME_RATE * self.hourlyRate
            monthly_pay = weekly_pay * 4  # Assuming 4 weeks in a month
            return monthly_pay
        else:
            weekly_pay = self.hoursWorked * self.hourlyRate
            monthly_pay = weekly_pay * 4
            return monthly_pay

class CommissionedEmployee(Employee):
    def __init__(self, name, ID, baseSalary, salesAmount, commissionRate):
        super().__init__(name, ID)
        self.baseSalary = baseSalary
        self.salesAmount = salesAmount
        self.commissionRate = commissionRate
        
    #implement the calculatePay()
    def calculatePay (self):
        commission = self.salesAmount * self.commissionRate
        totalPay = self.baseSalary + commission
        return totalPay

totalIncome = [SalariedEmployee("Alice", 1, 9000), HourlyEmployee("Bob", 2, 25, 45), CommissionedEmployee("Charlie", 3, 5000, 20000, 0.1)]
for income in totalIncome:
    print(f"Employee: {income.name}, ID: {income.ID}, Monthly Pay: {income.calculatePay():.2f}")

# Update the name of the first employee
totalIncome[0].name = "Sidra"
print(f"Updated Employee: {totalIncome[0].name}, ID: {totalIncome[0].ID}, Monthly Pay: {totalIncome[0].calculatePay():.2f}")

