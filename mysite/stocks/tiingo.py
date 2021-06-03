#API call for Tiingo API: https://api.tiingo.com/documentation

import requests

import os
import django
import sys

path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

if path not in sys.path:
    sys.path.append(path)
    
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")
os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"
django.setup()
from stocks.models import Favourite,watchlist


headers = {
    'Content-Type': 'application/jaon',
    'Authorization': 'Token 7c39770410248a95981a58472b1bf42bda56a0af'
}

def get_meta_data(ticker):
    url = "https://api.tiingo.com/tiingo/daily/{}".format(ticker)
    response = requests.get(url,headers=headers)
    return response.json()

def get_price_data(ticker):
    url = "https://api.tiingo.com/tiingo/daily/{}/prices".format(ticker)
    response = requests.get(url,headers=headers)
    return response.json()[0] #return result is array

    
'''
def get_hist_datta(ticker,sdate,edate):
    url = "https://api.tiingo.com/tiingo/daily/{}/prices?startDate={}}&endDate={}}".format(ticker)
'''
'''
a = get_meta_data('f')
print (a)
b = a.get('name')
print(b)


c = get_price_data('f')
print(c)
'''
id = 'amzn'
tempname = get_meta_data(id)
tempdata = get_price_data(id)


qs = watchlist.objects.all()
temp = qs.filter(ticker = id)
print(temp)
if not temp.exists():
    print('here')
    a = watchlist(ticker = str(id),
                    fname = tempname.get('name'),
                    open = tempdata.get('open'),
                    close = tempdata.get('close'),
                    volume = tempdata.get('volume'),
                    userid = 'User0'
                    )
    a.save()
    

