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
from .GetStockPrice import *
from .GetStockRecord import *

from bs4 import BeautifulSoup as bs
import requests 
import logging 
import re

# Create your views here.

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
        GetStockMsg_serializer = GetStockMsgPostSerializer(data = GetStockMsg_data)
        if GetStockMsg_serializer.is_valid():
            GetStockMsg_serializer.save()
            if GetStockMsg_data['func'] == 'GetStockPrice' : # 단순 주가 조회
                stockName = GetStockMsg_data['stockName']
                infoMsg = StockGetter.isKrStock(stockName)
                return JsonResponse(infoMsg, status=status.HTTP_201_CREATED) 

            elif GetStockMsg_data['func'] == 'GetStockRecord' : # 주가 기록
                stockName = GetStockMsg_data['stockName']
                IsInGoogle = StockRecordGetter.isInGoogle(stockName)
                if IsInGoogle['querySuccess'] :
                    return JsonResponse(IsInGoogle, status=status.HTTP_201_CREATED) 
                IsInNaver = StockRecordGetter.isKrStock(stockName)
                if IsInNaver['querySuccess'] : 
                    return JsonResponse(IsInNaver, status=status.HTTP_201_CREATED) 
                else : 
                    return JsonResponse({"stockName":stockName,"infomsg":"Error : not found.", "querySuccess":False}, status=status.HTTP_201_CREATED)

class GetStockPostView(generics.CreateAPIView) : 
    queryset = GetStockMsg.objects.all()
    serializer_class = GetStockMsgPostSerializer