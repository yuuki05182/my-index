import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
import jpholiday
import json

# 設定ファイル読み込み
with open('yuuki_index_config.json', 'r', encoding='utf-8') as f:
    config = json.load(f)

from datetime import datetime, timedelta
import jpholiday

def get_previous_trading_day(reference_date=None):
    if reference_date is None:
        reference_date = datetime.today()
    for i in range(1, 10):  # 最大9日前まで遡る
        candidate = reference_date - timedelta(days=i)
        if candidate.weekday() < 5 and not jpholiday.is_holiday(candidate):
            return candidate

# 設定値の展開
initial_average = config['initial_average']
base_value = config['base_value']
tickers = config['tickers']
start_date = config['start_date']

print("✅ 設定ファイル読み込み成功")
print("✅ 使用する銘柄:", tickers)
print("✅ 開始日:", start_date)
print("✅ 初期平均値:", initial_average)
print("✅ 基準値:", base_value)

# 最新営業日を取得
def get_latest_trading_day():
    today = datetime.today()
    for i in range(0, 7):
        candidate = today - timedelta(days=i)
        if candidate.weekday() < 5 and not jpholiday.is_holiday(candidate):
            return candidate

# データ取得
end_date = (get_latest_trading_day() + timedelta(days=1)).strftime('%Y-%m-%d')
all_data = {}
for ticker in tickers:
    try:
        df = yf.Ticker(ticker).history(start=start_date, end=end_date)
        all_data[ticker] = df['Close']
        print(f"✅ {ticker} のデータ取得成功（{len(df)}件）")
    except Exception as e:
        print(f"⚠️ {ticker} のデータ取得失敗: {e}")

combined_df = pd.DataFrame(all_data)
combined_df.index.name = 'Date'
combined_df.to_csv('yuuki_index_raw_prices.csv')

# 単純平均 → スケーリング
raw_index = combined_df.mean(axis=1)

# 🔍 ここで確認ログを追加
print("✅ 2021/1/4 の raw_index:", raw_index.loc["2021-01-04"])
print("✅ 設定された initial_average:", initial_average)
print("✅ スケーリング係数:", base_value)

diff = raw_index.loc["2021-01-04"] / initial_average * base_value
print("✅ 2021/1/4 の佑樹指数（計算結果）:", diff)

index_series = raw_index / initial_average * base_value
index_series = index_series.round(2)
index_df = pd.DataFrame({
    'Date': index_series.index.strftime('%Y-%m-%d'),
    'YuukiIndex': index_series.round(2)
})
index_df.to_csv('yuuki_index.csv', index=False)

# JSON生成
latest_date = index_series.index[-1]  # 最新の営業日（datetime型）
previous_date = get_previous_trading_day(latest_date)

latest = index_series.loc[latest_date]
previous = index_series.loc[previous_date]

diff = round(latest - previous, 2)
percent = round((diff / previous) * 100, 2)

diff = round(latest - previous, 2)
percent = round((diff / previous) * 100, 2)
json_data = {
    "dates": index_series.index.strftime('%Y-%m-%d').tolist(),
    "values": index_series.round(2).tolist(),
    "latest_diff": diff,
    "latest_percent": percent,  
    "last_updated": datetime.now().strftime('%Y年%m月%d日 %H:%M:%S')
}

print("✅ 最新日付:", latest_date.strftime('%Y-%m-%d'))
print("✅ 前営業日:", previous_date.strftime('%Y-%m-%d'))
print("✅ 最新値:", latest)
print("✅ 前日値:", previous)
print("✅ 差分:", diff)

with open('yuuki_index.json', 'w', encoding='utf-8') as f:
    json.dump(json_data, f, ensure_ascii=False, indent=2)

# 履歴ファイルに追加
log_entry = {
    "date": latest_date.strftime('%Y-%m-%d'),
    "value": round(latest, 2),
    "diff": diff,
    "percent": percent
}

log_path = 'update_log.json'

try:
    with open(log_path, 'r', encoding='utf-8') as f:
        log_data = json.load(f)
except FileNotFoundError:
    log_data = []

log_data.append(log_entry)

with open(log_path, 'w', encoding='utf-8') as f:
    json.dump(log_data, f, ensure_ascii=False, indent=2)

print("✅ 更新履歴を update_log.json に追加しました。")

print("✅ 佑樹指数を単純平均で更新しました（初期値10000、補正不要）。")
