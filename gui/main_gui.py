import PySimpleGUI as sg
from mortgage.fetch_rates import fetch_mortgage_rates
from mortgage.calculator import Mortgage
from mortgage.amortization import plot_amortization
import pandas as pd
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


# Create a GUI for the mortgage calculator with inputs for sale price, down payment, loan type, loan length, and
# outputs for monthly payment and amortization schedule.
def create_gui():
    rates = fetch_mortgage_rates()
    # Only able to use the GUI if the mortgage rates are available.
    if not rates:
        return

    # Convert rates dictionary to list of strings for the default rate display
    latest_rate = next(iter(rates.values()))

    # PySimpleGUI line by line layout for the mortgage calculator GUI
    layout = [
        [sg.Text('Sale Price:'), sg.Input(key='-SALEPRICE-')],
        [sg.Text('Down Payment:'), sg.Input(key='-DOWNPAYMENT-')],
        [sg.Text('Loan Type:'), sg.Combo(list(rates.keys()), key='-LOANTYPE-', enable_events=True)],
        [sg.Text('Rate (%):'), sg.Input(key='-RATE-', default_text=latest_rate)],
        [sg.Text('Loan Length (years):'), sg.Input(key='-LENGTH-', default_text='30')],
        [sg.Button('Calculate Monthly Payment', key='-CALCULATE-')],
        [sg.Text('Monthly Payment:'), sg.Text('', key='-MONTHLYPAYMENT-')],
        [sg.Button('Show Amortization Schedule', key='-SHOWSCHEDULE-')],
        [sg.Button('Close', key='-CLOSE-')]
    ]
    window = sg.Window('Mortgage Calculator', layout)

    # Loop to read the inputs and calculate the monthly payment and amortization schedule.
    # Loop only exits when the user closes the window or clicks the close button.
    while True:
        event, values = window.read()
        if event in ('-CLOSE-', sg.WIN_CLOSED):
            break
        # Update the rate text box when a loan type is selected
        if event == '-LOANTYPE-':
            selected_loan_type = values['-LOANTYPE-']
            if selected_loan_type in rates:
                window['-RATE-'].update(f'{rates[selected_loan_type]:.2f}')
        # Calculate and update the monthly payment within the GUI.
        if event == '-CALCULATE-':
            mortgage = mortgage_from_inputs(values)
            monthly_payment = mortgage.monthly_payment()
            window['-MONTHLYPAYMENT-'].update(f'{monthly_payment:.2f}')
        # Calculate and visualize the amortization schedule with a popup window.
        if event == '-SHOWSCHEDULE-':
            mortgage = mortgage_from_inputs(values)
            df = mortgage.calc_amortization()
            visualize_dataframe(df)
    window.close()


# Helper function to create a mortgage object from the inputs.
# This is rerun every time the user requests a mortgage calculation or amortization schedule.
def mortgage_from_inputs(values):
    saleprice = float(values['-SALEPRICE-'])
    downpayment = float(values['-DOWNPAYMENT-'])
    rate = float(values['-RATE-'])
    length = int(values['-LENGTH-'])
    loantype = values['-LOANTYPE-']
    arm = 'arm' in loantype.lower()
    cur_mortgage = Mortgage(saleprice, downpayment, rate, length, arm)
    return cur_mortgage


# Helper function to draw the amortization schedule figure.
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
    # Create the window with the amortization schedule figure.
    window = sg.Window('Amortization Chart', layout, finalize=True, size=(600, 800), resizable=True)
    # Get the canvas element and the canvas object.
    canvas_elem = window['-CANVAS-']
    canvas = canvas_elem.TKCanvas
    fig = plot_amortization(df)
    draw_figure(canvas, fig)

    while True:
        event, values = window.read()
        if event in ('-CLOSE-', sg.WIN_CLOSED):
            break
        if event == '-CSV-':
            # Choose destination for the CSV file.
            filename = sg.popup_get_file('Save to CSV', save_as=True, no_window=True, default_extension='.csv',
                                         file_types=(("CSV Files", "*.csv"),))
            if filename:
                # Write the dataframe to the CSV location.
                df.to_csv(filename, index=False)
    window.close()