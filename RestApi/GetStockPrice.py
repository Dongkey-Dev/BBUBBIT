from bs4 import BeautifulSoup as bs
import requests 
import logging 
import re
"""
1. 먼저 국장에서 찾아보고
2. 없으면 구글
"""
# Create your views here.

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

class StockGetter :
    @staticmethod
    def isHangul(text):
        hanCount = len(re.findall(u'[\u3130-\u318F\uAC00-\uD7A3]+', text))
        return hanCount > 0

    @staticmethod
    def requestsGet(url) :
        global headers_Get
        s = requests.Session()
        response = s.get(url, headers=headers_Get)
        if response.status_code == 200 : 
            return response.text 
        else : 
            logger.error("resquest's status code is {}".format(response.status_code))
            raise WrongHtml

    @staticmethod
    def isKrStock(stockName) : 
        global headers_Get
        paxnet = 'http://www.paxnet.co.kr/search/jongmok?kwd=' + stockName 
        logger.debug('paxnet URL is {}'.format(paxnet))
        s = requests.Session()
        response = s.get(paxnet, headers=headers_Get)
        s = bs(response.text, 'html.parser')
        code = response.text.split('value="')[2][:6]
        if code.isnumeric() : 
            return StockGetter.GetStockNaver(stockName, code)
        if s.select('input[name=searchSymbol]') and  s.select('strong') : 
            code = s.select('input[name=searchSymbol]')[0]['value']
            if not code.isnumeric() : 
                GetStockGoogle(stockName)
            stockName = s.select('strong')[0].text
            return StockGetter.GetStockNaver(stockName, code)
        else : 
            return StockGetter.GetStockGoogle(stockName)

    @staticmethod
    def GetStockNaver(stockName, code) : 
        try : 
            global headers_Get
            logger.debug('recieved StockName = {}'.format(stockName + ' ' + code))
            s = requests.Session()
            url = "https://polling.finance.naver.com/api/realtime?query=SERVICE_ITEM:" + code
            response = s.get(url, headers=headers_Get)
            html = response.text
            header = response.headers 
            status = response.status_code
            if status != 200 : 
                print('requests error')
                return 0
            if not html.split('nm":"') :
                return {"stockName": stockName,"InfoMsg": "Error {}".format("not found stock")}
            stockName = html.split('nm":"')[1].split('","sv"')[0]
            nv = html.split('nv":')[1].split(',"cv"')[0]
            sv = html.split('sv":')[1].split(',"nv"')[0]
            cv = html.split('cv":')[1].split(',"cr"')[0]
            cr = html.split('cr":')[1].split(',"rf"')[0]
            if (float(nv) > float(sv)) :
                cv = '+'+cv
            else :
                cv = '-'+cv
            msg = "[ " + stockName + " ]  \n" +"KRW" + nv + ", " + cv+ '  (' + cr + '%)'

            return {"stockName": stockName,"InfoMsg": msg, "querySuccess": True,"isKR":True}
        except Exception as e : 
            return {"stockName": stockName,"InfoMsg": "Error {}".format(e), "querySuccess": False}

    @staticmethod
    def GetStockGoogle(stockName) :
        # global headers_Get
        logger.debug('recieved StockName = {}'.format(stockName))
        s = requests.Session()
        url = 'https://www.google.com/search?q='+stockName+'+stock'
        response = s.get(url,  headers=headers_Get)
        html = response.text

        s = bs(html,'html.parser')
        if s.select('div.oPhL2e') : 
            stockName = s.select('div.oPhL2e')[0].text.strip()
            stockMoney = s.select('span.knFDje')[0].text.strip()
            Exchange = s.select('div.HfMth')[0].text.strip()
            Price = s.select('span[jsname=vWLAgc]')[0].text.strip()
            Date = s.select('span[jsname=ihIZgd]')[0].text.strip()
            Move = s.select('span[jsname=qRSVye]')[0].text.strip()
            Percentage = s.select('span[jsname=rfaVEf]')[0].text.strip()
            if s.select('span[jsname=wurNO]') :
                PaPrice = s.select('span[jsname=wurNO]')[0].text.strip()
                PaMove = s.select('span[jsname=TmYleb]')[0].text.strip()
                PaPercentage = s.select('span[jsname=sam3Lb]')[0].text.strip()
                Dividend = s.select('td.iyjjgb')[4].text.strip()
                infomsg = "[" + stockName +"]" + "\n" + Exchange + "\n" + "[" + Date+"]" + "\n" + stockMoney +" "+ Price + ", " + Move+Percentage +"\n" +       "[ Pre & After Market ]" + "\n" + stockMoney + PaPrice +", "+ PaMove + PaPercentage + "\n" + "[ Dividend yield ] : " + Dividend + "\n"
            else :
                infomsg = "[" + stockName +"]" + "\n" + Exchange + "\n" + "[" + Date+"]" + "\n" + stockMoney +" "+ Price + ", " + Move+Percentage +"\n" + "[ Dividend yield ] : " + Dividend + "\n"

            return {"stockName": stockName,"InfoMsg": infomsg, "querySuccess": True,"isKR":False}
        newUrl = list(filter(lambda x : 'investing.com' in x['href'],  list(filter(lambda x : x.get('href'), s.select('a'))) ))
        if newUrl : 
            newUrl = newUrl[0]['href']
            s = bs(StockGetter.requestsGet(newUrl),'html.parser')
            stockName = s.select('h1.float_lang_base_1')[0].text
            infomsg = " ["+stockName.strip()+"]\n"
            price = s.select('#last_last')[0].text 
            move,percentage = s.select('span.arial_20')
            move = move.text 
            percentage = percentage.text
            infomsg+=price+' '+move+' '+percentage
            return {"stockName": stockName,"InfoMsg": infomsg, "querySuccess": True,"isKR":False}
        else : 
            return {"stockName": stockName,"InfoMsg": "Error {}".format("not found stock"), "querySuccess": False}