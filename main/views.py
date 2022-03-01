from urllib import response
from django.shortcuts import render , redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from matplotlib.pyplot import prism
from . forms import UserRegisterForm,StockForm
from . models import Stock
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponse
from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.template import Context
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import JsonResponse

import os,sys
from gnewsclient import gnewsclient
from pynse import *
from nsepython import *
nse = Nse()
from matplotlib import markers
	
import yahoo_fin.stock_info as si
import yfinance as yf  
from yahoo_fin import news as yf_news


import requests
import pandas as pd
import json
import datetime,time

# Create your models here.


mode ='local'

if(mode=='local'):

        headers = {
            'Connection': 'keep-alive',
            'Cache-Control': 'max-age=0',
            'DNT': '1',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.79 Safari/537.36',
            'Sec-Fetch-User': '?1',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Sec-Fetch-Site': 'none',
            'Sec-Fetch-Mode': 'navigate',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'en-US,en;q=0.9,hi;q=0.8',
        }
        
def nsefetch(payload):
            try:
                output = requests.get(payload,headers=headers).json()
                #print(output)
            except ValueError:
                s =requests.Session()
                output = s.get("http://nseindia.com",headers=headers)
                output = s.get(payload,headers=headers).json()
            return output

run_time=datetime.datetime.now()
    #Constants
indices = ['NIFTY','FINNIFTY','BANKNIFTY']

    
def running_status():
        start_now=datetime.datetime.now().replace(hour=9, minute=15, second=0, microsecond=0)
        end_now=datetime.datetime.now().replace(hour=15, minute=30, second=0, microsecond=0)
        return start_now<datetime.datetime.now()<end_now

def nsesymbolpurify(symbol):
        symbol = symbol.replace('&','%26') #URL Parse for Stocks Like M&M Finance
        return symbol

def nse_marketStatus():
        #payload = json.loads(requests.get('https://www.nseindia.com/api/market-status-india?date='+str(datetime.datetime.now().date())).text)
        
        payload = nsefetch('https://nseindia.com/api/marketStatus')
        status = payload['marketState'][0]['marketStatus']
        #print(status)
        
        return status

def nse_events():
    output = nsefetch('https://www.nseindia.com/api/event-calendar')
    return pd.json_normalize(output)


class MyLoginView(LoginView):
    template_name = 'main/accounts/login.html'

    def get_success_url(self) -> str:
        return "/index/"

# Create your views here.
def register(request):
    form = UserRegisterForm()
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            htmly = get_template('main/accounts/email.html')
            d = { 'username': username }
            subject, from_email, to = 'welcome', 'greengraph07@gmail.com', email
            html_content = htmly.render(d)
            msg = EmailMultiAlternatives(subject, html_content, from_email, [to])
            msg.attach_alternative(html_content, "text/html")
            msg.send()
            messages.success(request, f'Account created for {username}!')
            response = redirect('/login/')
            return response

    else:
        form = UserRegisterForm()
    return render(request, 'main/accounts/register.html', {'form': form})

@login_required
def index(request):
    #print (json.dumps(getQuotes('NIFTY.NS'), indent=2))
    #getQuotes('NIFTY.NS')
    
    
    market=nse_marketStatus()
    topgainers = nse.top_gainers()
    toplosers = nse.top_losers()
    Banknifty = nse_quote_ltp('BANKNIFTY')
    nifty = nse_quote_ltp("NIFTY")
    
    #print(nse_results("equities","Quarterly"))
    #print(nse_results("equities","Annual"))
    #print(nse_results("sme","Quarterly"))
    #print(nse_results("sme","Annual"))
    bank_pchange = nse_get_index_quote("nifty bank")['percChange']
    nifty_pchange = nse_get_index_quote("nifty 50")['percChange']
    vix = nse_get_index_quote("India VIX")['last']
    vix_pchange = nse_get_index_quote("India VIX")['percChange']
    vix_data = {'vix':vix,'vix_pchange':vix_pchange}
    Banknifty_data = {'Banknifty':Banknifty,'Banknifty_pchange':bank_pchange}
    nifty_data = {'Nifty':nifty,'Nifty_pchange':nifty_pchange}
    
    #print(Banknifty_data)
    #print(nifty_data)
    
    #print(si.get_company_info('SBIN.NS'))
    
    if request.user.is_authenticated:
        if request.method == 'POST':
            stock = request.POST['stock']
            stock_info = nse.info(stock)
            
            form = StockForm(request.POST)
            if form.is_valid():
                form.save()
        else:
            form = StockForm()
        return render(request, 'main/index_2.html', {'form': form,'market':market,'topgainers':topgainers,'toplosers':toplosers,'User':request.user,'Banknifty':Banknifty_data,'nifty':nifty_data,'vix':vix_data})
    else:
        return redirect("/login/")

def error_404(request, exception, template_name='main/accounts/404.html'):
    #print("Excuse me biradar")
    #print(template_name)
    
    response = render(request, template_name)
    response.status_code = 404
    return response
    # return render(request, 'main/404.html',data)

def error_500(request,template_name='main/accounts/500.html'):
    response = render(request, template_name)
    response.status_code = 500
    return response

@login_required    
def fii_dii(request):
    market = nse_marketStatus()
    fii_dii_data = nse.fii_dii()
    fii = fii_dii_data['FII/FPI *']
    dii = fii_dii_data['DII **']
    return render(request, 'main/fii_dii.html', {'fii':fii,'dii':dii,'market':market,'User':request.user})

@login_required   
def optionchain(request):
    market = nse_marketStatus()
    nifty = nse.option_chain("NIFTY")
    banknifty = nse.option_chain("BANKNIFTY")
    expiry = nifty['expiryDate'].iloc[0]
    
    return render(request, 'main/optionchain.html', {'market':market,'nifty':nifty,'banknifty':banknifty,'expiry':expiry,'User':request.user})

@login_required   
def events(request):
    market = nse_marketStatus()
    events = nse_events()
    return render(request, 'main/events.html', {'market':market,'events':events,'User':request.user})

@login_required   
def block_deals(request):
    market = nse_marketStatus()
    
   
    #print(block_deals)
    
    return render(request, 'main/block_deals.html', {'market':market,'User':request.user})

@login_required
def news(request):
    market = nse_marketStatus()
    client = gnewsclient.NewsClient(language='English', location='india', topic='Business',max_results=50)
    news = client.get_news()
    
    # get news feed
    
    return render(request, 'main/news.html', {'market':market,'User':request.user,'news':news})

def stock_info(request,symbol):
    market = nse_marketStatus()
    stock_info = nse.info(symbol)
    return render(request, 'main/stock_info.html', {'market':market,'stock_info':stock_info,'User':request.user})

def requestSearch(request):
	ticker = request.GET.get('query')
	req = requests.get(f"https://api.tickertape.in/search?text={ticker}&types=stock,etf&exchanges=NSE")
	jsreq = req.json()
	resp = jsreq['data']['stocks']
	result = {}
	res = []
	for i in resp:
		name = i['ticker']
		res.append({'ticker':i['name'] + ' - ' + i['ticker'], 'name':i['name'] + ' - ' + i['ticker'], 'url': f'/stock/{name}'})
	result['results'] = res
	return JsonResponse(result, safe=False)

'''
Kite: https://kite.trade/docs/connect/v3/user/#login-flow
oc: https://github.com/ranjanrak/OptionChainStream
Sector: https://github.com/JerBouma/FinanceDatabase
Finance: https://github.com/LastAncientOne/SimpleStockAnalysisPython
https://github.com/pranjal-joshi/Screeni-py
'''