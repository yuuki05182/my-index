import yfinance as yf
import pandas as pd

tickers = {
    'Nintendo': '7974.T',
    'NEC': '6701.T',
    'Sony': '6758.T',
    'Fujitsu': '6702.T',
    'FastRetailing': '9983.T',
    'Daikin': '6367.T',
    'Nitori': '9843.T',
    'Unicharm': '8113.T',
    'Nidec': '6594.T',
    'Keyence': '6861.T'
}

start_date = "2021-01-01"
end_date = "2025-09-26"

price_data = pd.DataFrame()
for name, code in tickers.items():
    df = yf.Ticker(code).history(start=start_date, end=end_date)
    price_data[name] = df['Close']

price_data.index.name = 'Date'
price_data.to_csv('yuuki_index_raw_prices.csv')

print("2021年からの株価履歴を保存しました。")
