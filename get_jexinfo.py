# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@Author: DT
@Tool: Sublime Text3&Jupyter Notebook
'''
import requests
import json
import pandas as pd
import datetime


def get_jexmarket(url):
	infos=requests.get(url).json()
	dt=infos['data']
	BTCMarkets=dt['coinMarkets']['btc']
	USDTMarkets=dt['coinMarkets']['usdt']
	optionMarket=dt['optionMarket']
	with open('jex.csv','w') as f:
		f.write('交易对,当前价(元）,24h成交量,24h成交额(万）'+'\n')
	f.close()
	with open('jex.csv','a') as f:
		for x in BTCMarkets:
			BTCM=x['coinType']+','+x['money'].strip().replace('¥','')+','+str(round(float(x['volume']),0))+','+str(round(float(x['money'].strip().replace('¥',''))*float(x['volume'])/10000,0))+'\n'
			f.write(BTCM)

		for y in USDTMarkets:
			USDM=y['coinType']+','+y['money'].strip().replace('¥','')+','+str(round(float(y['volume']),0))+','+str(round(float(y['money'].strip().replace('¥',''))*float(y['volume'])/10000,0))+'\n'
			f.write(USDM)

		for z in optionMarket:
			QQQM=z['coinType']+','+z['money'].strip().replace('¥','')+','+str(round(float(z['volume']),0))+','+str(round(float(z['money'].strip().replace('¥',''))*float(z['volume'])/10000,0))+'\n'
			f.write(QQQM)
	f.close()


if __name__ == '__main__':
	url='https://www.jexzh.com/api/v2/pub/index/info?lang=0'
	get_jexmarket(url)

jex=pd.read_csv('jex.csv',encoding='gb18030')
NowTime=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
jexbtc=jex[jex.loc[:,'交易对']=='jex/btc'].iloc[0,3]
ethbtc=jex[jex.loc[:,'交易对']=='eth/btc'].iloc[0,3]
ltcbtc=jex[jex.loc[:,'交易对']=='ltc/btc'].iloc[0,3]
hbetf=jex[jex.loc[:,'交易对']=='火币ETF'].iloc[0,3]
bnetf=jex[jex.loc[:,'交易对']=='币安ETF'].iloc[0,3]
btcusdt=jex[jex.loc[:,'交易对']=='btc/usdt'].iloc[0,3]
ethusdt=jex[jex.loc[:,'交易对']=='eth/usdt'].iloc[0,3]
bnbusdt=jex[jex.loc[:,'交易对']=='BNB/USDT'].iloc[0,3]
selfbb=jexbtc+ethbtc+ltcbtc+hbetf+bnetf+btcusdt+ethusdt+bnbusdt
a=sum(jex.iloc[:25,-1])*0.02+selfbb*0.98
b=sum(jex.iloc[25:,-1])
c=(sum(jex.iloc[:25,-1])-a)/49
print("过去24小时，Jex平台")
print("币币交易额："+str(a)+'万元')
print("期权交易额："+str(b)+'万元')
print("共享交易额："+str(c)+'万元')
print("-----------------------\n"+"故成交总额："+str(a+b+c)+'万元'+"\nDA By DT."+NowTime)
jex
