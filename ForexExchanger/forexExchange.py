# Live FOREX Exchanger
# Uzair

from forex_python.converter import CurrencyRates
from datetime import datetime

# Function to print the current exchange rates for a base currency against multiple target currencies
def get_current_exchange_rates(base_currency, target_currencies):

    # Displaying the current time
    print(f"-------- Current Rate For 1.0 {base_currency} As Of {datetime.now().strftime('%d/%m/%Y %H:%M:%S')} --------")
    
    # Iterating through each target currency and printing its exchange rate against the base currency
    for currency in target_currencies:
        rate = currency_rates.get_rate(base_currency, currency)
        print(f"{rate} {currency}")
    print("--------------------------------------------------------------------\n")

# Function to convert a given amount from one currency to another
def convert_currency(amount, from_currency, to_currency):

    return currency_rates.convert(from_currency, to_currency, amount)

# Main function
def main():

    # List of target currencies
    target_currencies = ['USD', 'GBP', 'JPY', 'CAD', 'AUD']
    
    # Displaying current exchange rates for the base currency 'EUR'
    get_current_exchange_rates('EUR', target_currencies)

    # Taking user input for the amount and currency of conversion
    amount = float(input("Enter an amount to convert: "))
    from_currency = input("From Currency (e.g., EUR, USD, GBP): ").upper()
    to_currency = input("To Currency (e.g., EUR, USD, GBP): ").upper()

    # Performing the conversion and displaying the result
    result = convert_currency(amount, from_currency, to_currency)
    print(f"Conversion Amount: {round(result, 3)} {to_currency}")

# Ensures the script runs only when executed directly and not when imported as a module
if __name__ == "__main__":
    currency_rates = CurrencyRates()  
    main() 
