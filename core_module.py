import csv
import json
import os
from googleapiclient.discovery import build

# secret.csvから認証情報読取
def load_secrets(filename='secret.csv'):
    with open(filename, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        row = next(reader)
        return row['GOOGLE_API_KEY'], row['CUSTOM_SEARCH_ENGINE_ID']

DATA_FILE = 'data.json'

def get_search_results(query, num=10, api_key='', cse_id=''):
    service = build('customsearch', 'v1', developerKey=api_key)
    res = service.cse().list(q=query, cx=cse_id, num=num).execute()
    results = []
    for idx, item in enumerate(res.get('items', []), 1):
        results.append({
            'rank': idx,
            'title': item.get('title'),
            'link': item.get('link'),
            'snippet': item.get('snippet')
        })
    return results

def load_data():
    if not os.path.exists(DATA_FILE):
        return {}
    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_data(data):
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

if __name__ == '__main__':
    api_key, cse_id = load_secrets()
    query = input('検索キーワード: ')
    results = get_search_results(query, api_key=api_key, cse_id=cse_id)

    data = load_data()
    data[query] = results
    save_data(data)

    print(f'[{query}]で{len(results)}件取得しdata.jsonへ保存しました。')
    for r in results:
        print(f"{r['rank']}位: {r['title']} - {r['link']}")
