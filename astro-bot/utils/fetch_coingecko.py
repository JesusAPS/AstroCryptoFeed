import requests
from utils.format import log_event

def get_coingecko_data(token_id='ethereum'):
    url = f"https://api.coingecko.com/api/v3/simple/price?ids={token_id}&vs_currencies=usd&include_24hr_change=true"
    try:
        response = requests.get(url)
        data = response.json()
        return {
            'token': token_id,
            'price': data[token_id]['usd'],
            'change': data[token_id]['usd_24h_change']
        }
    except Exception as e:
        log_event(f"Error CoinGecko: {e}", "error")
        return None
