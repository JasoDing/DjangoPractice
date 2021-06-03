import os,django,datetime
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")
django.setup()

from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.forms import inlineformset_factory
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages


from stocks.forms import *
from stocks.templates.forms import UserRegisterForm
from stocks.models import *
from stocks.tiingo import get_meta_data, get_price_data
from stocks.webserivce import *
import pandas as pd
import json

#from django.http import HttpResponse



def index(request):
    if request.method == 'POST':
        tick = request.POST['ssearch']
        print('search...')
        return HttpResponseRedirect('ticker/'+tick)

    return render(request, 'templates/index.html')

def ticker(request, id):
    context = {}
    context['ticker'] = id
    form = TickForm()
    print('Loading...')
    '''
    now = datetime.date(datetime.now())
    qs = RecentStockData.objects.all()
    qs = qs.filter(ticker = id, date = now)
    if qs.exists():
    '''
    if request.method == "POST":
        print('POST!!!...')
        tick = request.POST['lst']
        form = TickForm(request.POST)
        if form.is_valid():
            ticker = request.POST['ticker']
        '''
        qs = watchlist.objects.all()
        temp = qs.filter(ticker = tick)
        '''
        print('ticker', tick)
        #if not temp.exists():
        tempname = get_meta_data(tick)
        tempdata = get_price_data(tick)
        a = watchlist(ticker = str(tick),fname = tempname.get('name'),open = tempdata.get('open'),close = tempdata.get('close'),volume = tempdata.get('volume'),userid = 'User0')
        a.save()
        print('success')
        return render (request, 'templates/dashboard.html')

    else:
        form = TickForm()
    context['meta'] = get_meta_data(id)
    context['price'] = get_price_data(id)
    
    return render(request, 'templates/ticker.html',context)#,{'form':form})

def account(request):
    print('Loading...')
    sq = watchlist.objects.all()
    print(sq)
    return render(request, 'templates/dashboard.html',{'data':sq})

def test(request):
    print('Loading...')
    context={}
    return render(request,'templates/test.html')

def refresh(request):
    print('Loading...')
    context={}
    return render(request,'templates/frame.html')

def registerPg(request):
    print('Loading...')
    if request.method == 'POST':
        print('POST!!!...')
        form = UserRegisterForm(request.POST)
        #messages.warning(request,f'is valid check?')
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username') 
            messages.success(request, f'Account created for {username}.')
            
            return render(request, 'templates/index.html') 
    else:
        form = UserRegisterForm()
        messages.error(request,f'Input Invalid.')
    context = {'form': form}
    return render(request, 'templates/register.html',context)

def loginPg(request):
    print('Loading...')
    context = {}
    return render(request, 'templates/login.html')

def about(request):
    if request.method == 'POST':
        print('POST!!!...')
        inputname = request.POST['contact_name']
        inputemail = request.POST['contact_email']
        inputsubject = request.POST['contact_subject']
        a = contactinfo(name = inputname, email = inputemail, subject = inputsubject)
        a.save()
        messages.success(request, f'Your message have been saved. We will contact you ASAP.')
    context={}
    return render(request,'templates/about.html')
        
def delete(request, id):
    print('Loading...')
    qs = watchlist.objects.all()
    print('id',id)
    #print('QS',qs)
    tick = str(id)
    item = qs.filter(ticker = id)
    print('CURRENT item :',item)

    if request.method == "POST":
        print('POST!!!...DELETE=======')
        item = qs.filter(ticker = id)
        item.delete()
        
        print('DELETED---------')
        return redirect('http://127.0.0.1:8000/stocks/account/')

    context = {'stock': item }
    return render(request,'templates/delete.html',context)

def suggest(request):
    print('Loading...suggest...')
    if request.method == "POST":
        print('POST!!!...')
        inputtick = request.POST['input_ticker']
        inputstdate = request.POST['input_startdate']
        inputeddate = request.POST['input_enddate']
        inputmoney = request.POST['input_cash']
        print('getting result...')
        res = run(inputtick,inputstdate,inputeddate,inputmoney)
        df = pd.DataFrame(res)
        jsonres = df.to_json()
        print('result:')
        print(df)
        data = []
        data = json.loads(jsonres)
        hf = df.to_html()
        #print('data',data)
        context = {'res':hf}
        return render(request,'templates/suggestion.html',context)

    context= {}
    return render(request,'templates/suggestion.html',context)