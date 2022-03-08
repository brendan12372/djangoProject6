import pickle
from io import BytesIO

import requests
import yfinance as yf
from PIL import Image
from os import listdir
from os.path import isfile, join

curentList = []

import json, os
import pandas as pd


def makeDir():
    curDir = os.getcwd()
    try:
        os.mkdir('sectorData')
        os.mkdir('data')

    except Exception as e:
        print(e)

    dataDir = os.path.join(curDir, 'data')
    sectorDataDir = os.path.join(curDir, 'SectorData')


def temp(sortBy='yearReturn'):
    dfList = []
    x = []
    y = []
    z = []
    sectorList = []
    sl = []
    for a, b, c in os.walk(dataDir):
        z.append(a)
        sectorList.append(b)
        sl.append(c)
        fileList = []
    fileList = sl

    # print(fileList)
    sectorList = sectorList[0]
    # print(sectorList)
    sector = sectorList[4]  ####change
    fileList = []
    filePathList = []
    for i in range(len(sl) - 1):
        sectorPath = os.path.join(sectorDataDir, sector)
        fileList.append(sl[i + 1])
    myDict = dict(zip(sectorList, fileList))
    x = myDict
    keys = list(x.keys())
    vals = list(x.values())
    # print(keys)
    # print(vals)
    symbol_list = []
    for i in range(len(keys)):
        x = vals

    # print(keys)
    # print(x)
    for i in range(len(keys)):

        key = keys[i]
        # print(key)
        symbols = []
        vl = []
        na = sortBy

        for val in x[i]:
            message = val

            # check if the message ends with fun
            if message.endswith('json'):
                p = os.path.join(dataDir, key, val)

                # JSON file
                # print(p)

                f = open(p)

                # Reading from file
                data = json.loads(f.read())

                # print(f"{data['symbol']} {data['yearReturn']}")
                symbols.append(data['symbol'])
                symbol_list.append(data['symbol'])
                vl.append(data[na])

        data = {
            "symbols": symbols,
            na: vl
        }
        df = pd.DataFrame(data)
        # df['rank']=df.yearReturn.sort()
        dfList.append(df)

        df = df.sort_values(by=na, ascending=False)
        print(df)
        try:
            p = os.path.join(sectorDataDir, sortBy)
            os.mkdir(p)

        except Exception as e:
            # print(f'89 {e}')
            pass
        p = os.path.join(p, f'{key}.csv')
        df.to_csv(p)

    import pickle
    with open('universe.pickel', 'wb') as f:
        pickle.dump(symbol_list, f)
    # with open("universe.txt", 'w') as f:
    #     for item in symbol_list:
    #         f.write("%s\n" % item)


curDir = os.getcwd()
try:
    os.mkdir('data')
except:
    pass
dataDir = os.path.join(curDir, 'data')
sectorDataDir = os.path.join(curDir, 'sectorData')


class Stock:
    def __init__(self, symbol, p='1y'):
        self.path = dataDir
        curentList.append(symbol)
        self.symbol = symbol
        self.ticker = yf.Ticker(symbol)
        self.info = self.ticker.info
        self.sector = self.info['sector']
        try:
            self.sectorDir = os.path.join(dataDir, self.sector)
            os.mkdir(self.sectorDir)
        except:
            pass
        self.filePath = os.path.join(dataDir, self.sector, self.symbol) + '.json'
        self.hist = self.ticker.history(period=p)
        try:
            self.news = self.ticker.news
        except:
            self.news = None
        self.yearReturn = self.info['52WeekChange']
        self.pegRatio = self.info['pegRatio']
        self.shortPercentOfFloat = self.info['shortPercentOfFloat']
        self.marketCap = self.info['marketCap']
        self.payoutRatio = self.info['payoutRatio']
        try:
            self.fullTimeEmployees = self.info['fullTimeEmployees']
        except Exception as e:
            print(f'136: {e}')
            self.fullTimeEmployees = 0
        try:
            self.teps = self.info['trailingEps']
            self.feps = self.info['forwardEps']
            self.ebitdaMargins = self.info['ebitdaMargins']
            self.fpe = self.info['forwardPE']
            self.logo = self.info['logo_url']
            self.response = requests.get(self.logo)
            self.img = Image.open(BytesIO(self.response.content))
            self.ptb = self.info['priceToBook']
            self.roe = self.info['returnOnEquity']
            self.currentRatio = self.info['currentRatio']
            self.debtEquityRatio = self.info['debtToEquity']
            self.insiders = self.info['heldPercentInsiders']
            self.tcps = self.info['totalCashPerShare']
            self.quickRatio = self.info['quickRatio']
            self.shortName = self.info['shortName']
            self.lastDividendValue = self.info['lastDividendValue']
            self.beta = self.info['beta']
            self.threeYearAverageReturn = self.info['threeYearAverageReturn']
            self.sharesPercentSharesOut = self.info['sharesPercentSharesOut']
        except Exception as e:
            print(f'err: {e}')

        self.method_list = [method for method in dir(self) if method.startswith('__') is False]
        self.mySave()

    def mySave(self):
        fp = os.path.join(dataDir, self.sector, self.symbol) + '.pickle'
        with open(fp, 'wb') as f:
            # Pickle the 'data' dictionary using the highest protocol available.
            pickle.dump(self, f, pickle.HIGHEST_PROTOCOL)
        x = json.dumps(self.__dict__, indent=4, sort_keys=True, default=str)
        j = json.loads(x)
        with open(self.filePath, 'w') as f:
            json.dump(j, f)

    def __repr__(self):
        return self.filePath


