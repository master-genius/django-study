import json as myjson
from django.shortcuts import render
from django.views import View
from django.http.response import HttpResponse,JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.mixins import PermissionRequiredMixin
import time
from .models import *

def index(req):
    return HttpResponse(time.ctime())

def req_test(req):
    info = {
        'method' : req.method,
        'encoding' : req.encoding,
        'pathinfo' : req.path_info,
        'content_type' : req.content_type,
        'remote_addr' : req.META['REMOTE_ADDR'],
        'get_params' : req.META['QUERY_STRING'],
    }
    return JsonResponse(info)

def show_login(req):
    return render(req, 'login.html')

def show_register(req):
    return render(req, 'register.html')

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


class NewsView(View):
    def __init__(self, ):
        self.route = ''
        self.route_get_dict = {
            'show':self.ShowNews,
            'newslist':self.NewsList,
        }
        
        self.route_post_dict = {
            'addnews':self.AddNews,
            'updnews':self.UpdateNews,
        }

    def get_route(self, req):
        url_list = req.path_info.strip('/').split('/')
        if len(url_list) > 1:
            self.route = url_list[1]
        print(self.route)

    def dispatch(self, req, *args, **argv):
        self.get_route(req)
        ret = super(NewsView, self).dispatch(req, *args, **argv)
        return ret
    
    def get(self, req):
        try:
            return self.route_get_dict[self.route](req)
        except KeyError as e:
            return JsonResponse({
                    'status':-1,'errinfo':'not found'
                   })

    def post(self, req):
        try:
            return self.route_post_dict[self.route](req)
        except KeyError as e:
            return JsonResponse({
                    'status':-1, 'errinfo':'post not found' 
                   })

    def NewsList(self, req):
        nlist = News.objects.order_by('-create_time').values('id','news_title')
        return JsonResponse([n for n in nlist],safe=False)

    def ShowNews(self, req):
        pass


    def AddNews(self, req):
        pass

    def UpdateNews(self, req):
        pass



'''
class Test(View):
    def dispatch(self, req, *args, **argv):
        ret = super(Test, self).dispatch(req, *args, **argv)
        return ret

    def get(self, req):
        return HttpResponse(
                    ' '.join([req.method, time.ctime()])
               )

    def post(self, req):
        return HttpResponse('post')
'''

