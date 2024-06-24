from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json

from investing.models import ActiveCoin


def upload_coins_to_db():
    """ Скачивание CoinMarketCup MAP в базу данных """

    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/map'
    parameters = {
        'CMC_PRO_API_KEY': '***',
        'limit': 21, # количество криптокоинов
        'sort': 'cmc_rank', # сортировка по рангу (стоимости по market_capitalize)
        'aux': 'is_active' # дополнительные поля для коина в ответе
    }
    headers = {
        'Accepts': 'application/json'
    }

    session = Session()
    session.headers.update(headers)

    try:
        response = session.get(url, params=parameters)
        data = json.loads(response.text)
    except (ConnectionError, Timeout, TooManyRedirects) as e:
        data = None
        return False
    else:
        if data:
            for coin in data['data']:
                try:
                    model = ActiveCoin(
                        id_in_cmc = coin['id'],
                        name = coin['name'],
                        symbol = coin['symbol'],
                        rank = coin['rank'],
                        is_active = coin['is_active']
                    )
                except:
                    print('ERROR')
                    break
                else:
                    try:
                        model.save()
                    except:
                        continue
            return True
        else:
            return False


def get_coins_data():
    """ Данные по определенным коинам через запрос для view контроллера """

    coins_id = ''  # для формирования json
    coins_models = ActiveCoin.objects.all()  # База cmc map для запроса более детальной инфы именно по этим коинам
    for coin in coins_models:
        coins_id += f',{coin.id_in_cmc}'
    coins_id = coins_id[1:]

    url = 'https://pro-api.coinmarketcap.com/v2/cryptocurrency/quotes/latest'
    parameters = {
        'CMC_PRO_API_KEY': '012a80e9-77f8-42a3-a371-09ccb9a29578',
        'id': coins_id
    }
    headers = {
        'Accepts': 'application/json'
    }

    session = Session()
    session.headers.update(headers)

    try:
        response = session.get(url, params=parameters)
        data = json.loads(response.text)
        
        # with open('cmc_map.txt', 'r') as file:
        #     response = file.read()
        #     data = json.loads(response)
        # print("test")
    except (ConnectionError, Timeout, TooManyRedirects) as e:
        data = None
        return None
    else:
        coins_data = []
        if data['status']['error_code'] == 0:
            try:
                for coin_id in data['data']:
                    coin = data['data'][coin_id]
                    coins_data.append({
                        'id': coin['id'],
                        'name': coin['name'],
                        'symbol': coin['symbol'],
                        'date_added': coin['date_added'][0:10],
                        'rank': coin['cmc_rank'],
                        'quote_currency': 'USD',
                        'price': round(coin['quote']['USD']['price'], 2),
                        'percent_1h': round(coin['quote']['USD']['percent_change_1h'], 2),
                        'percent_24h': round(coin['quote']['USD']['percent_change_24h'], 2),
                        'percent_7d': round(coin['quote']['USD']['percent_change_7d'], 2),
                        'market_cap': round(coin['quote']['USD']['market_cap'], 2)
                    })
            except:
                return None
            else:
                return tuple(coins_data)
        else:
            return None





