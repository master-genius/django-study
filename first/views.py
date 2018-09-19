
#import json as myjson
from django.shortcuts import render
from django.views import View
from django.http.response import HttpResponse,JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.mixins import PermissionRequiredMixin
import time
from .models import *
import os


class RootView(View):
    def __init__(self,):
        self.page_vars = {
            'user_info_cell':'<a href="/user/login/">Login</a>'
        }

    def dispatch(self, req, *args, **argv):
        if req.user.is_authenticated:
            self.page_vars['user_info_cell'] = req.session['username']

        ret = super(RootView, self).dispatch(req, *args, **argv)
        return ret

    def get(self, req):
        pass

    def post(self, req):
        pass


class IndexView(RootView):
    def dispatch(self, req, *args, **argv):
        #print(dir(req.session))
        print("fuck")
        print(self.page_vars)
        print('shit')
        ret = super(IndexView, self).dispatch(req, *args, **argv)
        return ret

    def get(self, req):
        return render(req, 'index.html', self.page_vars)

    def post(self, req):
        pass

class NewsCellView(RootView):
    def dispatch(self, req, *args, **argv):
        ret = super(NewsCellView, self).dispatch(req, *args, **argv)
        return ret

    def get(self, req):
        return render(req, 'index.html', self.page_vars)

    def post(self, req):
        return HttpResponse('post')

class NewsView(RootView):
    def dispatch(self, req, *args, **argv):
        ret = super(NewsView, self).dispatch(req, *args, **argv)
        return ret

    def get(self, req):
        return HttpResponse('index')

    def post(self, req):
        return HttpResponse('post')


class LoginView(RootView):
    def dispatch(self, req, *args, **argv):
        ret = super(LoginView, self).dispatch(req, *args, **argv)
        return ret

    def get(self, req):
        return render(req, 'login.html', self.page_vars)

    def post(self, req):
        return HttpResponse('post')


class RegisterView(RootView):
    def dispatch(self, req, *args, **argv):
        ret = super(LoginView, self).dispatch(req, *args, **argv)
        return ret

    def get(self, req):
        return render(req, 'register.html', self.page_vars)

    def post(self, req):
        return HttpResponse('post')


def index(req):
    return render(req, 'index.html')

def show_login(req):
    return render(req, 'login.html')

def show_register(req):
    return render(req, 'register.html')

def newscell(req):
    return render(req, 'newscell.html')

def runregister(req):
    username = req.POST['username']
    passwd = req.POST['passwd']
    user_email = req.POST['email']
    try:
        user = User.objects.create_user(username, user_email, passwd)
        user.save()
        return JsonResponse({
            'status':0,
            'info':'success'
        })
    except ValueError as e:
        return JsonResponse({
            'status':-1,
            'info':'Error: register failed'
        })

def runlogin(req):
    username = req.POST['username']
    passwd = req.POST['passwd']
    u = authenticate(req, username=username, password=passwd)
    if u is not None:
        req.session['user_id'] = u.id
        req.session['username'] = u.username
        login(req, u)
        return JsonResponse({
            'status':0,
            'info':'success'
        })
    else:
        return JsonResponse({
            'status':1,
            'info':'Error: login failed'
        })

@login_required(login_url='/user/login/')
def show_addnews(req):
    return render(req, 'addnews.html')

@login_required(login_url='/user/login/')
def add_news(req):
    #return JsonResponse(req.POST)
    ret_info = {'status':0, 'info':'success'}
    if req.method != 'POST':
        ret_info['status'] = -1;
        ret_info['errinfo'] = 'Error: It is not POST';
        return JsonResponse(ret_info)
    try:
        nw =News(
            news_title = req.POST['news_title'],
            news_content = req.POST['news_content'],
        )
        ret = nw.save()
    except ValueError as e:
        print(e)
        ret_info = {'status':1, 'info':'Error:failed'}
    except TypeError as e:
        print(e)
        ret_info = {'status':1, 'info':'Error:bad data'}
    
    return JsonResponse(ret_info)

def news_list(req):
    nlist = News.objects.order_by('-create_time').values('id','news_title')
    #funcs = dir(nlist)
    #return HttpResponse('<br>'.join(funcs))
    return JsonResponse([n for n in nlist],safe=False)

def get_news(req,news_id):
    '''
    try:
        one_news = News.objects.get(id=news_id)
        news_info = {
            'id' : one_news.id,
            'news_title' : one_news.news_title,
            'news_content' : one_news.news_content,
            'create_time' : one_news.create_time
        }
    except News.DoesNotExist:
        return JsonResponse({'error':'not exists'})
        
    funcs = dir(one_news)
    print(one_news.__dict__)
    return HttpResponse('<br>'.join(funcs))
    '''
    nw = News()
    news_info = nw.get_news(news_id, [
                    'id',
                    'news_title',
                    'news_content',
                    'create_time'
                ])
    if news_info:
        return JsonResponse(news_info)
    else:
        return JsonResponse({'status':-1, 'errinfo':'Failed to get news'})

def show_news(req, news_id):
    nw = News()
    news_info = nw.get_news(news_id, [
                    'id',
                    'news_title',
                    'news_content',
                    'create_time'
                ])
    if news_info == False:
        return render(req, '404.html')

    return render(req, 'show_news.html', news_info)

