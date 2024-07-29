# mortgage/amortization.py
import pandas as pd
import matplotlib.pyplot as plt


# creates a plot of interest and principal due each month over the full length of the mortgage
# todo highlight the 50/50 point for principal/interest
# todo years may be a better x axis
def plot_amortization(df: pd.DataFrame):
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.plot(df['Month'], df['Interest Due'], label='Interest Due', color='red')
    ax.plot(df['Month'], df['Principal Due'], label='Principal Due', color='blue')
    ax.set_xlabel('Month')
    ax.set_ylabel('Amount ($)')
    ax.set_title('Amortization Schedule')
    ax.legend()
    return fig
