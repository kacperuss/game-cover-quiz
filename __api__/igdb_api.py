import requests, json


def generate_static_api_iter(token, cid, max_requests, max_games_per_req):
    all_data = []
    last_rating = 999999
    for i in range(max_requests):
        json_data = get_api_json(token, cid, max_games_per_req, None if i == 0 else last_rating)
        last_rating = json_data[-1]['rating_count']
        all_data += json_data
        print(f'Request {i+1} finished')
    
    with open('./api_iter.json', 'w', encoding="utf-8") as f:
        try:
            f.write(json.dumps(all_data, ensure_ascii=False))
        except:
            print('API iter - Failed JSON dump to file')
            input('...')
            exit()


def get_api_json(token, cid, max_games, max_rating_count=None):
    try:
        return json.loads(base_api_req(token, cid, max_games, max_rating_count))
    except:
        print('API to JSON - JSON parse failed, returning empty list')
        return []


def generate_static_api(token, cid, max_games):
    content = base_api_req(token, cid, max_games)

    with open('./last_req.json', 'wb') as f:
        f.write(content)


def base_api_req(token, cid, max_games, max_rating_count=None):
    rating = f' & rating_count < {int(max_rating_count)}' if max_rating_count else ''
    response = requests.post(
        'https://api.igdb.com/v4/games',
        f'fields name, rating_count, screenshots.image_id, alternative_names.name, franchises.name, franchise.name, version_title; \
            where rating_count > 1 & category = 0{rating}; \
            sort rating_count desc; \
            limit {int(max_games)};', 
        headers={
            'Authorization': f'Bearer {token}',
            'Client-ID': cid,
        }
    )
    if response.status_code != 200:
        print(f'API - Request error: {response.status_code}')
        input('...')
        exit()
    
    return response.content


def test_req(token, cid):
    response = requests.post(
        'https://api.igdb.com/v4/games',
        # 'https://api.igdb.com/v4/artworks',
        # 'https://api.igdb.com/v4/screenshots',
        # 'https://api.igdb.com/v4/characters',
        # 'fields name, rating_count; where rating_count > 1; sort rating_count desc; limit 200;',
        # 'fields name, rating_count, screenshots.url; where rating_count < 500; sort rating_count desc; limit 20;',
        'fields name, rating_count, alternative_names.comment, screenshots.image_id, alternative_names.name, franchises.name, franchise.name, version_title; \
            where rating_count > 1 & category = 0; \
            sort rating_count desc; \
            limit 20;',
        # 'fields *;',
        headers={
            'Authorization': f'Bearer {token}',
            'Client-ID': cid,
        }
    )
    if response.status_code != 200:
        print(f'API - Request error: {response.status_code}')
        input('...')
        exit()

    content = response.content
    content = content.replace(b'//images', b'http://images').replace(b't_thumb', b't_1080p')

    with open('./last_req.json', 'wb') as f:
        f.write(content)
    pass