
import pandas as pd
import numpy as np
from datetime import datetime

orderbook_data = pd.read_csv('2024-05-01-upbit-BTC-book.csv')
orderbook_data['timestamp'] = pd.to_datetime(orderbook_data['timestamp'])

def truncate(number, digits) -> float:
    stepper = 10.0 ** digits
    return int(number * stepper) / stepper


def cal_total_quantity(gr_bid_level, gr_ask_level):
    total_quantity = gr_bid_level['quantity'].sum() + gr_ask_level['quantity'].sum()
    return total_quantity
    
def cal_mid_price (gr_bid_level, gr_ask_level):
    level = 5 
    if len(gr_bid_level) > 0 and len(gr_ask_level) > 0:
        mid_price = ((gr_bid_level.head(level))['price'].mean() + (gr_ask_level.head(level))['price'].mean()) * 0.5
        return mid_price

def live_cal_book_i_v1(param, gr_bid_level, gr_ask_level, diff, var, mid):
    mid_price = mid
    ratio = param[0]; level = param[1]; interval = param[2]
    _flag = var['_flag']
    if _flag:
        var['_flag'] = False
        return 0.0
    quant_v_bid = gr_bid_level.quantity**ratio
    price_v_bid = gr_bid_level.price * quant_v_bid
    quant_v_ask = gr_ask_level.quantity**ratio
    price_v_ask = gr_ask_level.price * quant_v_ask

    askQty = quant_v_ask.values.sum()
    bidPx = price_v_bid.values.sum()
    bidQty = quant_v_bid.values.sum()
    askPx = price_v_ask.values.sum()
    bid_ask_spread = interval
    book_price = 0
    if bidQty > 0 and askQty > 0:
        book_price = (((askQty*bidPx)/bidQty) + ((bidQty*askPx)/askQty)) / (bidQty+askQty)
    indicator_value = (book_price - mid_price) / bid_ask_spread
    return indicator_value

var = {'_flag': True}
param = [0.2, 5, 1]  # ratio, level, interval
results = []

for timestamp, group in orderbook_data.groupby('timestamp'):
    gr_bid_level = group[group['type'] == 0]
    gr_ask_level = group[group['type'] == 1]
    mid_price = cal_mid_price(gr_bid_level, gr_ask_level)
    book_imbalance = live_cal_book_i_v1(param, gr_bid_level, gr_ask_level, None, var, mid_price)
    total_quantity = cal_total_quantity(gr_bid_level, gr_ask_level)
    results.append([timestamp, mid_price, book_imbalance, total_quantity])
result_df = pd.DataFrame(results, columns=['timestamp', 'mid_price', 'book_imbalance', 'total_quantity'])
result_df.to_csv('orderbook_analysis.csv', index=False, sep='│')
