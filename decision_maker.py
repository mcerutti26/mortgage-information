from _base import Mortgage

if __name__ == '__main__':
    cur_mort = Mortgage(795000,(79500+5000),5.75,30,True)
    pay = cur_mort.monthly_payment()
    print('Your monthly P&I is $' + str(round(pay, 2)) + '.')