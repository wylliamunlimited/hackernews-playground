import requests
from datetime import datetime
import json
from collections import deque

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


def walk_thread(start_ids: list[int]): 
    '''Traverse function - walking each node and their corresponding kids
    '''
    pass


def longest_comment(story_id: int): 
    '''Traverse function - getting the longest comment thread
    '''

    comments = fetch_item(id=story_id).get('kids', [])
    q = deque((kid, 1) for kid in comments)
    max_depth = 0

    while q: 
        item_id, depth = q.popleft()
        max_depth = max(depth, max_depth)

        data = fetch_item(item_id)
        if data:
            for kid in data.get('kids', []):
                q.append((kid, depth + 1))
    return max_depth

def longest_comment_dfs(story_id: int):

    comments = fetch_item(id=story_id).get('kids', [])

    stack = [(c, 1) for c in comments]
    max_depth = 0
    
    while stack: 
        item_id, depth = stack.pop()

        max_depth = max(depth, max_depth)

        item_data = fetch_item(item_id)
        if item_data:
            for kid in item_data.get('kids', []):
                stack.append((kid, depth + 1))
    return max_depth




def main():
    
    # print(f"Fetching HackerNews Current ({datetime.now().isoformat()}) Max Item...")
    # maxitem_id = fetch_maxitem()
    # print(f"Max Item ID: {maxitem_id}")

    print(f"Fetching top stories ({datetime.now().isoformat()})...")
    ids = fetch_top_stories()
    print(f"IDs fetched: {ids[:5]}")
    print()
    item_data = fetch_item(ids[4])
    
    # for id in ids[:5]: 
    #     print(f"Fetching the details for {id}...")
    #     data = fetch_item(id)
    #     print(f"data: {json.dumps(data, indent=4)}")
    #     print()

    print(f"Fetching the deepest comment depth for {ids[4]} - {item_data.get('title')}...")
    depth, depth_dfs = longest_comment(ids[4]), longest_comment_dfs(story_id=ids[4])
    print(f"For Story {ids[4]} - Deepest Comment at depth = {depth} [BFS] vs {depth_dfs} [DFS]")



if __name__ == "__main__":
    main()
