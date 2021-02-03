from time import sleep
from celery import shared_task
from .models import GetStockMsg
from bs4 import BeautifulSoup as bs
from pprint import pprint as pp
import requests

headers_Get = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:49.0) Gecko/20100101 Firefox/49.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate',
    'DNT': '1',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1'
    }

@shared_task
def UpdateStockGoogle() :
    print('Update..')
    s = requests.Session()
    url = 'https://www.google.com/search?q=TSLA+stock'
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
            Dividend = s.select('td.iyjjgb')[1].text.strip()
            infomsg = "[" + stockName +"]" + "\n" + Exchange + "\n" + "[" + Date+"]" + "\n" + stockMoney +" "+ Price + ", " + Move+Percentage +"\n" +       "[ Pre & After Market ]" + "\n" + stockMoney + PaPrice +", "+ PaMove + PaPercentage + "\n" + "[ Dividend yield ] : " + Dividend + "\n"
        else :
            infomsg = "[" + stockName +"]" + "\n" + Exchange + "\n" + "[" + Date+"]" + "\n" + stockMoney +" "+ Price + ", " + Move+Percentage +"\n" + "[ Dividend yield ] : " + Dividend + "\n"

        data = {'stockName' : stockName, 'stockInfo' : infomsg} 
        print(infomsg)
        GetStockMsg.objects.filter(stockName=stockName).update(**data)
        sleep(1) 
    
    else :
        print('update fail')
        pp(s)

@shared_task
def GetStockGoogle() :
    # global headers_Get
    print('step 1 ')
    s = requests.Session()
    url = 'https://www.google.com/search?q=TSLA+stock'
    response = s.get(url,  headers=headers_Get)
    html = response.text
    # header = response.headers 
    # status = response.status_code
    # if status != '200' : 
    #     print('requests error')
    #     return 0

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
            Dividend = s.select('td.iyjjgb')[1].text.strip()
            infomsg = "[" + stockName +"]" + "\n" + Exchange + "\n" + "[" + Date+"]" + "\n" + stockMoney +" "+ Price + ", " + Move+Percentage +"\n" +       "[ Pre & After Market ]" + "\n" + stockMoney + PaPrice +", "+ PaMove + PaPercentage + "\n" + "[ Dividend yield ] : " + Dividend + "\n"
        else :
            infomsg = "[" + stockName +"]" + "\n" + Exchange + "\n" + "[" + Date+"]" + "\n" + stockMoney +" "+ Price + ", " + Move+Percentage +"\n" + "[ Dividend yield ] : " + Dividend + "\n"

        print(infomsg)

        GetStockMsg.objects.create(
            stockInfo = infomsg,
            stockName = stockName
        )
        sleep(1) 
    else : 
        pp(s)
    print('step 3 ')

GetStockGoogle()
while True:
    sleep(15)
    UpdateStockGoogle()