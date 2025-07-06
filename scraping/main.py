## Version 1
# import requests

# response = requests.get('https://en.wikipedia.org/wiki/Khabib_Nurmagomedov')
# assert(response.status_code == 200)

# with open('khabib.html', 'w', encoding = 'utf-8') as f:
#     f.write(response.text)
    
# Version 2

import requests
import json
from scraping.wiki_fighter import get_opponent,get_fighter_info,get_opponent_with_info
import sys 

def default():
    if len(sys.argv) == 1:
        raise Exception('missing  argument.......')

    target = sys.argv[1]
    url = sys.argv[2]
    output = sys.argv[3]
    handler = None
    if target == 'ops':
        handler = get_opponent
    elif target == 'ops+info':
        handler = get_opponent_with_info
    elif target == 'info':
        handler = get_fighter_info
        
    response = requests.get(url)

    result = handler(response.text)


    results = json.dumps(result)

    with open(f'{output}.json', 'w', encoding = 'utf-8') as f:
        f.write(results)

