import requests
from binance.client import Client
import pandas as pd
import MetaTrader5 as mt5
import pandas as pd
import ta
from binance.exceptions import BinanceAPIException
from time import sleep
mt5.initialize(
path,
    login='42126244',
    password='S6BU3c7it5DK'
)

api_key='kNwf6SqhSU2LzdJ1mEg9V8N7utaakjX5R2i78BV9SinixyCPj1Bl4PDYKtPaQLQC'
api_secret='0xESDbSnqO4GpsKGUoiJmlDMdduJTVWmZKjVWjrBUvGiaBoWBw1A9XW1BAkJLvA3'
client = Client(api_key=api_key, api_secret=api_secret)

url = 'https://api.coingecko.com/api/v3/coins/bitcoin/market_chart'
params = {
        'vs_currency': 'usd',
        'days': 3650
    # Retrieve data for 10 years
    }

response = requests.get(url, params=params)
btc_rate=pd.DataFrame.from_dict(response.json())

def dataHandler(URL,**params):
    headers={
    'accept': 'application/json'
}
    response=requests.get(URL,headers=headers,params=params)

    data=pd.DtaFrame.from_dict(response.json())


# Установка необходимых параметров
symbol = "EURUSD"  # Замените на нужную валютную пару
timeframe = mt5.TIMEFRAME_D1  # Замените на нужный таймфрейм
start_time = pd.Timestamp("2007-01-01")  # Замените на нужную начальную дату
end_time = pd.Timestamp("2023-07-01")  # Замените на нужную конечную дату

# Получение исторических данных
rates = mt5.copy_rates_range(symbol, timeframe, start_time, end_time)

# Преобразование данных в DataFrame
df = pd.DataFrame(rates)


# Сохранение данных в CSV файл
filename = f"{symbol}_{timeframe}.csv"
df.to_csv(filename, index=False)

# Завершение подключения к MetaTrader
mt5.shutdown()