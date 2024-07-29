import PySimpleGUI as sg
from mortgage.fetch_rates import fetch_mortgage_rates
from mortgage.calculator import Mortgage
from mortgage.amortization import plot_amortization
import pandas as pd
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


# Create a GUI for the mortgage calculator with inputs for sale price, down payment, loan type, and loan length and
# outputs for monthly payment and amortization schedule.
def create_gui():
    rates = fetch_mortgage_rates()
    # only able to use the gui if the mortgage rates are available
    if not rates:
        return
    # pysimplegui line by line layout for the mortgage calculator gui
    layout = [
        [sg.Text('Sale Price:'), sg.Input(key='-SALEPRICE-')],
        [sg.Text('Down Payment:'), sg.Input(key='-DOWNPAYMENT-')],
        [sg.Text('Loan Type:'), sg.Combo(list(rates.keys()), key='-LOANTYPE-')],
        [sg.Text('Loan Length (years):'), sg.Input(key='-LENGTH-', default_text='30')],
        [sg.Button('Calculate Monthly Payment', key='-CALCULATE-')],
        [sg.Text('Monthly Payment:'), sg.Text('', key='-MONTHLYPAYMENT-')],
        [sg.Button('Show Amortization Schedule', key='-SHOWSCHEDULE-')],
        [sg.Button('Close', key='-CLOSE-')]
    ]
    window = sg.Window('Mortgage Calculator', layout)
    # loop to read the inputs and calculate the monthly payment and amortization schedule
    # loop only exits when the user closes the window or clicks the close button
    while True:
        event, values = window.read()
        if event in ('-CLOSE-', sg.WIN_CLOSED):
            break
        # calculate and update the monthly payment within the gui
        if event == '-CALCULATE-':
            mortgage = mortgage_from_inputs(values, rates)
            monthly_payment = mortgage.monthly_payment()
            window['-MONTHLYPAYMENT-'].update(f'{monthly_payment:.2f}')
        # calculate and visualize the amortization schedule with a popup window
        if event == '-SHOWSCHEDULE-':
            mortgage = mortgage_from_inputs(values, rates)
            df = mortgage.calc_amortization()
            visualize_dataframe(df)
    window.close()

# helper function to create a mortgage object from the inputs
# this is rerun every time the user requests a mortgage calculation or amortization schedule
def mortgage_from_inputs(values, rates):
    saleprice = float(values['-SALEPRICE-'])
    downpayment = float(values['-DOWNPAYMENT-'])
    loantype = values['-LOANTYPE-']
    rate = float(rates[loantype])
    length = int(values['-LENGTH-'])
    arm = 'arm' in loantype.lower()
    cur_mortgage = Mortgage(saleprice, downpayment, rate, length, arm)
    return cur_mortgage

# helper function to draw the amortization schedule figure
def draw_figure(canvas, figure):
    figure_canvas_agg = FigureCanvasTkAgg(figure, canvas)
    figure_canvas_agg.draw()
    figure_canvas_agg.get_tk_widget().pack(side='top', fill='both', expand=1)
    return figure_canvas_agg


def visualize_dataframe(df: pd.DataFrame):
    layout = [
        [sg.Canvas(key='-CANVAS-')],
        [sg.Button('Export to CSV', key='-CSV-'), sg.Button('Close', key='-CLOSE-')]
    ]
    # create the window with the amortization schedule figure
    window = sg.Window('Amortization Chart', layout, finalize=True, size=(600, 800), resizable=True)
    # get the canvas element and the canvas object
    canvas_elem = window['-CANVAS-']
    canvas = canvas_elem.TKCanvas
    fig = plot_amortization(df)
    draw_figure(canvas, fig)

    while True:
        event, values = window.read()
        if event in ('-CLOSE-', sg.WIN_CLOSED):
            break
        if event == '-CSV-':
            # choose destination for the csv file
            filename = sg.popup_get_file('Save to CSV', save_as=True, no_window=True, default_extension='.csv',
                                         file_types=(("CSV Files", "*.csv"),))
            if filename:
                # write the dataframe to the csv location
                df.to_csv(filename, index=False)
    window.close()
