import pandas as pd
import json

# CSV読み込み
df = pd.read_csv('yuuki_index.csv')

# 最新日と前日の差分を計算
latest_value = df['YuukiIndex'].iloc[-1]
previous_value = df['YuukiIndex'].iloc[-2]
difference = latest_value - previous_value
percent_change = (difference / previous_value) * 100

# JSON形式に変換
data = {
    "dates": df['Date'].tolist(),
    "values": df['YuukiIndex'].tolist(),
    "latest_diff": round(difference, 2),
    "latest_percent": round(percent_change, 2)
}

# 保存
with open('yuuki_index.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print("JSONファイルを作成しました。")
