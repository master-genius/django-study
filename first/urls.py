from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.index),
    path('addnews', views.add_news),
    path('show_addnews',views.show_addnews),
    path('info', views.req_test),
    path('getnews/<int:news_id>',views.get_news),
    path('newslist', views.news_list),
    path('shownews/<int:news_id>', views.show_news),
    #path('user/login/', auth_views.LoginView.as_view()),
    path('user/login/', views.show_login),
    path('user/runlogin/', views.runlogin),
    
    path('user/register/', views.show_register),
    path('user/runregister/', views.runregister),
    path('fuck/newslist', views.NewsView.as_view()),
    path('fuck/addnews', views.NewsView.as_view()),
    path('fuck/show', views.NewsView.as_view()),
    path('fuck/updnews', views.NewsView.as_view()),
]

