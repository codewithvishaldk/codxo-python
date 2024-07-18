import tkinter as tk
from tkinter import ttk
import requests

class CurrencyConverterApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Currency Converter")
        self.geometry("400x250")

        self.api_key = '41c9fd462f9dcf2581011636' 
        self.base_url = 'https://v6.exchangerate-api.com/v6/'

      
        self.create_widgets()
        
       
        self.currencies = self.get_currencies()

    def create_widgets(self):
        self.amount_label = ttk.Label(self, text="Amount:")
        self.amount_label.grid(row=0, column=0, padx=10, pady=10)

        self.amount_entry = ttk.Entry(self, width=15, font=('Helvetica', 12))
        self.amount_entry.grid(row=0, column=1, padx=10, pady=10)

        self.from_currency_label = ttk.Label(self, text="From Currency:")
        self.from_currency_label.grid(row=1, column=0, padx=10, pady=10)

        self.from_currency_combobox = ttk.Combobox(self, values=[], width=12, font=('Helvetica', 12))
        self.from_currency_combobox.grid(row=1, column=1, padx=10, pady=10)

        self.to_currency_label = ttk.Label(self, text="To Currency:")
        self.to_currency_label.grid(row=2, column=0, padx=10, pady=10)

        self.to_currency_combobox = ttk.Combobox(self, values=[], width=12, font=('Helvetica', 12))
        self.to_currency_combobox.grid(row=2, column=1, padx=10, pady=10)

        self.convert_button = ttk.Button(self, text="Convert", command=self.convert_currency)
        self.convert_button.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

        self.result_label = ttk.Label(self, text="", font=('Helvetica', 14, 'bold'))
        self.result_label.grid(row=4, column=0, columnspan=2, padx=10, pady=10)

    def get_currencies(self):
        try:
            response = requests.get(f'{self.base_url}{self.api_key}/codes')
            data = response.json()
            if data['result'] == 'success':
                # Assuming the response is a list of currency codes
                currencies = data.get('supported_codes', [])
                # Populate the comboboxes with currency codes
                currency_codes = [code for code, name in currencies]
                self.from_currency_combobox['values'] = currency_codes
                self.to_currency_combobox['values'] = currency_codes
                self.from_currency_combobox.set('USD')  # Set default value
                self.to_currency_combobox.set('EUR')    # Set default value
                return {code: name for code, name in currencies}
            else:
                self.result_label.config(text="Failed to fetch currency codes.")
                return {}
        except Exception as e:
            self.result_label.config(text=f"Error: {str(e)}")
            return {}

    def convert_currency(self):
        try:
            amount = float(self.amount_entry.get())
            from_currency = self.from_currency_combobox.get().upper()
            to_currency = self.to_currency_combobox.get().upper()

            if from_currency and to_currency:
                conversion_rate = self.get_conversion_rate(from_currency, to_currency)
                if conversion_rate:
                    result = amount * conversion_rate
                    self.result_label.config(text=f"{amount} {from_currency} = {result:.2f} {to_currency}")
                else:
                    self.result_label.config(text="Conversion rate not available.")
            else:
                self.result_label.config(text="Please select currencies.")
        except ValueError:
            self.result_label.config(text="Please enter a valid amount.")

    def get_conversion_rate(self, from_currency, to_currency):
        try:
            response = requests.get(f'{self.base_url}{self.api_key}/latest/{from_currency}')
            data = response.json()
            if data['result'] == 'success':
                return data['conversion_rates'].get(to_currency)
            else:
                self.result_label.config(text="Failed to fetch conversion rate.")
                return None
        except Exception as e:
            self.result_label.config(text=f"Error: {str(e)}")
            return None

if __name__ == "__main__":
    app = CurrencyConverterApp()
    app.mainloop()
