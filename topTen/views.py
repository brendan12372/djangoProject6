import requests

from pyFundamental.utils import sortStocks
from django.shortcuts import render
from .forms import optionForm,addForm
from statistics import mean
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseRedirect
from pyFundamental.utils import add_stock,sectorList,ml,sortSectors,info,sectorLL,sectorsDict
from .models import Options,Sectoroptions
o=Options()
s=Sectoroptions()



@csrf_exempt
def vTwo(request):
    context = {
        "ml": ml,
        "sectorList": sectorList,
        "sectorLL": sectorLL,

        "sector": o.sector,
        "sortBy": o.sortBy,
        "info":"111",


        "dir":o.dir,
        "data": ['x','x']
    }
    if request.method == 'POST':
        try:
            add_stock(request.POST["symbol"])
        except:
            pass
        o.sortBy=request.POST["sortBy"]
        o.sector=request.POST["sector"]
        o.normalize=request.POST["normalize"]
        o.dir=request.POST["dir"]
        o.save()
        print(f'dir:{o.dir}')
        data=sortStocks(sector=o.sector,sortBy=o.sortBy,dir=o.dir)
        ave=mean(data.values())
        norm_data = []
        for v in data.values():
            norm_data.append(round(v/ave,2))
        norm_data=dict(zip(data.keys(),norm_data))
        if o.normalize=="True":
            data=norm_data
        else:
            data=data
        try:
            x=info[o.sortBy]
        except:
            x='testinfo'

        context = {
            "ml": ml,
            "sectorList": sectorList,
            "sector": o.sector,
            "sortBy": o.sortBy,
            "dir":o.dir,
            "normalize": o.normalize,
            'info':x,
            "data": data,
            "sectorLL": sectorLL,
            "sectorDict":sectorsDict,
            "average":round(ave,2)
        }

    template_name = "topTen/test2.html"
    x=sortStocks(sector='Technology',sortBy='yearReturn')
    return render(template_name=template_name,request=request,context=context)

@csrf_exempt
def sector_view(request):

    # if request.method == 'POST':
    #     data = sortSectors(sortBy="yearReturn", dir='up')
    context = {
        "ml": ml,
        "sectorList": sectorList,
        'dir':s.dir,
        'sortBy':s.sortBy,
        'normalize': s.normalize,
        'info':info[s.sortBy],


        "data": ['data']
    }
    print(request)
    if request.method == 'POST':
        print('post')

        s.normalize = request.POST["normalize"]
        s.sortBy=request.POST["sortBy"]
        s.dir=request.POST["dir"]
        s.save()
        data = sortSectors( sortBy=s.sortBy, dir=s.dir)
        ave=mean(data.values())
        norm_data=[]
        norm_data = []
        for v in data.values():
            norm_data.append(round(v/ave,2))
        norm_data=dict(zip(data.keys(),norm_data))
        if s.normalize=="True":
            data=norm_data
        else:
            data=data
        try:
            print(s.sortBy)
            i=info.s.sortBy
        except :
           i='None Yet'
    context = {
        "ml": ml,
        "sectorList": sectorList,
        "options": s,
        'dir':s.dir,
        'sortBy':s.sortBy,
        'normalize': s.normalize,
        "info":info[s.sortBy],

        "data":  data
    }


    template_name = "topTen/sector.html"
    return render(template_name=template_name, request=request, context=context)

