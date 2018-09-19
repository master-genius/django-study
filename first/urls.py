from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.IndexView.as_view()),
    path('addnews', views.add_news),
    path('show_addnews',views.show_addnews),
    #path('info', views.req_test),
    path('getnews/<int:news_id>',views.get_news),
    path('newslist', views.news_list),
    path('shownews/<int:news_id>', views.show_news),
    #path('user/login/', auth_views.LoginView.as_view()),
    path('user/login/', views.LoginView.as_view()),
    path('user/runlogin/', views.runlogin),
    
    path('user/register/', views.RegisterView.as_view()),
    path('user/runregister/', views.runregister),

    path('index', views.IndexView.as_view()),
    path('newscell', views.NewsCellView.as_view()),
]

