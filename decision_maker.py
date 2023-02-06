from _base import Mortgage
import PySimpleGUI as sg

if __name__ == '__main__':
    cur_mort = Mortgage(500000,(60000),6.25,30,True)
    pay = cur_mort.monthly_payment()
    print('Your monthly P&I is $' + str(round(pay, 2)) + '.')
    amoritization_df = cur_mort.calc_amoritization()
    headings = list(amoritization_df.columns)
    values = amoritization_df.values.tolist()
    layout = [[sg.Table(values=values,font=72, headings=headings,key='-TABLE-',expand_x=True,expand_y=True,auto_size_columns=True,justification='center',alternating_row_color='blue')]]
    window = sg.Window('Amoritization Chart', layout, size=(400,400),resizable=True)
    event, value = window.read()
    print(amoritization_df)