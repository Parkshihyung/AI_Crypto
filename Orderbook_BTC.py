import time
import requests
import pandas as pd
import datetime
from datetime import datetime

while(1):
    book = {}
    response = requests.get("https://api.bithumb.com/public/orderbook/BTC_KRW/?count=5")
    book = response.json()

    data = book['data']
    timestamp_seconds = int(data['timestamp']) / 1000
    time_stamp = datetime.fromtimestamp(timestamp_seconds)

    bids = (pd.DataFrame(data['bids'])).apply(pd.to_numeric,errors='ignore')
    bids.sort_values('price', ascending=False, inplace = True)
    bids = bids.reset_index(); del bids['index']
    bids['type'] = 0 
    bids['timestamp'] = time_stamp
    

    asks =(pd.DataFrame(data['asks'])).apply(pd.to_numeric,errors='ignore')
    asks.sort_values('price', ascending=True, inplace= True)
    asks['type'] = 1
    asks['timestamp'] = time_stamp
    print(bids)
    print(asks)
    time.sleep(4.9)
