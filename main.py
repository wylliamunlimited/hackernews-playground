import requests
from datetime import datetime
import json

BASE_URL = 'https://hacker-news.firebaseio.com/v0'


def get(url: str, params: dict = {}) -> dict: 
    '''Get request helper function'''
    resp = requests.get(url, params=params)
    resp.raise_for_status()
    return resp.json()


def fetch_item(id: str, pretty: bool = False) -> dict: 
    '''Fetching item through /item/<id>.json

    Returns:
        dict - details of the fetched item
    '''

    params = {}
    if pretty:
        params['print'] = 'pretty'
    
    resp = get(BASE_URL + f'/item/{id}.json')
    return resp


def fetch_maxitem(pretty: bool = False) -> int: 
    '''Fetching Maximum Item through /maxitem.json endpoint

    Returns:
        int - ID of the max item
    '''

    params = {}
    if pretty: 
        params['print'] = 'pretty'
    
    resp = get(BASE_URL + '/maxitem.json', params=params)
    return resp


def main():
    
    print(f"Fetching HackerNews Current ({datetime.now().isoformat()}) Max Item...")
    maxitem_id = fetch_maxitem()
    print(f"Max Item ID: {maxitem_id}")
    print(f"Fetching the details for {maxitem_id}...")
    data = fetch_item(maxitem_id)
    print(f"data: {json.dumps(data, indent=4)}")


if __name__ == "__main__":
    main()