def updateUniverse():
    with open('universe.pickle', 'rb') as pickle_file:
        content = pickle.load(pickle_file)
    sc = []
    for c in content:
        sc.append(c.strip())
    final = set(sc)
    for s in final:
        print(s)
        x = Stock(s, '1y')


def sortUniverse():
    ml = ['payoutRatio', 'pegRatio', 'fullTimeEmployees', 'yearReturn', 'beta', 'currentRatio', 'debtEquityRatio',
          'ebitdaMargins', 'feps', 'fpe', 'insiders' 'ptb',
          'quickRatio', 'marketCap']
    for m in set(ml):
        try:
            temp(sortBy=m)
        except Exception as e:
            print(e)


def sortStocks(sector, sortBy):
    r = requests.get(f'http://127.0.0.1:8000/stocks/{sector}/{sortBy}').json()
    keys = []
    vals = []
    ranks = []
    rank = 0

    for i in range(len(r)):
        try:
            val = r[i][sortBy]
        except:
            val = None
            print(r[i])
        if val != None:
            rank += 1
            symbol = r[i]["symbol"]
            keys.append(symbol)
            ranks.append(rank)
            vals.append(val)

    dictionary = dict(zip(keys, vals))
    return dictionary


sectorList = ['Basic%20Materials', 'Consumer%20Defensive', 'Healthcare', 'Communication%20Services', 'Energy',
              'Industrials',
              'Consumer%20Cyclical', 'Financial%20Services', 'Technology']

