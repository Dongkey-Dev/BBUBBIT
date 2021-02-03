from django.db import models

class GetStockMsg(models.Model) : 
    stockInfo = models.CharField(max_length = 400)
    stockName = models.CharField(max_length = 40)
    querySuccess = models.BooleanField(default=False)
    class Meta : 
        verbose_name = 'GetStockMsg'
        verbose_name_plural = 'GetStockMsges'

    def __str__(self) : 
        return self.stockName