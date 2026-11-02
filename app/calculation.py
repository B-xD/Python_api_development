def add(num1: int, num2:int):

    return num1+num2

def subtract(num1: int, num2:int):
    return num1-num2

def multiply(num1: int, num2:int):
    return num1*num2

def divide(num1: int, num2:int):
    return num1/num2

class InsuficientFunds(Exception):
    pass 

class BankAccount():
    def __init__(self, startingbalance=0):
        self.balance = startingbalance

    def deposit(self, amount:int):
        self.balance+=amount 

    def withdrawal(self, amount:int):
        if self.balance < amount:
            raise InsuficientFunds("Insuficient balance")
        self.balance-=amount 

    def collected_interest(self):
        self.balance *= 1.1
    

    