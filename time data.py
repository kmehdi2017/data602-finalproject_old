import requests
import pandas as pd
import time



def predict():
    spike_date = '20170701'
    
    full_list= pd.DataFrame()
    pre_spike = pd.DataFrame()
    post_spike = pd.DataFrame()
    
    market = requests.get("https://bittrex.com/api/v1.1/public/getmarkets").json()
    marketDF = pd.DataFrame(market['result'])
    marketDF = marketDF.loc[marketDF['BaseCurrency']=='USDT']
    currencies = marketDF[['MarketCurrencyLong']]
    currencies = currencies.replace(' ', '-', regex=True)
    currencies = currencies.replace('Ada', 'Cardano', regex=True)
    currencies = currencies['MarketCurrencyLong'].values.tolist()
    currencies.remove('TrueUSD')
    
    for m in currencies:
        full_market_info = pd.read_html("https://coinmarketcap.com/currencies/"+m+"/historical-data/?start=201501010&end="+time.strftime("%Y%m%d"))[0]
        full_market_info['Volume'] = full_market_info['Volume'].astype('int64')
        full_market_info["Coin"] = m
        full_list = full_list.append(full_market_info, ignore_index=True)
        
    for n in currencies:
        pre_market_info = pd.read_html("https://coinmarketcap.com/currencies/"+n+"/historical-data/?start=201501010&end="+spike_date)[0]
        pre_market_info['Volume'] = pre_market_info['Volume'].astype('int64')
        pre_market_info["Coin"] = n
        pre_spike = pre_spike.append(pre_market_info, ignore_index=True)
        
    for o in currencies:
        post_market_info = pd.read_html("https://coinmarketcap.com/currencies/"+o+"/historical-data/?start="+spike_date+"&end="+time.strftime("%Y%m%d"))[0]
        post_market_info['Volume'] = post_market_info['Volume'].astype('int64')
        post_market_info["Coin"] = o
        post_spike = post_spike.append(post_market_info, ignore_index=True)
    
    return full_list, pre_spike, post_spike
