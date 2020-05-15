from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_v, name="login"),
    path("logout", views.logout_v, name="logout"),
    path("register", views.register_v, name="register"),
    path("pizzaorder", views.pizzaorder, name="pizzaorder"),
    path("suborder", views.suborder, name="suborder"),
    path("pastaorder", views.pastaorder, name="pastaorder"),
    path("saladorder", views.saladorder, name="saladorder"),
    path("dinnerorder", views.dinnerorder, name="dinnerorder"),
    path("pizzaprice", views.pizzaprice, name="pizzaprice"),
    path("subprice", views.subprice, name="subprice"),
    path("pastaprice", views.pastaprice, name="pastaprice"),
    path("saladprice", views.saladprice, name="saladprice"),
    path("dinnerprice", views.dinnerprice, name="dinnerprice"),
    path("cart", views.cart, name="cart"),
    path("removeorder", views.removeorder, name="removeorder"),
    path("cancelorder", views.cancelorder, name="cancelorder"),
    path("finalizeorder", views.finalizeorder, name="finalizeorder"),
    path("myorders", views.myorders, name="myorders"),
    path("allorders", views.allorders, name="allorders"),
    path("completeorder", views.completeorder, name="completeorder")
]

