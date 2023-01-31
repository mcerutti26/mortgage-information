import pandas as pd


# Mortgage class

class Mortgage:
    def __init__(self, saleprice, downpayment, rate, length, arm):
        self.saleprice = saleprice
        self.downpayment = downpayment
        self.rate = (rate/100)
        self.monthly_rate = self.rate/12
        self.length = length
        self.arm = arm
        self.n_compound = 12*self.length

    def monthly_payment(self):
        total_payment = (self.saleprice-self.downpayment)*(self.monthly_rate*((1+self.monthly_rate)**self.n_compound))/(((1+self.monthly_rate)**self.n_compound)-1)
        return total_payment
    def monthly_interest(self):
        pass
    def monthly_principal(self):
        pass
