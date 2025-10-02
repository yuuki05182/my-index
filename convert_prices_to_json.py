import pandas as pd
import json

# CSV読み込み
df = pd.read_csv('yuuki_index_raw_prices.csv')

# JSON形式に変換（銘柄ごとに配列化）
data = {
    "dates": df['Date'].tolist(),
    "series": []
}

for column in df.columns[1:]:  # 最初の列はDate
    data["series"].append({
        "label": column,
        "data": df[column].where(pd.notnull(df[column]), None).tolist()
    })

# 保存
with open('yuuki_prices.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print("JSONファイルを作成しました。")
