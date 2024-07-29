import requests
from config import API_URL
import PySimpleGUI as sg

# Currently, the API is not available. This is a placeholder for when it is.
def fetch_mortgage_rates():
    return {'Fixed': 6, 'ARM': 5.75}
    # todo test the below code once a mortgage rate API is available
    # response = requests.get(API_URL)
    # if response.status_code == 200:
    #     return response.json()
    # else:
    #     sg.popup_error("Failed to fetch mortgage rates.")
    #     return None
