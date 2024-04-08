from flask import Flask,request
import numpy as np
import pandas as pd
import yfinance as yf
from ta.momentum import RSIIndicator as rrsi
from ta.volatility import AverageTrueRange as atrds
import numpy as np
import pandas as pd
from pandas import DataFrame as df
from ta.volume import MFIIndicator as mfi
from ta.volume import OnBalanceVolumeIndicator as Obv
from ta.trend import EMAIndicator as ema 
from ta.trend import MACD as mov 
from pandas import DataFrame as df
from flask_cors import CORS
app = Flask(__name__)
CORS(app)
@app.route("/pythonapi",methods = ["POST","GET"])
def getvalue():
   da = request.json["postt"]   
   input_data = da
   coins = {'USD_coins': {0: 'BTC-USD', 1: 'ETH-USD', 2: 'BNB-USD', 3: 'XRP-USD', 4: 'SOL-USD', 
                          5: 'STETH-USD', 6: 'ADA-USD', 7: 'DOGE-USD', 8: 'TRX-USD', 9: 'WTRX-USD', 
                          10: 'LINK-USD', 11: 'AVAX-USD', 12: 'MATIC-USD', 13: 'DOT-USD', 14: 'WBTC-USD', 
                          15: 'DAI-USD', 16: 'LTC-USD', 17: 'SHIB-USD', 18: 'BCH-USD', 19: 'OKB-USD', 
                          20: 'ATOM-USD', 21: 'XLM-USD', 22: 'TUSD-USD', 23: 'XMR-USD', 24: 'KAS-USD', 
                          25: 'ETC-USD', 26: 'CRO-USD', 27: 'LDO-USD', 28: 'FIL-USD'}}
   cod = {'Coins':[],'Price':[],'RSI':[],'ATR':[],'EMA':[],'MFI':[],'MACD':[]}
   priority = {"RSI":1,"ATR":2,"MFI":3,"MACD":4}
   Indicator = list(input_data.keys())
   def Sort_Ind(Indicator_value):
       sort = sorted(Indicator_value,key=lambda x: priority.get(x,float('inf')))
       return sort
   sorted_indicator = Sort_Ind(Indicator)
   coin_length = len(coins)
   for i in range(0,coin_length):
        coin_name = coins['USD_coins'][i]
        ticker = yf.Ticker(coin_name)
        data = ticker.history(period='500h',interval='1h').tail(500)
        R_S  =  rrsi(close=data['Close'],window=14,fillna=False)
        Rsi_499 = R_S.rsi()
        atr = atrds(high=data['High'],low = data['Low'],close=data['Close'], window= 14,fillna= False)
        Atr_499 = atr.average_true_range()
        EMA = ema(close=data['Close'], window= 14,fillna= False)
        Ema_499 = EMA.ema_indicator()
        Money_FI =  mfi(high=data['High'],low=data['Low'],close=data['Close'],volume=data['Volume'],window=14,fillna=False)
        Mfi_499 = Money_FI.money_flow_index()
        Mov_aver_Conv_Div =  mov(close=data['Close'], window_slow=26, window_fast=12, window_sign= 9, fillna = False)
        temp_macd = Mov_aver_Conv_Div.macd()
        temp_diff = Mov_aver_Conv_Div.macd_diff()
        temp_signal = Mov_aver_Conv_Div.macd_signal()   
       # On_Balance_Vol = Obv(close=data['High'],volume=data['Close'],fillna=False)
       # Obv_499 = On_Balance_Vol.on_balance_volume()
        #cod['OBV'].append(Obv_499.iloc[-1])
        cod['RSI'].append(round(Rsi_499.iloc[-1],2))
        cod['ATR'].append(round(Atr_499.iloc[-1],4))
        cod['EMA'].append(round(Ema_499.iloc[-1],4))
        cod['MFI'].append(round(Mfi_499.iloc[-1],3))
        cod['Coins'].append(coin_name)
        cod['MACD'].append(round(temp_macd.iloc[-1],4))
        cod['Price'].append(round(data['Close'].iloc[-1],4))
   output = df(cod)
   if(sorted_indicator!=0):
    ascending_dict = [False]*len(sorted_indicator)
    output_sorted = output.sort_values(by=sorted_indicator, ascending=ascending_dict)
   else:
    output_sorted = output.sort_values(by=['RSI'], ascending=[False, False])  
   result = output_sorted.iloc[:15].to_dict(orient='records')
   print(result)
   return result
@app.route("/api",methods = ["GET"])
def api():
    return "Done Done..."
if __name__ == "__main__":
    app.run(host="0.0.0.0",port=5000)