sectorLL = ['Basic Materials', 'Consumer Defensive', 'Healthcare', 'Communication Services', 'Energy','Industrials','Consumer Cyclical', 'Financial Services', 'Technology']
sectorsDict=dict(zip(sectorList,sectorLL))
# ml = ['ptb','pegRatio', 'yearReturn'
#       , 'fpe', 'insiders', 'marketCap']
# ml = [
#     'ebitdaMargins',
#     'yearReturn',
#     'pegRatio',
#     'shortPercentOfFloat',
#     'marketCap',
#     'payoutRatio',
#     'fullTimeEmployees',
#     'teps',
#     'feps',
#     'fpe',
#     'ptb',
#     'roe',
#     'currentRatio',
#     'debtEquityRatio',
#     'insiders',
#     'tcps',
#     'quickRatio',
#     'beta',
#     'sharesPercentSharesOut']
ml= ['zip', 'sector', 'fullTimeEmployees', 'longBusinessSummary', 'city', 'phone', 'state', 'country',
         'companyOfficers', 'website', 'maxAge', 'address1', 'industry', 'address2', 'ebitdaMargins', 'profitMargins',
         'grossMargins', 'operatingCashflow', 'revenueGrowth', 'operatingMargins', 'ebitda', 'targetLowPrice',
         'recommendationKey', 'grossProfits', 'freeCashflow', 'targetMedianPrice', 'currentPrice', 'earningsGrowth',
         'currentRatio', 'returnOnAssets', 'numberOfAnalystOpinions', 'targetMeanPrice', 'debtToEquity',
         'returnOnEquity', 'targetHighPrice', 'totalCash', 'totalDebt', 'totalRevenue', 'totalCashPerShare',
         'financialCurrency', 'revenuePerShare', 'quickRatio', 'recommendationMean', 'exchange', 'shortName',
         'longName', 'exchangeTimezoneName', 'exchangeTimezoneShortName', 'isEsgPopulated', 'gmtOffSetMilliseconds',
         'quoteType', 'symbol', 'messageBoardId', 'market', 'annualHoldingsTurnover', 'enterpriseToRevenue',
         'beta3Year', 'enterpriseToEbitda', '52WeekChange', 'morningStarRiskRating', 'forwardEps',
         'revenueQuarterlyGrowth', 'sharesOutstanding', 'fundInceptionDate', 'annualReportExpenseRatio', 'totalAssets',
         'bookValue', 'sharesShort', 'sharesPercentSharesOut', 'fundFamily', 'lastFiscalYearEnd',
         'heldPercentInstitutions', 'netIncomeToCommon', 'trailingEps', 'lastDividendValue', 'SandP52WeekChange',
         'priceToBook', 'heldPercentInsiders', 'nextFiscalYearEnd', 'yield', 'mostRecentQuarter', 'shortRatio',
         'sharesShortPreviousMonthDate', 'floatShares', 'beta', 'enterpriseValue', 'priceHint',
         'threeYearAverageReturn', 'lastSplitDate', 'lastSplitFactor', 'legalType', 'lastDividendDate',
         'morningStarOverallRating', 'earningsQuarterlyGrowth', 'priceToSalesTrailing12Months', 'dateShortInterest',
         'pegRatio', 'ytdReturn', 'forwardPE', 'lastCapGain', 'shortPercentOfFloat', 'sharesShortPriorMonth',
         'impliedSharesOutstanding', 'category', 'fiveYearAverageReturn', 'previousClose', 'regularMarketOpen',
         'twoHundredDayAverage', 'trailingAnnualDividendYield', 'payoutRatio', 'volume24Hr', 'regularMarketDayHigh',
         'navPrice', 'averageDailyVolume10Day', 'regularMarketPreviousClose', 'fiftyDayAverage',
         'trailingAnnualDividendRate', 'open', 'toCurrency', 'averageVolume10days', 'expireDate', 'algorithm',
         'dividendRate', 'exDividendDate', 'circulatingSupply', 'startDate', 'regularMarketDayLow', 'currency',
         'regularMarketVolume', 'lastMarket', 'maxSupply', 'openInterest', 'marketCap', 'volumeAllCurrencies',
         'strikePrice', 'averageVolume', 'dayLow', 'ask', 'askSize', 'volume', 'fiftyTwoWeekHigh', 'fromCurrency',
         'fiveYearAvgDividendYield', 'fiftyTwoWeekLow', 'bid', 'tradeable', 'dividendYield', 'bidSize', 'dayHigh',
         'regularMarketPrice', 'preMarketPrice', 'logo_url']


def add_stock(symbol):
    url = ('http://127.0.0.1:8000/stocks/all/yearReturn/up')
    myobj = {"symbol": symbol}
    x = requests.post(url, data=myobj)


def sortStocks(sector, sortBy, dir='up'):
    r = requests.get(f'http://127.0.0.1:8000/stocks/{sector}/{sortBy}/{dir}').json()
    keys = []
    vals = []
    ranks = []
    rank = 0
    for i in range(len(r)):
        val = r[i][sortBy]
        if val != None:
            rank += 1
            symbol = r[i]["symbol"]
            keys.append(symbol)
            ranks.append(rank)
            vals.append(val)

    dictionary = dict(zip(keys, vals))
    return dictionary


def sortSectors(sortBy='yearReturn', dir='up',normalize='True'):
    r = requests.get(f'http://127.0.0.1:8000/sectors/{sortBy}/{dir}').json()
    print(f'len:{len(r)} r[0]:{r[0]["ave"]}')


    keys = []
    vals = []
    ranks = []
    rank = 0
    for i in range(len(r)):
        val=r[i]["ave"]
        sec=r[i]["name"]
        if val != None:
            rank += 1
            keys.append(sec)
            ranks.append(rank)
            vals.append(val)

    dictionary = dict(zip(keys, vals))
    return dictionary


