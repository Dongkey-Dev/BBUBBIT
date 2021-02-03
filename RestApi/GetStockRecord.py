from bs4 import BeautifulSoup as bs
import requests 
import logging 
import re
"""
1. 먼저 구글에서 찾아보고
2. 없으면 국장
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

parseDate = {
    'Jan':'1','Feb':'2','Mar':'3','Apr':'4','May':'5','Jun':'6','Jul':'7','Aug':'8','Sep':'9','Oct':'10','Nov':'11','Dec':'12'
}    
korean = re.compile('[\u3131-\u3163\uac00-\ud7a3]+')

logger = logging.getLogger(__name__)        

class WrongHtml(Exception) : 
    def __init__(self):
        super().__init__('Fail to get HTML')

class StockRecordGetter :
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
            return bs(response.text ,'html.parser')
        else : 
            logger.error("resquest's status code is {}".format(response.status_code))
            raise WrongHtml

    
    @staticmethod 
    def isInGoogle(stockName) :
        isInGoogle = StockRecordGetter.GetStockRecordInvesting(stockName)
        return isInGoogle

    @staticmethod
    def isKrStock(stockName) : 
        global headers_Get
        paxnet = 'http://www.paxnet.co.kr/search/jongmok?kwd=' + stockName 
        logger.debug('paxnet URL is {}'.format(paxnet))
        s = requests.Session()
        response = s.get(paxnet, headers=headers_Get)
        code = response.text.split('value="')[2][:6]
        if code : 
            return StockRecordGetter.GetStockRecordNaver(stockName, code)
        elif s.select('input[name=searchSymbol]') and s.select('strong') : 
            code = s.select('input[name=searchSymbol]')[0]['value']
            if not code.isnumeric() : 
                return {"stockName": stockName,"InfoMsg": "Error {}".format("not found stock"), "querySuccess": False}
            stockName = s.select('strong')[0].text
            return StockRecordGetter.GetStockRecordNaver(stockName, code)
        else : 
            return {"stockName": stockName,"InfoMsg": "Error {}".format("not found stock"), "querySuccess": False}

    @staticmethod
    def GetStockRecordNaver(stockName, code) : 
        global headers_Get
        logger.debug('recieved StockName = {}'.format(stockName + ' ' + code))
        s = requests.Session()
        url = "https://finance.naver.com/item/sise_day.nhn?code=" + code
        response = s.get(url, headers=headers_Get)
        html = response.text
        header = response.headers 
        status = response.status_code
        if status != 200 : 
            return {"stockName": stockName,"InfoMsg": "Error : {}".format("Naver Request Error"), "querySuccess": False}
        s=bs(html,'html.parser')
        trg = s.select('tr[onmouseover=mouseOver(this)]')
        if len(trg) >= 10 : 
            maxLength = 10 
        else : 
            maxLength = len(trg)
        infomsg = " ["+stockName.strip()+"]\n"
        recent = trg[0].select('td.num')[0].text.replace(',','')
        late = trg[maxLength-1].select('td.num')[0].text.replace(',','')
        cal = int(recent) - int(late)
        if cal == 0 : 
            total_percentage='+0'
        else : 
            total_percentage = cal/int(late)*100
            if total_percentage>=0 : 
                total_percentage='+'+str(total_percentage)
            if '.' in total_percentage : 
                total_percentage = total_percentage.split('.')[0] + '.' + total_percentage.split('.')[1][:2]
        for i in range(maxLength) : 
            date = trg[i].select('td[align=center]')[0].text
            price = trg[i].select('td.num')[0].text.replace(',','')
            moveup = trg[i].select('span.tah.p11.red02')
            movedown = trg[i].select('span.tah.p11.nv01')
            movezero = trg[i].select('span.tah.p11')
            if movezero[0].text == '0' : 
                percentage = '+0'
            elif moveup : 
                moveup=moveup[0].text.replace(',','')
                lastPrice = int(price)-int(moveup)
                percentage = int(moveup)/lastPrice*100
                if '.' in str(percentage) :
                    percentage = str(percentage).split('.')[0] + '.' +str(percentage).split('.')[1][:2]
                else : 
                    percentage = '+'+str(percentage)
            elif movedown : 
                movedown=movedown[0].text.replace(',','')
                lastPrice = int(price)+int(movedown)
                percentage = int(movedown)/lastPrice*100
                if '.' in str(percentage) :
                    percentage = str(percentage).split('.')[0] + '.' +str(percentage).split('.')[1][:2]
                else : 
                    percentage = '-'+str(percentage)
            infomsg+=date+": "+format(int(price),',')+" ("+percentage+"%) \n"
        infomsg+=str(maxLength)+"일간의 수익률 : "+str(total_percentage)+"%"
        return {"stockName": stockName.strip(),"InfoMsg": infomsg, "querySuccess": True}

    @staticmethod
    def GetStockRecordInvesting(stockName) :
        global korean
        global headers_Get
        logger.debug('recieved StockName = {}'.format(stockName))
        s = requests.Session()
        url = 'https://www.google.com/search?q='+stockName+'+historical+data'
        s = StockRecordGetter.requestsGet(url)
        newUrl = list(filter(lambda x : 'investing.com' in x['href'],  list(filter(lambda x : x.get('href'), s.select('a'))) ))
        if newUrl : 
            newUrl = newUrl[0]['href']
            s = StockRecordGetter.requestsGet(newUrl)
            stockName = s.select('h1.float_lang_base_1')[0].text
            infomsg = " ["+stockName.strip()+"]\n"
            data = s.select('table.genTbl.closedTbl.historicalTbl > tbody > tr')
            if len(data) >= 10 : 
                maxLength = 10 
            else : 
                maxLength = len(data)
            recent = s.select('table.genTbl.closedTbl.historicalTbl > tbody > tr')[0].select('td')[1].text
            late = s.select('table.genTbl.closedTbl.historicalTbl > tbody > tr')[maxLength-1].select('td')[1].text
            if ',' in recent : 
                recent = recent.replace(',','')
                late = late.replace(',','')
            cal = float(recent) - float(late)
            if cal == 0.0 :
                totalPercentage = '+0'
            else : 
                totalPercentage = float(cal)/float(late)*100
                if totalPercentage>=0 : 
                    totalPercentage = '+' + str(totalPercentage)
                else : 
                    totalPercentage=str(totalPercentage)
                totalPercentage = totalPercentage.split('.')[0] + '.' + totalPercentage.split('.')[1][:2]

            for i in range(maxLength) : 
                date = data[i].select('td')[0].text 
                date = re.sub(korean, '.', date)
                if date[-1] == '.' : 
                    date = date[:-1]
                price = data[i].select('td')[1].text 
                percentage = data[i].select('td')[6].text
                infomsg+=date+": "+price+" ("+percentage+")\n"
            infomsg+=str(maxLength)+"일간의 수익률 : "+ totalPercentage
            return {"stockName": stockName.strip(),"InfoMsg": infomsg, "querySuccess": True}
        else : 
            return {"stockName": stockName.strip(),"InfoMsg": "Error :{}".format("not found stock"), "querySuccess": False}