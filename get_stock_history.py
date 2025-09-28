import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
import jpholiday

def get_latest_trading_day():
    today = datetime.today()
    for i in range(0, 7):
        candidate = today - timedelta(days=i)
        if candidate.weekday() < 5 and not jpholiday.is_holiday(candidate):
            return candidate

# 銘柄コード（東証銘柄は .T を付ける）
tickers = [
    '7974.T',  # 任天堂
    '6701.T',  # NEC
    '6758.T',  # ソニー
    '6702.T',  # 富士通
    '9983.T',  # ファーストリテイリング
    '6367.T',  # ダイキン
    '9843.T',  # ニトリ
    '8113.T',  # ユニ・チャーム
    '6594.T',  # ニデック
    '6861.T'   # キーエンス
]

# 取得期間
start_date = "2021-01-01"
end_date = (get_latest_trading_day() + timedelta(days=1)).strftime('%Y-%m-%d')

# データ取得
all_data = {}
for ticker in tickers:
    df = yf.Ticker(ticker).history(start=start_date, end=end_date)
    all_data[ticker] = df['Close']
print(f"{ticker}: 最終日 = {df.index[-1].strftime('%Y-%m-%d')}")

# データを1つのDataFrameに統合
combined_df = pd.DataFrame(all_data)
combined_df.index.name = 'Date'

# 保存
combined_df.to_csv('yuuki_index_raw_prices.csv')

print("株価履歴を取得して保存しました。")
