from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.IndexView.as_view()),
    path('addnews', views.NewsAdd.as_view()),
    path('runaddnews',views.NewsAdd.as_view()),
    #path('info', views.req_test),
    path('getnews/<int:news_id>',views.get_news),
    path('api/newslist', views.news_list),
    path('shownews/<int:news_id>', views.NewsShow.as_view()),
    #path('user/login/', auth_views.LoginView.as_view()),
    path('user/login/', views.LoginView.as_view()),
    path('user/runlogin/', views.LoginView.as_view()),
    
    path('user/register/', views.RegisterView.as_view()),
    path('user/runregister/', views.RegisterView.as_view()),
    path('user/logout/', views.user_logout),

    path('index', views.IndexView.as_view()),
    path('newslist', views.NewsListView.as_view()),
    
]

