import yfinance as yf
import pandas as pd
import datetime
import os

# 今日の日付
today = datetime.date.today().strftime('%Y-%m-%d')

# 銘柄コードと基準日株価（例：2020年12月30日）
tickers = {
    '任天堂': '7974.T',
    'NEC': '6701.T',
    'ソニー': '6758.T',
    '富士通': '6702.T',
    'ファーストリテイリング': '9983.T',
    'ダイキン': '6367.T',
    'ニトリ': '9843.T',
    'ユニ・チャーム': '8113.T',
    'ニデック': '6594.T',
    'キーエンス': '6861.T'
}
base_prices = {
    '任天堂': 6250.0,
    'NEC': 4800.0,
    'ソニー': 10200.0,
    '富士通': 14000.0,
    'ファーストリテイリング': 88000.0,
    'ダイキン': 22000.0,
    'ニトリ': 18000.0,
    'ユニ・チャーム': 650.0,
    'ニデック': 13000.0,
    'キーエンス': 65000.0
}

# 最新株価取得と変化率計算
change_rates = []
for name, code in tickers.items():
    data = yf.Ticker(code).history(period='1d')
    if not data.empty:
        current_price = data['Close'].iloc[-1]
        rate = current_price / base_prices[name]
        change_rates.append(rate)

# 佑樹指数の算出（基準値10000）
average_rate = sum(change_rates) / len(change_rates)
yuuki_index = round(10000 * average_rate, 2)

# CSVに追記保存
df = pd.DataFrame([[today, yuuki_index]], columns=['Date', 'YuukiIndex'])
if os.path.exists('yuuki_index.csv'):
    df.to_csv('yuuki_index.csv', mode='a', header=False, index=False)
else:
    df.to_csv('yuuki_index.csv', index=False)

print(f"{today} の佑樹指数（YuukiIndex）: {yuuki_index}")
