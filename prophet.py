from fbprophet import Prophet 

m = Prophet()
eth_m = Prophet()

#BTC
bitcoin_market_info = pd.read_html("https://coinmarketcap.com/currencies/bitcoin/historical-data/?start=20160101&end="+time.strftime("%Y%m%d"))[0]
bitcoin_market_info = bitcoin_market_info.assign(Date=pd.to_datetime(bitcoin_market_info['Date']))
bitcoin_market_info['Volume'] = bitcoin_market_info['Volume'].astype('int64')
bitcoin_market_info.columns = ['Date','bt_Open','bt_High','bt_Low','bt_Close','bt_Volume','bt_MarketCap']


bitcoin_market_info['ds'] = bitcoin_market_info['Date']
bitcoin_market_info['y'] = bitcoin_market_info['bt_Close']


#ETH
eth_market_info = pd.read_html("https://coinmarketcap.com/currencies/ethereum/historical-data/?start=20160101&end="+time.strftime("%Y%m%d"))[0]
eth_market_info = eth_market_info.assign(Date=pd.to_datetime(eth_market_info['Date']))
eth_market_info['Volume'] = eth_market_info['Volume'].astype('int64')
eth_market_info.columns = ['Date','eth_Open','eth_High','eth_Low','eth_Close','eth_Volume','eth_MarketCap']


eth_market_info['ds'] = eth_market_info['Date']
eth_market_info['y'] = eth_market_info['eth_Close']

#Prophet
forecast_data = bitcoin_market_info[['ds', 'y']].copy()
eth_data = eth_market_info[['ds', 'y']].copy()


m.fit(forecast_data)
eth_m.fit(eth_data)

future = m.make_future_dataframe(periods=5, freq='D')


forecast = m.predict(future)
eth_forecast = eth_m.predict(future)

btc_pred = forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail()
eth_pred = eth_forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail()


btc_pred.columns = ['Date','Price Prediction','Lowest Price Prediction','Highest Price Prediction']
eth_pred.columns = ['Date','Price Prediction','Lowest Price Prediction','Highest Price Prediction']

print(btc_pred)
print(eth_pred)
    
