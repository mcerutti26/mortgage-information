import pandas as pd


# the primary class for the project, storing and calculating the mortgage details
class Mortgage:
    def __init__(self, saleprice, downpayment, rate, length, arm):
        self.saleprice = saleprice
        self.downpayment = downpayment
        self.rate = rate / 100
        self.monthly_rate = self.rate / 12
        self.length = length
        # arm is a boolean, True if the loan is an ARM loan
        self.arm = arm
        self.n_compound = 12 * self.length

    def monthly_payment(self):
        total_payment = (self.saleprice - self.downpayment) * (
                self.monthly_rate * ((1 + self.monthly_rate) ** self.n_compound)) / (
                                ((1 + self.monthly_rate) ** self.n_compound) - 1)
        return total_payment

    # a pandas dataframe to calculate and store the amortization schedule
    def calc_amortization(self):
        df = pd.DataFrame(columns=['Month', 'Interest Due', 'Principal Due'])
        df['Month'] = list(range(1, (self.length * 12) + 1))
        principal = self.saleprice - self.downpayment
        total_monthly_payment = self.monthly_payment()

        for month in range(1, (self.length * 12) + 1):
            interest_payment = principal * self.monthly_rate
            principal_payment = total_monthly_payment - interest_payment
            df.loc[month - 1] = [month, interest_payment, principal_payment]
            principal -= principal_payment
        return df
