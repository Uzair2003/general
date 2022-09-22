# Live FOREX Exchanger
# Uzair

# pip install forex-python
from forex_python.converter import CurrencyRates
from datetime import datetime

# Retrieve the current date and time 
time = datetime.now()
dt_string = time.strftime("%d/%m/%Y %H:%M:%S")

currency = CurrencyRates()

# Print the current exchange rate for the EURO agaisnt multiple other currencies
print("\33[32m-------- Current Rate For 1.0 EUR As Of", dt_string, "--------\33[0m")
countries = ['USD','GBP','JPY','CAD','AUD']
for i in countries:
    print(currency.get_rate('EUR', i), i)
print("\33[32m--------------------------------------------------------------------\n\33[0m")

# Take In User Input 
amount = int(input("Enter An Amount To Convert: "))
from_curr = input("From Currency(e.g. EUR,USD,GBP): ").upper()
to_curr = input("To Currency(e.g. EUR,USD,GBP): ").upper()

# Pass on the 3 inputted variables to be computed
result = currency.convert(from_curr, to_curr, amount)
print("Conversion Amount:", round(result, 3), to_curr)
