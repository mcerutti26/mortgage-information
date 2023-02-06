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
    def calc_amoritization(self):
        # interest = P * (interest rate/compounds per year)
        df = pd.DataFrame()
        df['Month'] = list(range(1,(self.length*12)+1))
        df['Interest Due'] = 0
        df['Principal Due'] = 0
        principal = self.saleprice - self.downpayment
        total_monthly_payment = self.monthly_payment()
        for index, data in df.iterrows():
            cur_interest_payment = principal * (self.rate/12)
            data['Interest Due'] = cur_interest_payment
            cur_principal_payment = total_monthly_payment-cur_interest_payment
            data['Principal Due'] = cur_principal_payment
            principal = principal - cur_principal_payment
        return df
