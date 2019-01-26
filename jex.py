import requests
import json
import pandas as pd
import datetime


def getjexmarket(url):
	infos=requests.get(url).json()
	dt=infos['data']
	BTCMarkets=dt['coinMarkets']['btc']
	USDTMarkets=dt['coinMarkets']['usdt']
	optionMarket=dt['optionMarket']
	BTCM=[{"交易对":x['coinType'],"当前价(元)":x['money'].strip().replace('¥',''),'24h成交量':round(float(x['volume']),0),'24h成交额(万)':round(float(x['money'].strip().replace('¥',''))*float(x['volume'])/10000,0)} for x in BTCMarkets]
	USDM=[{"交易对":x['coinType'],"当前价(元)":x['money'].strip().replace('¥',''),'24h成交量':round(float(x['volume']),0),'24h成交额(万)':round(float(x['money'].strip().replace('¥',''))*float(x['volume'])/10000,0)} for x in USDTMarkets]
	QQQM=[{"交易对":x['coinType'],"当前价(元)":x['money'].strip().replace('¥',''),'24h成交量':round(float(x['volume']),0),'24h成交额(万)':round(float(x['money'].strip().replace('¥',''))*float(x['volume'])/10000,0)} for x in optionMarket]
	JEXM=BTCM+USDM+QQQM
	dt=pd.DataFrame(JEXM)
	return dt

def jexvl():
	NowTime=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
	bb=['jex/btc','eth/btc','ltc/btc','火币ETF','币安ETF','btc/usdt','eth/usdt','BNB/USDT']
	jex=getjexmarket('https://www.jexzh.com/api/v2/pub/index/info?lang=0')

	selfbb=0
	for b in bb:
		selfbb+=float(jex[jex.loc[:,'交易对']==b]['24h成交额(万)'].values[0])

	a=round(sum(jex.iloc[:24,1].values)*0.01+selfbb*0.99,0)
	b=round(sum(jex.iloc[24:,1].values),0)
	c=round((sum(jex.iloc[:24,1].values)-a)/99,0)

	info="过去24小时,\n"+"币币交易额："+str(a)+"万元,\n期权交易额："+str(b)+"万元,\n共享交易额："+str(c)+"万元,\n-----------------------\n"+"故成交总额："+str(a+b+c)+"万元,\nDA By DT."+NowTime
	return info


if __name__ == '__main__':
	print(jexvl())
