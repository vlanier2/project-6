import requests
from datetime import datetime

def APIinsert(data_dict, api_url):

    result = requests.post(
        api_url, 
        headers={"Content-Type" : "application/json"}, 
        json=data_dict)
    
    return result.json()

def APIdisplay(api_url):
    
    result = requests.get(api_url)
    brevets = result.json()


    if result.status_code != 200 or len(brevets) == 0:
        return {}
    
    last_brevet_saved = brevets[-1]
    last_brevet_saved.pop('_id')
    last_brevet_saved['start_time'] = datetime.utcfromtimestamp(last_brevet_saved['start_time']['$date'] // 1000).isoformat()
    for checkpoint in last_brevet_saved['checkpoints']:
        checkpoint['open_time'] = datetime.utcfromtimestamp(checkpoint['open_time']['$date'] // 1000).isoformat()
        checkpoint['close_time'] = datetime.utcfromtimestamp(checkpoint['close_time']['$date'] // 1000).isoformat()

    return last_brevet_saved