import yfinance as yf
import matplotlib.pyplot as plt
import pandas as pd

# ✅ 日本語フォント設定（ここに追加）
plt.rcParams['font.family'] = 'IPAexGothic'  # または 'Noto Sans CJK JP'

tickers = [
    "6701.T", "6758.T", "9983.T", "7974.T", "6702.T",
    "6861.T", "6367.T", "9843.T", "8113.T", "6594.T"
]

start_date = "2021-01-04"
end_date = "2025-09-29"

contributions = {}
total_change = 0

ticker_names = {
    "6701.T": "NEC",
    "6758.T": "ソニー",
    "9983.T": "ファストリ",
    "7974.T": "任天堂",
    "6702.T": "富士通",
    "6861.T": "キーエンス",
    "6367.T": "ダイキン工業",
    "9843.T": "ニトリ",
    "8113.T": "ユニ・チャーム",
    "6594.T": "ニデック"
}

labels = [ticker_names.get(t, t) for t in contributions.keys()]

for ticker in tickers:
    df = yf.Ticker(ticker).history(start="2020-12-28", end="2025-10-01")
    if df.empty:
        print(f"⚠️ データが空です: {ticker}")
        contributions[ticker] = 0
        continue

    try:
        # ✅ タイムゾーン付き日付で営業日補正
        import pytz
        tokyo = pytz.timezone("Asia/Tokyo")

        start_dt = pd.to_datetime(start_date).tz_localize(tokyo)
        end_dt = pd.to_datetime(end_date).tz_localize(tokyo)

        nearest_start_idx = df.index.get_indexer([start_dt], method='nearest')[0]
        nearest_end_idx = df.index.get_indexer([end_dt], method='nearest')[0]

        price_start = df.iloc[nearest_start_idx]["Close"]
        price_end = df.iloc[nearest_end_idx]["Close"]

        # ✅ 貢献度計算
        change = (price_end - price_start) / price_start
        contributions[ticker] = change / len(tickers)
        total_change += change / len(tickers)
        print(f"{ticker}: start={price_start:.2f}, end={price_end:.2f}, change={change*100:.2f}%")
    except Exception as e:
        print(f"❌ {ticker} の株価取得エラー: {e}")
        contributions[ticker] = 0 

from matplotlib import font_manager as fm

# ✅ 日本語フォントのパス（環境に応じて変更）
font_path = "C:/Windows/Fonts/YuGothM.ttc"  # Windows例
jp_font = fm.FontProperties(fname=font_path)

# グラフ描画
plt.figure(figsize=(10, 6))

# ✅ 銘柄名変換（安全な方法）
labels = [ticker_names.get(t, t) for t in contributions.keys()]
values = [v * 100 for v in contributions.values()]

print("✅ contributions.keys():", list(contributions.keys()))
print("✅ ticker_names.keys():", list(ticker_names.keys()))

plt.bar(labels, values, color='skyblue')
plt.axhline(y=total_change * 100, color='red', linestyle='--', label=f'合計: {total_change*100:.2f}%')

plt.title("佑樹指数の構成銘柄別貢献度（2021/1/4 → 2025/9/29）", fontproperties=jp_font)
plt.ylabel("貢献度（%）", fontproperties=jp_font)
plt.xlabel("銘柄名", fontproperties=jp_font)
plt.xticks(rotation=30, fontproperties=jp_font)
plt.legend()  # 凡例を描画
legend = plt.gca().get_legend()
for text in legend.get_texts():
    text.set_fontproperties(jp_font)
plt.grid(True)
plt.tight_layout()
plt.show()
