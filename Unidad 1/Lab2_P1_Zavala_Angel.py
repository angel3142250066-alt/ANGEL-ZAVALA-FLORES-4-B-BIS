class bankAccount:
    def __init__(self, holder, balance):
        self.holder = holder
        self.__balance = balance


    def deposit(self, amount):
        if amount <= 0:
            print("Deposits less tha zero are not allowed")
        else:
            self.__balance = self.__balance + amount
            print("Successful deposit")

    def withdraw(self, amount):
        if amount > self.__balance:
            print("Deposits more than balance are not allowed")
        else:
            self.__balance = self.__balance - amount
            print("Successful withdraw")            

    def check_balance(self):
        return self.__balance

bankAccount1 = bankAccount("Raul perez", 5000)
bankAccount2 = bankAccount("Joel Lopez", 3000)

#Show the holder's name
print(bankAccount1.holder)
print(bankAccount2.holder)

#Show the actual balance 
print(bankAccount1.check_balance())
print(bankAccount2.check_balance())

#Make a deposit
bankAccount1.deposit(700)

#Make a withdraw
bankAccount2.withdraw(300)

#Show the new balance
print(bankAccount1.check_balance())
print(bankAccount2.check_balance())