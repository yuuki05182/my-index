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
base_value = config['base_value']
tickers = config['tickers']
start_date = config['start_date']

print("✅ 設定ファイル読み込み成功")
print("✅ 使用する銘柄:", tickers)
print("✅ 開始日:", start_date) 
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
# 一括取得
raw_df = yf.download(tickers=tickers, start=start_date, end=end_date, group_by="ticker")

# 終値だけを抽出して整形
close_data = {}
for ticker in tickers:
    try:
        close_data[ticker] = raw_df[ticker]["Close"]
        print(f"✅ {ticker} の終値取得成功（{len(close_data[ticker])}件）")
    except Exception as e:
        print(f"⚠️ {ticker} の終値取得失敗: {e}")

combined_df = pd.DataFrame(close_data)
combined_df.index.name = 'Date'
combined_df.to_csv('yuuki_index_raw_prices.csv')

combined_df.index.name = 'Date'
combined_df.to_csv('yuuki_index_raw_prices.csv')

# 🔍 2025-09-29 の終値が存在するか確認
target_date = "2025-09-29"
missing_on_target = []

for ticker in tickers:
    try:
        value = combined_df.loc[target_date, ticker]
        if pd.isna(value):
            missing_on_target.append(ticker)
    except KeyError:
        missing_on_target.append(ticker)

if missing_on_target:
    print(f"⚠️ {target_date} に欠損している銘柄: {missing_on_target}")
else:
    print(f"✅ {target_date} の全銘柄データが揃っています")

# 単純平均 → スケーリング
raw_index = combined_df.mean(axis=1)

# ✅ 初期平均値を実データから取得（2021年1月4日を基準）
if "2021-01-04" in raw_index.index:
    initial_average = raw_index.loc["2021-01-04"]
else:
    raise ValueError("2021-01-04 のデータが存在しません。佑樹指数の基準値を設定できません。")

# 🔍 ここで確認ログを追加
print("✅ 2021/1/4 の raw_index:", raw_index.loc["2021-01-04"])
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
dates = index_series.index
latest_date = dates[-1]  # 最新の営業日（datetime型）

dates = index_series.index
latest_date = dates[-1]

latest_date = index_series.index[-1]
previous_date = index_series.index[-2]

print(f"✅ 最新日付: {latest_date.strftime('%Y-%m-%d')}")
print(f"✅ 前日付: {previous_date.strftime('%Y-%m-%d')}")

    # 前日データの欠損銘柄を確認
previous_date_str = previous_date.strftime('%Y-%m-%d')
missing_tickers = [ticker for ticker in combined_df.columns if pd.isna(combined_df.loc[previous_date_str, ticker])]

if missing_tickers:
    print(f"⚠️ 前日 {previous_date_str} に欠損している銘柄: {missing_tickers}")
else:
    print(f"✅ 前日 {previous_date_str} の全銘柄データが揃っています")

# 🔧 前日データの欠損数をカウント（confirmed フラグ用）
missing_count = combined_df.loc[previous_date_str].isna().sum()

latest = index_series.loc[latest_date]
previous = index_series.loc[previous_date]

diff = round(latest - previous, 2)
percent = round((diff / previous) * 100, 2)

diff = round(latest - previous, 2)
percent = round((diff / previous) * 100, 2)

from datetime import datetime, timedelta, timezone

jst_now = datetime.now(timezone.utc) + timedelta(hours=9)
formatted_time = jst_now.strftime('%Y年%m月%d日 %H:%M:%S')

json_data = {
    "dates": index_series.index.strftime('%Y-%m-%d').tolist(),
    "values": index_series.round(2).tolist(),
    "latest_diff": diff if diff is not None else None,
    "latest_percent": percent if percent is not None else None,
    "last_updated": formatted_time,
    "confirmed": bool(missing_count == 0)  # 欠損ゼロなら True、欠損ありなら False
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
    "percent": percent,
    "confirmed": bool(missing_count == 0)
}

log_path = 'update_log.json'

try:
    with open(log_path, 'r', encoding='utf-8') as f:
        log_data = json.load(f)
except FileNotFoundError:
    log_data = []

# ✅ すでに同じ日付があるか確認して上書き
log_data = [entry for entry in log_data if entry["date"] != latest_date.strftime('%Y-%m-%d')]
log_data.append(log_entry)

with open(log_path, 'w', encoding='utf-8') as f:
    json.dump(log_data, f, ensure_ascii=False, indent=2)

print("✅ 更新履歴を update_log.json に追加しました。")

print("✅ 佑樹指数を単純平均で更新しました（初期値10000、補正不要）。")
