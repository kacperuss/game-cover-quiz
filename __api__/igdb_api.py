import requests, os

def test_req(token):
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
            'Client-ID': 'urmk40nw91thaiv607vkigckoxy7my',
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