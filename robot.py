import MetaTrader5 as mt5
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from indicators import calculate_rsi
mt5.initialize()
def get_position(symbol):
    position = mt5.positions_get(symbol=symbol)
    if position:
        return position[0]
    else:
        return None

# Вход в позицию
def enter_position(symbol, trade_type):
    if trade_type == 'buy':
        result = mt5.order_send(...)
        # Здесь добавьте код для отправки ордера на покупку
    elif trade_type == 'sell':
        result = mt5.order_send(...)
        # Здесь добавьте код для отправки ордера на продажу

    if result.retcode != mt5.TRADE_RETCODE_DONE:
        print(f"Ошибка при открытии позиции: {result.comment}")

# Выход из позиции
def exit_position(position):
    result = mt5.order_send(...)
    # Здесь добавьте код для отправки ордера на закрытие позиции

    if result.retcode != mt5.TRADE_RETCODE_DONE:
        print(f"Ошибка при закрытии позиции: {result.comment}")
# Основная стратегия
def run_strategy(symbol):
    # Получите данные для анализа (например, цены закрытия)
    prices = mt5.copy_rates_from_pos(symbol, mt5.TIMEFRAME_D1, 0, 100)

    # Рассчитайте RSI
    rsi = calculate_rsi(prices)

    # Определите условия входа в позицию и выхода из нее на основе RSI
    if rsi[-1] < 30:
        if get_position(symbol) is None:
            enter_position(symbol, 'buy')
    elif rsi[-1] > 70:
        position = get_position(symbol)
        if position is not None:
            exit_position(position)


# Запуск стратегии


# Получение исторических данных
symbol = "EURUSD"
timeframe = mt5.TIMEFRAME_D1
start_time = pd.Timestamp("2022-01-01")
end_time = pd.Timestamp("2022-12-31")

rates = mt5.copy_rates_range(symbol, timeframe, start_time, end_time)

df = pd.DataFrame(rates)
df['time'] = pd.to_datetime(df['time'], unit='s')

X = df[['open', 'high', 'low', 'close']]
y = df['target']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = LogisticRegression()
model.fit(X_train, y_train)

signals = model.predict(X_test)

lot_size = 5  # Установите размер лота на основе вашего требования

current_position = 0
for i in range(len(signals)):
    if signals[i] == 1 and current_position != 1:
        current_position = 1

    elif signals[i] == -1 and current_position != -1:
        current_position = -1  # Обновите текущую позицию

    elif signals[i] == 0 and current_position != 0:  # Сигнал на закрытие текущей позиции

        current_position = 0  # Обновите текущую позици
symbol = ["EURUSD"]
run_strategy(symbol)
mt5.shutdown()
