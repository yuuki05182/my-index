import pandas as pd

# ① 生データを読み込む（10銘柄の終値）
df = pd.read_csv('yuuki_index_raw_prices.csv', index_col='Date', parse_dates=True)

# ② 日付ごとの平均値（佑樹指数）を計算
raw_index = df.mean(axis=1)  # 元の平均値（スケーリング前）
index_series = raw_index / raw_index.iloc[0] * 10000  # 初期値10000にスケーリング

# ✅ 初期値を10000にスケーリング
base_value = raw_index.iloc[0]
scaled_index = raw_index / base_value * 10000

# ③ 整形して保存
index_df = pd.DataFrame({
    'Date': index_series.index.strftime('%Y-%m-%d'),
    'YuukiIndex': index_series.round(2)
})

index_df.to_csv('yuuki_index.csv', index=False)

print("✅ yuuki_index.csv を生成しました（佑樹指数の平均値）。")
