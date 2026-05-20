import requests
from datetime import datetime
import json
from collections import deque

BASE_URL = 'https://hacker-news.firebaseio.com/v0'


class Node: 
    id: int 
    author: str
    kids: list
    score: int
    time: int
    type: str


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


def fetch_top_stories(pretty: bool = False) -> list: 
    '''Fetching the top 500 stories through /topstories endpoint 

    Returns: 
        list(int) - List of IDs
    '''

    params = {}
    if pretty: 
        params['print'] = 'pretty'
    
    resp = get(BASE_URL + '/topstories.json', params=params)
    return resp


def walk_thread(start_ids: list(int)): 
    '''Traverse function - walking each node and their corresponding kids
    '''
    pass




def main():
    
    # print(f"Fetching HackerNews Current ({datetime.now().isoformat()}) Max Item...")
    # maxitem_id = fetch_maxitem()
    # print(f"Max Item ID: {maxitem_id}")

    print(f"Fetching top stories ({datetime.now().isoformat()})...")
    ids = fetch_top_stories()
    print(f"IDs fetched: {ids[:5]}")
    print()
    
    for id in ids[:5]: 
        print(f"Fetching the details for {id}...")
        data = fetch_item(id)
        print(f"data: {json.dumps(data, indent=4)}")
        print()


if __name__ == "__main__":
    main()
