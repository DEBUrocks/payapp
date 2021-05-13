from django.urls import path
from . import views

urlpatterns = [
    path('', views.home,name="home"),
    path('transaction/', views.userTrans,name="trans"),
    path('tlist/', views.userTransList,name="translist"),
    path('login/', views.loginPage,name="login"),
    path('logout/', views.logoutUser,name="logout"),
    path('register/', views.registerPage,name="reg"),
]
