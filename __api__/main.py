from my_token import get_token
import igdb_api
import json_rewrite

def main():
    token, cid = get_token()
    igdb_api.generate_static_api_iter(token, cid, 10, 500)
    json_rewrite.main_rewrite('./api_iter.json', './api.json', ofnmin='./api.min.json')

if __name__ == "__main__":
    main()