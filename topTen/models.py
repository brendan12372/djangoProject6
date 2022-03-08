from django.db import models

from django.db import models
from pyFundamental.utils import Stock as St


class Sectoroptions(models.Model):
    sortBy = models.CharField(max_length=200, blank=True, default='yearReturn')
    normalize = models.BooleanField(blank=True, default=False)
    dir = models.CharField(max_length=200, blank=True, default='up')


class Options(models.Model):
    sector = models.CharField(max_length=200, blank=True)
    sortBy = models.CharField(max_length=200, blank=True)
    normalize = models.BooleanField(blank=True, default=False)
    dir = models.CharField(max_length=200, blank=True)


class Stock(models.Model):
    symbol = models.CharField(max_length=200, unique=True)
    ebitdaMargins = models.FloatField(default=0, blank=True, null=True)
    sector = models.CharField(max_length=200, blank=True)
    yearReturn = models.FloatField(blank=True, null=True)
    pegRatio = models.FloatField(default=0, blank=True, null=True)
    shortPercentOfFloat = models.FloatField(default=0, blank=True, null=True)
    marketCap = models.IntegerField(default=0, blank=True, null=True)
    payoutRatio = models.FloatField(blank=True, null=True)
    fullTimeEmployees = models.IntegerField(blank=True, null=True)
    teps = models.FloatField(default=0, blank=True, null=True)
    feps = models.FloatField(default=0, blank=True, null=True)
    fpe = models.FloatField(default=0, blank=True, null=True)
    ptb = models.FloatField(default=0, blank=True, null=True)
    roe = models.FloatField(default=0, blank=True, null=True)
    currentRatio = models.FloatField(default=0, blank=True, null=True)
    debtEquityRatio = models.FloatField(default=0, blank=True, null=True)
    insiders = models.FloatField(default=0)
    tcps = models.FloatField(default=0)
    quickRatio = models.FloatField(default=0, blank=True, null=True)
    shortName = models.CharField(max_length=222, default='', blank=True)
    beta = models.FloatField(blank=True, null=True)
    sharesPercentSharesOut = models.FloatField(default=0)

    def getValue(self):
        if self.roe == 0:
            S = St(self.symbol)
            self.ebitdaMargins = round(S.ebitdaMargins,2)
            self.sector = S.sector
            self.yearReturn = round(S.yearReturn,2)
            self.pegRatio = round(S.pegRatio,2)
            self.shortPercentOfFloat = round(S.shortPercentOfFloat,2)
            self.marketCap = S.marketCap
            self.payoutRatio = round(S.payoutRatio,2)
            self.fullTimeEmployees = round(S.fullTimeEmployees)
            self.teps = round(S.teps,2)
            self.feps = round(S.feps,2)
            self.fpe = round(S.fpe,2)
            try:
                self.ptb = S.ptb
            except:
                pass
            try:
                self.roe = S.roe
            except:
                pass
            try:
                self.currentRatio = S.currentRatio
            except:
                self.currentRatio = 0
            try:
                self.debtEquityRatio = S.debtEquityRatio
            except:
                self.debtEquityRatio = 0
            try:
                self.insiders = S.insiders
            except:
                pass
            try:
                self.tcps = S.tcps
            except:
                pass
            try:
                self.quickRatio = S.quickRatio
            except:
                self.quickRatio = 0
            try:
                self.shortName = S.shortName
            except:
                self.shortName = S.symbol
            try:
                self.beta = S.beta
            except:
                pass
            try:
                self.sharesPercentSharesOut = S.sharesPercentSharesOut
            except:
                pass

    def __str__(self):
        return self.symbol

    # def save(self, *args, **kwargs):
    #     self.getValue()
    #     super(Stock, self).save(*args, **kwargs)
