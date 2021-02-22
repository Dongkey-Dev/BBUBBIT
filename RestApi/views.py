from django.http.response import JsonResponse
from django.shortcuts import render

from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser
from rest_framework.response import Response 
from django.http import HttpResponse
from rest_framework import generics
from rest_framework import status

from .serializers import GetStockMsgSerializer, GetStockMsgPostSerializer
from .models import GetStockMsg
from .GetIndicesFuture import *
from .GetInfoKrMarket import *
from .GetStockRecord import *
from .GetStockPrice import *
from .RestApiPK import PK

from bs4 import BeautifulSoup as bs
import requests 
import logging 
import re

logger = logging.getLogger(__name__)   

class ListGetStockView(generics.ListAPIView):
    queryset = GetStockMsg.objects.all()
    serializer_class = GetStockMsgSerializer

@api_view(['Get','POST'])
def GetStock(request) :  
    if request.method=='GET':
        qs = GetStockMsg.objects.all()
        serializer = GetStockMsgSerializer(qs, many=True)
        return HttpResponse(serializer.data , content_type="application/json")  

    elif request.method=='POST':
        GetStockMsg_data = JSONParser().parse(request)
        logger.info(GetStockMsg_data)   
        if GetStockMsg_data['PK'] != PK : 
            return JsonResponse({"Error":"WhoRU"}, status=status.HTTP_201_CREATED)
        GetStockMsg_serializer = GetStockMsgPostSerializer(data = GetStockMsg_data)
        if GetStockMsg_serializer.is_valid():
            GetStockMsg_serializer.save()
            if GetStockMsg_data['func'] == 'GetStockPrice' : # 단순 주가 조회
                stockName = GetStockMsg_data['stockName']
                infoMsg = StockGetter.isKrStock(stockName)
                logger.info({"ROOM": GetStockMsg_data['room'], "stockName":infoMsg['stockName'], "isKR":infoMsg['isKR']})
                return JsonResponse(infoMsg, status=status.HTTP_201_CREATED) 

            elif GetStockMsg_data['func'] == 'GetStockRecord' : # 주가 기록
                stockName = GetStockMsg_data['stockName']
                IsInGoogle = StockRecordGetter.isInGoogle(stockName)
                if IsInGoogle['querySuccess'] :
                    logger.info({"ROOM": GetStockMsg_data['room'], "stockName":IsInGoogle['stockName'], "isKR":False})
                    return JsonResponse(IsInGoogle, status=status.HTTP_201_CREATED) 
                IsInNaver = StockRecordGetter.isKrStock(stockName)
                if IsInNaver['querySuccess'] : 
                    logger.info({"ROOM": GetStockMsg_data['room'], "stockName":IsInNaver['stockName'], "isKR":True})
                    return JsonResponse(IsInNaver, status=status.HTTP_201_CREATED) 
                else : 
                    return JsonResponse({"stockName":stockName,"infomsg":"Error : not found.", "querySuccess":False}, status=status.HTTP_201_CREATED)
            
            elif GetStockMsg_data['func'] == 'Indices' : 
                if GetStockMsg_data['stockName'] == '선물' :
                    InfoMsg = StockIndicesGetter.GetStockIndicesFutureInvesting() 
                    if InfoMsg['querySuccess'] : 
                        logger.info({"ROOM": GetStockMsg_data['room'], "stockName":GetStockMsg_data['stockName'] , "isKR":False})
                        return JsonResponse(InfoMsg, status=status.HTTP_201_CREATED) 
                    else : 
                        return JsonResponse({"stockName":"선물","infomsg":"Error, Can't Connect Kr.investing.com/IndicesFuture", "querySuccess":False}, status=status.HTTP_201_CREATED)

                elif GetStockMsg_data['stockName'] == '원자재' :
                    InfoMsg = StockIndicesGetter.GetStockIndicesMaterialsInvesting() 
                    if InfoMsg['querySuccess'] : 
                        logger.info({"ROOM": GetStockMsg_data['room'], "stockName":GetStockMsg_data['stockName'] , "isKR":False})
                        return JsonResponse(InfoMsg, status=status.HTTP_201_CREATED) 
                    else : 
                        return JsonResponse({"stockName":"원자재","infomsg":"Error, Can't Connect Kr.investing.com/IndicesFuture", "querySuccess":False}, status=status.HTTP_201_CREATED)

                elif GetStockMsg_data['stockName'] == '지수' :
                    InfoMsg = StockIndicesGetter.GetStockIndicesInvesting() 
                    if InfoMsg['querySuccess'] : 
                        logger.info({"ROOM": GetStockMsg_data['room'], "stockName":GetStockMsg_data['stockName'] , "isKR":False})
                        return JsonResponse(InfoMsg, status=status.HTTP_201_CREATED) 
                    else : 
                        return JsonResponse({"stockName":"지수","infomsg":"Error, Can't Connect Kr.investing.com/major-Indices", "querySuccess":False}, status=status.HTTP_201_CREATED)                    

            elif GetStockMsg_data['func'] == 'KrMarket' : 
                if GetStockMsg_data['stockName'] == '국장' :
                    InfoMsg = KrMarketGetter.GetKrMarketMove() 
                    if InfoMsg['querySuccess'] : 
                        logger.info({"ROOM": GetStockMsg_data['room'], "stockName":GetStockMsg_data['stockName'], "isKR":True})
                        return JsonResponse(InfoMsg, status=status.HTTP_201_CREATED) 
                    else : 
                        return JsonResponse({"stockName":"국장","infomsg":"Error, Can't Connect Kr.investing.com/major-Indices", "querySuccess":False}, status=status.HTTP_201_CREATED)                    

class GetStockPostView(generics.CreateAPIView) : 
    queryset = GetStockMsg.objects.all()
    serializer_class = GetStockMsgPostSerializer