info = {
    "payoutRatio":
        "The payout ratio shows the proportion of earnings a company pays its shareholders in the form of dividends,"
        " expressed as a percentage of the company's total earnings. The calculation is derived by dividing the "
        "total dividends being paid out by the net income generated.",
"ebitdaMargins":"The EBITDA margin is a measure of a company's operating profit as a percentage of its revenue. The "
                "acronym EBITDA stands for earnings before interest, taxes, depreciation, and amortization. Knowing "
                "the EBITDA margin allows for a comparison of one company's real performance to others in its "
                "industry.",

"marketCap":"Market cap—or market capitalization—refers to the total value of all a company's shares of stock. It is calculated by multiplying the price of a stock by its total number of outstanding shares. For example, a company with 20 million shares selling at $50 a share would have a market cap of $1 billion.",
"ptb": "Companies use the price-to-book ratio (P/B ratio) to compare a firm's market capitalization to its book value. It's calculated by dividing the company's stock price per share by its book value per share (BVPS). An asset's book value is equal to its carrying value on the balance sheet, and companies calculate it netting the asset against its accumulated depreciation. Book value is also the tangible net asset value of a company calculated as total assets minus intangible assets (.e.g. patents, goodwill) and liabilities. For the initial outlay of an investment, book value may be net or gross of expenses, such as trading costs, sales taxes, and service charges. Some people may know this ratio by its less common name, the price-equity ratio.",
"fullTimeEmployees": "Number of employees",
"pegRatio":"The price/earnings to growth ratio (PEG ratio) is a stock's price-to-earnings (P/E) ratio divided by the growth rate of its earnings for a specified time period. The PEG ratio is used to determine a stock's value while also factoring in the company's expected earnings growth, and it is thought to provide a more complete picture than the more standard P/E ratio. ",
"yearReturn":"change in share price last year",
"fpe":"A variation of the price-to-earnings ratio (P/E ratio) is the forward P/E ratio, which is based on a prediction of a company's future earnings. Earnings used in the forward P/E ratio are estimates of future earnings, while the standard P/E ratio uses actual earnings per share from the company's previous four quarters.",
"quickRatio":" QR = (Current Assets - Inventories - Prepaid Expenses) / Current Liabilities.The quick ratio is an indicator of a company’s short-term liquidity position and measures a company’s ability to meet its short-term obligations with its most liquid assets. Since it indicates the company’s ability to instantly use its near-cash assets (assets that can be converted quickly to cash) to pay down its current liabilities, it is also called the acid test ratio. An 'acid test' is a slang term for a quick test designed to produce instant results. ",
"currentRatio":" The current ratio is a liquidity ratio that measures a company’s ability to pay short-term obligations or those due within one year. It tells investors and analysts how a company can maximize the current assets on its balance sheet to satisfy its current debt and other payables.A current ratio that is in line with the industry average or slightly higher is generally considered acceptable. A current ratio that is lower than the industry average may indicate a higher risk of distress or default. Similarly, if a company has a very high current ratio compared with its peer group, it indicates that management may not be using its assets efficiently.The current ratio is called current because, unlike some other liquidity ratios, it incorporates all current assets and current liabilities. The current ratio is sometimes called the working capital ratio. ",
"roe":"Return on equity (ROE) is a measure of financial performance calculated by dividing net income by shareholders' equity. Because shareholders' equity is equal to a company’s assets minus its debt, ROE is considered the return on net assets. ROE is considered a gauge of a corporation's profitability and how efficient it is in generating profits. ",
    "teps":
        " Trailing earnings per share (EPS) is a company's earnings generated over a prior period (often a fiscal year) reported on a per-share basis."
"The term trailing moreover implies a value calculated on a rolling basis. That is, trailing EPS may describe the most recent 12-month period or four earnings releases. The period used for a trailing EPS will change as the most recent earnings are added to the calculation and earnings from five quarters ago are dropped from the calculation. ",
    "feps":"The Forward Price-to-Earnings or Forward P/E Ratio. The forward P/E ratio (or forward price-to-earnings ratio) divides the current share price of a company by the estimated future earnings per share (EPS) of that company.",
    "debtEquityRatio":"The debt-to-equity (D/E) ratio compares a company's total liabilities to its shareholder equity and can be used to evaluate how much leverage a company is using. Higher-leverage ratios tend to indicate a company or stock with higher risk to shareholders.",
    "shortPercentOfFloat":"The short percentage of float is the percentage of a company's stock that has been shorted by institutional traders, compared to the number of shares of a company's stock that are available to the public.",
    "beta":"Beta is a measure of a stock's volatility in relation to the overall market. By definition, the market, such as the S&P 500 Index, has a beta of 1.0, and individual stocks are ranked according to how much they deviate from the market. A stock that swings more than the market over time has a beta above 1.0.",
    "insiders":"The insiders percentage is the percentage of float is the percentage of a company's stock that has been shorted by institutional traders,ort percentage of float is owned by employees",
}
