import os, json

def main_rewrite(ifn, ofn, *, ofnmin=None):
    if not os.path.isfile(ifn):
        print('Input file doesn\'t exist')
        input('...')
        exit()
    with open(ifn, encoding="utf-8") as f:
        try:
            json_data = json.loads(f.read())
        except:
            print('Invalid input file')
            input('...')
            exit()
    
    new_games = []
    new_games_min = []
    for game in json_data:
        if 'screenshots' not in game:
            continue

        names = [game['name']]
        if 'alternative_names' in game:
            for i in game['alternative_names']:
                names += [i['name']]
        franchises = [game['franchise']['name']] if 'franchise' in game else []
        if 'franchises' in game:
            for i in game['franchises']:
                if i['name'] not in franchises:
                    franchises += [i['name']]
        screens = []
        for i in game['screenshots']:
            screens += [i['image_id']]
        
        new_games += [{
            'names': names,
            'franchises': franchises,
            'screenshots': screens
        }]
        if ofnmin:
            new_games_min += [{
                'n': names,
                'f': franchises,
                's': screens
            }]

    # print(new_games)
    
    with open(ofn, 'w', encoding="utf-8") as f:
        try:
            f.write(json.dumps(new_games, indent=4, ensure_ascii=False))
        except:
            print('Invalid output data')
            input('...')
            exit()
    
    if ofnmin:
        with open(ofnmin, 'w', encoding="utf-8") as f:
            try:
                f.write(json.dumps(new_games_min, ensure_ascii=False))
            except:
                print('Invalid output data (min)')
                input('...')
                exit()

if __name__ == "__main__":
    main_rewrite('./last_req.json', './api.json')