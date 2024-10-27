import requests
import json
import os
from src.config import ALPHA_VANTAGE_API_KEY
from src.logger import logger

CACHE_FILE = 'data/economic_indicators_cache.json'

def get_economic_indicators():
    if os.path.exists(CACHE_FILE):
        with open(CACHE_FILE, 'r') as f:
            cache = json.load(f)
            return cache.get('interest_rate'), cache.get('cpi')

    try:
        interest_rate_url = f'https://www.alphavantage.co/query?function=FEDERAL_FUNDS_RATE&apikey={ALPHA_VANTAGE_API_KEY}&datatype=json'
        response_interest = requests.get(interest_rate_url)
        response_interest.raise_for_status()
        current_interest_rate = response_interest.json().get('data', [{}])[0].get('value')
        
        if current_interest_rate is None:
            logger.error("Interest rate retrieval failed.")

        cpi_url = f'https://www.alphavantage.co/query?function=CPI&apikey={ALPHA_VANTAGE_API_KEY}&datatype=json'
        response_cpi = requests.get(cpi_url)
        response_cpi.raise_for_status()
        current_cpi = response_cpi.json().get('data', [{}])[0].get('value')

        if current_cpi is None:
            logger.error("CPI retrieval failed.")

        # Cache the results
        with open(CACHE_FILE, 'w') as f:
            json.dump({'interest_rate': current_interest_rate, 'cpi': current_cpi}, f)

        return current_interest_rate, current_cpi

    except requests.RequestException as e:
        logger.error(f"Error fetching economic indicators: {e}")
        return None, None
