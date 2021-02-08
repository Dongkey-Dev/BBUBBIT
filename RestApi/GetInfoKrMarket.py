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

class KrMarketGetter :
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
    def GetKrMarketMove() :
        global headers_Get
        s = requests.Session()
        url = 'https://finance.naver.com/sise/'
        s = KrMarketGetter.requestsGet(url)
        Kospi = s.select('#KOSPI_now')
        if Kospi : 
            Kospi = s.select('#KOSPI_now')[0].text
            KospiMove = s.select('#KOSPI_change')[0].text
            KSPGaemi = s.select('li.c2')[0].text
            KSPWaein = s.select('li.c3')[0].text
            KSPGigwan = s.select('li.c4')[0].text
            Kosdaq = s.select('#KOSDAQ_now')[0].text
            KosdaqMove = s.select('#KOSDAQ_change')[0].text
            KSDGaemi = s.select('li.c2')[1].text
            KSDWaein = s.select('li.c3')[1].text
            KSDGigwan = s.select('li.c4')[1].text
            infomsg = "    [ 국장 ]\n"
            infomsg+="코스피 :"+Kospi.strip() +' '+KospiMove.strip().replace('상승','')+"\n"
            infomsg+="개인 : "+KSPGaemi.replace('개인','')+"\n"
            infomsg+="외국인 : "+KSPWaein.replace('외국인','')+"\n"
            infomsg+="기관 : "+KSPGigwan.replace('기관','')+"\n\n"
            infomsg+="코스닥 :"+Kosdaq.strip() +' '+KosdaqMove.strip().replace('상승','')+"\n"
            infomsg+="개인 : "+KSDGaemi.replace('개인','')+"\n"
            infomsg+="외국인 : "+KSDWaein.replace('외국인','')+"\n"
            infomsg+="기관 : "+KSDGigwan.replace('기관','')+""
            return {"stockName": '국장',"InfoMsg": infomsg, "querySuccess": True}
        else : 
            return {"stockName": "국장","InfoMsg": "Error :{}".format("not found stock"), "querySuccess": False}        