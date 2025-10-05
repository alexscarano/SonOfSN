import requests

async def fetch_price():
    # Pega o preço atual e a variação de 24h do Bitcoin
    url = "https://api.coingecko.com/api/v3/coins/bitcoin"
    request = requests.get(url)

    if request is None or request.status_code != 200:
        return False 

    response = request.json()
    
    price = response["market_data"]["current_price"]["usd"]
    priceInBrl = response["market_data"]["current_price"]["brl"]
    change_24h = response["market_data"]["price_change_percentage_24h"]

    return price, priceInBrl, change_24h