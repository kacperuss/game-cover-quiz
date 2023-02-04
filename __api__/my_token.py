import requests, json, os
from datetime import datetime

now = lambda: int(datetime.timestamp(datetime.now()))

def get_token():
    if os.path.isfile('./token.json'):
        with open('./token.json') as f:
            try:
                json_data = json.loads(f.read())
                if json_data['date'] > now():
                    return json_data['access_token'], json_data['client_id']
                print('token.json expired')
            except:
                print('Invalid token.json')
    
    if not os.path.isfile('./twitch_api_keys.json'):
        print('twitch_api_keys.json missing. Refer to [https://api-docs.igdb.com/#account-creation] and [./__twitch_api_keys__template.json]')
        input('...')
        exit()

    cid = ''
    with open('./twitch_api_keys.json') as f:
        print('Requesting new token')
        try:
            json_data = json.loads(f.read())
            response = requests.post('https://id.twitch.tv/oauth2/token', {
                'client_id': json_data['client_id'],
                'client_secret': json_data['client_secret'],
                'grant_type': 'client_credentials',
            })
            cid = json_data['client_id']
        except:
            print('Invalid twitch_api_keys.json')
    if response.status_code != 200:
        print(f'Token - Request error: {response.status_code}')
        input('...')
        exit()
    
    response = response.json()
    response['date'] = now() + response['expires_in']
    response['client_id'] = cid
    with open('./token.json', 'w') as f:
        f.write(json.dumps(response))
    return response['access_token'], cid
