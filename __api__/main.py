from my_token import get_token
import igdb_api

token = get_token()
igdb_api.test_req(token)
