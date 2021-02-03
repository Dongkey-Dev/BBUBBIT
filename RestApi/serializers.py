from django.views.generic import View
from rest_framework import serializers 
from .models import GetStockMsg 

class GetStockMsgSerializer(serializers.ModelSerializer) :
    class Meta : 
        model = GetStockMsg 
        fields = '__all__'

class GetStockMsgPostSerializer(serializers.ModelSerializer) :
    class Meta : 
        model = GetStockMsg 
        fields = ['stockName']

     