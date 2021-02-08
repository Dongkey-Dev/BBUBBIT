from bs4 import BeautifulSoup as bs
import requests 
import logging 
import re

headers_Get = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:49.0) Gecko/20100101 Firefox/49.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate',
    'DNT': '1',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1'
    }

logger = logging.getLogger(__name__)        

class WrongHtml(Exception) : 
    def __init__(self):
        super().__init__('Fail to get HTML')

class StockIndicesGetter :
    @staticmethod
    def requestsGet(url) :
        global headers_Get
        s = requests.Session()
        response = s.get(url, headers=headers_Get)
        if response.status_code == 200 : 
            return bs(response.text ,'html.parser')
        else : 
            logger.error("resquest's status code is {}".format(response.status_code))
            raise WrongHtml

    @staticmethod
    def GetStockIndicesMaterialsInvesting() :
        global headers_Get
        s = requests.Session()
        url = 'https://kr.investing.com/commodities/'
        s = StockIndicesGetter.requestsGet(url)
        WTI = s.select('td.pid-8849-last')
        if WTI : 
            WTI = s.select('td.pid-8849-last')[0].text
            WTIMove = s.select('td.pid-8849-pcp')[0].text
            Brent = s.select('td.pid-8833-last')[0].text
            BrentMove = s.select('td.pid-8833-pcp')[0].text
            Gas = s.select('td.pid-8862-last')[0].text
            GasMove = s.select('td.pid-8862-pcp')[0].text
            Gold = s.select('td.pid-8830-last')[0].text
            GoldMove = s.select('td.pid-8830-pcp')[0].text
            Silver = s.select('td.pid-8836-last')[0].text
            SilverMove = s.select('td.pid-8836-pcp')[0].text 
            infomsg = "    [ 원자재 ]\n"
            infomsg+="$WTI유 ("+WTI +' '+WTIMove+")\n"
            infomsg+="$브렌트유 ("+Brent+' ' +BrentMove+")\n"
            infomsg+="$천연가스 ("+Gas+' ' +GasMove+")\n"
            infomsg+="$ 금  ("+Gold+' ' +GoldMove+")\n"
            infomsg+="$ 은  ("+Silver+' ' +SilverMove+")"
            return {"stockName": '원자재',"InfoMsg": infomsg, "querySuccess": True}
        else : 
            return {"stockName": '원자재',"InfoMsg": "Error :{}".format("not found stock"), "querySuccess": False}        

    @staticmethod
    def GetStockIndicesFutureInvesting() :
        global headers_Get
        s = requests.Session()
        url = 'https://kr.investing.com/indices/indices-futures'
        s = StockIndicesGetter.requestsGet(url)
        Nasdaq = s.select('td.pid-8874-last')
        if Nasdaq : 
            Nasdaq = s.select('td.pid-8874-last')[0].text
            NasdaqMove = s.select('td.pid-8874-pcp')[0].text
            SP = s.select('td.pid-8839-last')[0].text
            SPMove = s.select('td.pid-8839-pcp')[0].text
            Dow = s.select('td.pid-8873-last')[0].text
            DowMove = s.select('td.pid-8873-pcp')[0].text
            Hangsang = s.select('td.pid-8984-last')[0].text
            HangsangMove = s.select('td.pid-8984-pcp')[0].text
            VIX = s.select('td.pid-8884-last')[0].text
            VIXMove = s.select('td.pid-8884-pcp')[0].text
            Kospi = s.select('td.pid-8987-last')[0].text
            KospiMove = s.select('td.pid-8987-pcp')[0].text    
            infomsg = "    [ 선물 ]\n"
            infomsg+="$나스닥 ("+Nasdaq+' ' +NasdaqMove+")\n"
            infomsg+="$S&P500 ("+SP+' ' +SPMove+")\n"
            infomsg+="$다우30 ("+Dow+' ' +DowMove+")\n"
            infomsg+="$ VIX  ("+VIX+' ' +VIXMove+")\n"
            infomsg+="$ 항생  ("+Hangsang+' ' +HangsangMove+")\n"
            infomsg+="$코스피 ("+Kospi+' ' +KospiMove+")"
            return {"stockName": '선물',"InfoMsg": infomsg, "querySuccess": True}
        else : 
            return {"stockName": '선물',"InfoMsg": "Error :{}".format("not found stock"), "querySuccess": False}

    @staticmethod
    def GetStockIndicesInvesting() :
        global headers_Get
        s = requests.Session()
        url = 'https://kr.investing.com/indices/major-indices'
        s = StockIndicesGetter.requestsGet(url)
        Nasdaq = s.select('td.pid-14958-last')
        if Nasdaq : 
            Nasdaq = s.select('td.pid-14958-last')[0].text
            NasdaqMove = s.select('td.pid-14958-pcp')[0].text
            SP = s.select('td.pid-166-last')[0].text
            SPMove = s.select('td.pid-166-pcp')[0].text
            Dow = s.select('td.pid-169-last')[0].text
            DowMove = s.select('td.pid-169-pcp')[0].text
            Hangsang = s.select('td.pid-179-last')[0].text
            HangsangMove = s.select('td.pid-179-pcp')[0].text
            VIX = s.select('td.pid-44336-last')[0].text
            VIXMove = s.select('td.pid-44336-pcp')[0].text
            Kospi = s.select('td.pid-37426-last')[0].text
            KospiMove = s.select('td.pid-37426-pcp')[0].text    
            Kosdaq = s.select('td.pid-38016-last')[0].text
            KosdaqMove = s.select('td.pid-38016-pcp')[0].text             
            infomsg = "    [ 선물 ]\n"
            infomsg+="$나스닥 ("+Nasdaq+' ' +NasdaqMove+")\n"
            infomsg+="$S&P500 ("+SP+' ' +SPMove+")\n"
            infomsg+="$다우30 ("+Dow+' ' +DowMove+")\n"
            infomsg+="$ VIX  ("+VIX+' ' +VIXMove+")\n"
            infomsg+="$ 항생  ("+Hangsang+' ' +HangsangMove+")\n"
            infomsg+="$코스피 ("+Kospi+' ' +KospiMove+")\n"
            infomsg+="$코스닥 ("+Kosdaq+' ' +KosdaqMove+")"
            return {"stockName": '지수',"InfoMsg": infomsg, "querySuccess": True}
        else : 
            return {"stockName": '지수',"InfoMsg": "Error :{}".format("not found stock"), "querySuccess": False}