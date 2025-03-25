import requests
import logging
import time
import json
from datetime import datetime, timedelta
import os

# Configure logging
logging.basicConfig(level=logging.INFO)

# Alpha Vantage API key
API_KEY = "613OXF7784P638VD"  # Your API key

# File to store cached exchange rates
CACHE_FILE = "exchange_rates_cache.json"

def get_most_recent_business_day():
    """
    Get the most recent business day (Monday to Friday).
    If today is a weekend, return the last Friday.
    """
    today = datetime.now()
    if today.weekday() >= 5:  # Saturday (5) or Sunday (6)
        today -= timedelta(days=today.weekday() - 4)  # Go back to Friday
    return today.strftime("%Y-%m-%d")

def is_cache_valid(cache_time):
    """
    Check if the cached exchange rates are still valid (until 18:00 New York time).
    """
    now = datetime.now()
    cache_time = datetime.fromisoformat(cache_time)
    # New York time is UTC-4 (EDT) or UTC-5 (EST)
    # Assume New York time is UTC-4 for simplicity (you can adjust this based on daylight saving time)
    new_york_time = now - timedelta(hours=4)
    cache_new_york_time = cache_time - timedelta(hours=4)
    # Check if the cache is from the same day and before 18:00 New York time
    return (cache_new_york_time.date() == new_york_time.date() and
            cache_new_york_time.time() < datetime.strptime("18:00", "%H:%M").time())

def load_cached_rates():
    """
    Load cached exchange rates from the file if they are valid.
    """
    if os.path.exists(CACHE_FILE):
        with open(CACHE_FILE, "r") as file:
            cache = json.load(file)
            if is_cache_valid(cache["timestamp"]):
                logging.info("Using cached exchange rates.")
                return cache["rates"]
    return None

def save_cached_rates(rates):
    """
    Save the fetched exchange rates to the cache file.
    """
    cache = {
        "timestamp": datetime.now().isoformat(),
        "rates": rates
    }
    with open(CACHE_FILE, "w") as file:
        json.dump(cache, file)
    logging.info("Exchange rates cached.")

def get_exchange_rates():
    """
    Fetch exchange rates from Alpha Vantage or use cached rates if valid.
    """
    # Try to load cached rates
    cached_rates = load_cached_rates()
    if cached_rates:
        return cached_rates

    try:
        currencies = ["BRL", "EUR", "CNY"]
        exchange_rates = {"USD": 1.0}
        business_day = get_most_recent_business_day()
        logging.info(f"Fetching exchange rates for {business_day}")

        for currency in currencies:
            url = f"https://www.alphavantage.co/query?function=FX_DAILY&from_symbol=USD&to_symbol={currency}&apikey={API_KEY}"
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            print(f"DEBUG: API Response for {currency}: {data}")

            if "Error Message" in data:
                logging.error(f"Alpha Vantage API error: {data['Error Message']}")
                raise Exception(data["Error Message"])
            if "Note" in data:
                logging.error(f"Alpha Vantage API Note: {data['Note']}")
                raise Exception(data["Note"])

            historical_rates = data.get("Time Series FX (Daily)", {})
            if business_day in historical_rates:
                rate = float(historical_rates[business_day]["4. close"])
                exchange_rates[currency] = rate
            else:
                logging.warning(f"No data available for {business_day} for {currency}. Using fallback rates.")
                exchange_rates[currency] = {"BRL": 5.0, "EUR": 0.90, "CNY": 7.0}[currency]

            time.sleep(1)  # Add a delay to avoid hitting the API rate limit

        logging.info("Successfully fetched exchange rates from Alpha Vantage.")
        save_cached_rates(exchange_rates)  # Save the fetched rates to cache
        return exchange_rates

    except requests.exceptions.RequestException as e:
        logging.error(f"Network error fetching exchange rates: {e}")
        return {"BRL": 5.0, "EUR": 0.90, "CNY": 7.0, "USD": 1.0}
    except Exception as e:
        logging.error(f"Error fetching exchange rates: {e}")
        return {"BRL": 5.0, "EUR": 0.90, "CNY": 7.0, "USD": 1.0}