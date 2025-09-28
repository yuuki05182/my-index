import pandas as pd

# 株価履歴のCSVを読み込み
df = pd.read_csv('yuuki_index_raw_prices.csv')
df.set_index('Date', inplace=True)

# 基準日（2020年12月30日）の株価を設定
base_prices = {
    'Nintendo': 6250.0,
    'NEC': 4800.0,
    'Sony': 10200.0,
    'Fujitsu': 14000.0,
    'FastRetailing': 88000.0,
    'Daikin': 22000.0,
    'Nitori': 18000.0,
    'Unicharm': 650.0,
    'Nidec': 13000.0,
    'Keyence': 65000.0
}

# 初日の倍率平均を取得してスケーリング係数を決定
first_row = df.iloc[0]
first_rates = [first_row[name] / base_prices[name] for name in base_prices if pd.notnull(first_row[name])]
scaling_factor = 10000 / (sum(first_rates) / len(first_rates))

# 佑樹指数を計算
yuuki_index_series = []
for date, row in df.iterrows():
    rates = []
    for name in base_prices:
        if pd.notnull(row[name]):
            rate = row[name] / base_prices[name]
            rates.append(rate)
    if rates:
        avg_rate = sum(rates) / len(rates)
        yuuki_index = round(avg_rate * scaling_factor, 2)
        yuuki_index_series.append((date, yuuki_index))

# 保存
result_df = pd.DataFrame(yuuki_index_series, columns=['Date', 'YuukiIndex'])
result_df.to_csv('yuuki_index.csv', index=False)

print("佑樹指数を再計算して保存しました（初日を10000にスケーリング）。")
