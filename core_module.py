import json
import os
from googleapiclient.discovery import build

# 設定
GOOGLE_API_KEY = 'あなたのAPIキー'
CUSTOM_SEARCH_ENGINE_ID = 'あなたのCSE ID'
DATA_FILE = 'data.json'

# Google検索順位（上位10件）取得
def get_search_results(query, num=10):
    service = build('customsearch', 'v1', developerKey=GOOGLE_API_KEY)
    res = service.cse().list(q=query, cx=CUSTOM_SEARCH_ENGINE_ID, num=num).execute()
    results = []
    for idx, item in enumerate(res.get('items', []), 1):
        results.append({
            'rank': idx,
            'title': item.get('title'),
            'link': item.get('link'),
            'snippet': item.get('snippet')
        })
    return results

# data.json を読み込む
def load_data():
    if not os.path.exists(DATA_FILE):
        return {}
    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

# data.json にデータを書き込む
def save_data(data):
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

# 実行例
if __name__ == '__main__':
    query = input('検索キーワード: ')
    results = get_search_results(query)

    data = load_data()
    data[query] = results
    save_data(data)

    print(f'[{query}]で{len(results)}件取得しdata.jsonへ保存しました。')
    for r in results:
        print(f"{r['rank']}位: {r['title']} - {r['link']}")
