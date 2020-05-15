from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Pizza_type, Pizza_price, Sub, Dinnerplatter, Pasta, Salad, Topping, Sub_extra, Order, Pizza_order, Sub_order, Dinnerplatter_order, Salad_order, Pasta_order


# Create your views here.
def index(request):
    if not request.user.is_authenticated:
        return render(request, "orders/login.html", {"mes": None})
    if request.user.is_superuser:
        superuser = True
    else:
        superuser = False
    reg = Pizza_type.objects.get(pk=1)
    sic = Pizza_type.objects.get(pk=2)
    regpizzas = Pizza_price.objects.filter(type=reg)
    sicpizzas = Pizza_price.objects.filter(type=sic)
    regpizzaprices = []
    sicpizzaprices = []
    for i in regpizzas:
        regpizzaprices.append(['{:03.2f}'.format(i.small), '{:03.2f}'.format(i.large)])
    for i in sicpizzas:
        sicpizzaprices.append(['{:03.2f}'.format(i.small), '{:03.2f}'.format(i.large)])
    cart = 0
    order = Order.objects.filter(user=request.user, status=1).first()
    myorders = Order.objects.filter(user = request.user, status=2).all()
    if order is not None:
        cart = len(order.pizzaorders.all()) + len(order.suborders.all()) + len(order.pastaorders.all()) + len(order.saladorders.all()) + len(order.dinnerorders.all())
    context = {
        "superuser": superuser,
        "pizzatypes": Pizza_type.objects.all(),
        "user": request.user,
        "cart": cart,
        "myorders": len(myorders),
        "regpizzas" : regpizzaprices,
        "sicpizzas" : sicpizzaprices,
        "toppings" : Topping.objects.all(),
        "subs" : Sub.objects.all(),
        "pastas" : Pasta.objects.all(),
        "salads" : Salad.objects.all(),
        "dinnerplatters" : Dinnerplatter.objects.all(),
        "extras" : Sub_extra.objects.all()
    }
    return render(request, "orders/index.html", context)

def login_v(request):
    if request.method == 'GET' and not request.user.is_authenticated:
        return render(request, "orders/login.html", {"mes": None})
    elif request.method == 'GET' and request.user.is_authenticated:
        return HttpResponseRedirect(reverse("index"))
    try:    
        username = request.POST["username"]
        password = request.POST["password"]
    except:
        return render(request, "orders/error.html", {"mes": "No username or password"})
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "orders/login.html", {"mes": "Invalid creditentials"})

def logout_v(request):
    if request.user.is_authenticated:    
        logout(request)
        return render(request, "orders/login.html", {"mes": "Logged out"})
    else:
        return render(request, "orders/login.html")

def register_v(request):
    if request.method == 'GET'and not request.user.is_authenticated:
        return render(request, "orders/register.html", {"mes": None})
    elif request.method == 'GET' and request.user.is_authenticated:
        return HttpResponseRedirect(reverse("index"))
    try:    
        username = request.POST["username"]
        password = request.POST["password"]
        confpassword = request.POST["confpassword"]
        email = request.POST["email"]
    except:
        return render(request, "orders/register.html", {"mes": "Missing creditentials"})
    if len(username.strip()) < 1 or password != confpassword:
        return render(request, "orders/register.html", {"mes": "Invalid creditentials"})
    if not username or not password or not confpassword or not email:
        return render(request, "orders/register.html", {"mes": "Missing creditentials"})
    user = User.objects.create_user(username, email, password)
    user.save()
    login(request, user)
    return HttpResponseRedirect(reverse("index"))

def pizzacheck(request):
    err = 0
    try:
        type = Pizza_type.objects.get(pk=request.POST["type"])
        size = int(request.POST["size"])
    except:
        err += 1
    toppings = 0
    try:
        top1 = Topping.objects.get(pk=request.POST["2top1"])
        toppings +=1
    except:
        top1 = None
    try:
        top2 = Topping.objects.get(pk=request.POST["2top2"])
        toppings +=1
    except:
        top2 = None
    try:
        top3 = Topping.objects.get(pk=request.POST["2top3"])
        toppings +=1
    except:
        top3 = None
    try:
        top4 = Topping.objects.get(pk=request.POST["2top4"])
        toppings +=1
    except:
        top4 = None
    tops = set()
    if top1 is not None:
        tops.add(top1)
    if top2 is not None and top2 in tops:
        err += 1
    else:
        tops.add(top2)
    if top3 is not None and top3 in tops:
        err += 1
    else:
        tops.add(top3)
    if top4 is not None and top4 in tops:
        err += 1
    else:
        tops.add(top4)
    return [err, toppings, top1, top2, top3, top4, size, type]

def pizzaorder(request):
    stuff = pizzacheck(request)
    if stuff[0] >0 :
        return JsonResponse({"succ": False, "error": "Invalid order"})
    price = Pizza_price.objects.filter(type=stuff[7], topping=stuff[1]).first()
    if stuff[6] == 1:
        fprice = price.small
    else:
        fprice = price.large   
    order = Order.objects.filter(user= request.user, status=1).first()
    if order is None:
        order = Order.objects.create(status=1, user=request.user)
    pizzaorder = Pizza_order.objects.create(type=stuff[7], top1=stuff[2], top2=stuff[3], top3=stuff[4], top4=stuff[5], size=stuff[6], price=fprice, order=order)
    return JsonResponse({"succ": True})

def suborder(request):
    try:
        type = Sub.objects.get(pk=request.POST["type"])
        size = int(request.POST["size"])
    except:
        return JsonResponse({"succ": False, "error": "Invalid order"})
    try:
        extcheese = int(request.POST["extcheese"])
    except:
        extcheese = 0
    try:
        checks = request.POST.getlist('checks[]')
    except:
        checks = []
    if request.POST["type"] != "10" and checks != []:
        return JsonResponse({"succ": False, "error": "Invalid order"})
    extras = [None, None, None, None]
    for n in range(len(checks)):
        extras[n] = Sub_extra.objects.get(pk=checks[n])
    fprice = 0
    if extcheese == 1:
        extras[3] = Sub_extra.objects.get(pk=1)
        fprice = 0.5
    if size == 1:
        fprice += type.small + len(checks)* 0.5
    else:
        fprice += type.large + len(checks)* 0.5
    order = Order.objects.filter(user= request.user, status=1).first()
    if order is None:
        order = Order.objects.create(status=1, user=request.user)
    suborder = Sub_order.objects.create(type=type, ext1=extras[0], ext2=extras[1], ext3=extras[2], ext4=extras[3], size=size, price=fprice, order=order)
    return JsonResponse({"succ": True})

def pastaorder(request):
    try:
        type = Pasta.objects.get(pk=request.POST["type"])
    except:
        return JsonResponse({"succ": False, "error": "Invalid order"})
    if type is None:
        return JsonResponse({"succ": False, "error": "Invalid order"})
    order = Order.objects.filter(user= request.user, status=1).first()
    if order is None:
        order = Order.objects.create(status=1, user=request.user)
    pastaorder = Pasta_order.objects.create(type=type, order=order)
    return JsonResponse({"succ": True})

def saladorder(request):
    try:
        type = Salad.objects.get(pk=request.POST["type"])
    except:
        return JsonResponse({"succ": False, "error": "Invalid order"})
    if type is None:
        return JsonResponse({"succ": False, "error": "Invalid order"})
    order = Order.objects.filter(user= request.user, status=1).first()
    if order is None:
        order = Order.objects.create(status=1, user=request.user)
    saladorder = Salad_order.objects.create(type=type, order=order)
    return JsonResponse({"succ": True})

def dinnerorder(request):
    try:
        type = Dinnerplatter.objects.get(pk=request.POST["type"])
    except:
        return JsonResponse({"succ": False, "error": "Invalid order"})
    if type is None:
        return JsonResponse({"succ": False, "error": "Invalid order"})
    try:
        size = int(request.POST["size"])
    except:
        return JsonResponse({"succ": False, "error": "Invalid order"})
    if size <1 or size > 2:
        return JsonResponse({"succ": False, "error": "Invalid order"})
    order = Order.objects.filter(user= request.user, status=1).first()
    if order is None:
        order = Order.objects.create(status=1, user=request.user)
    if size ==1:    
        dinnerorder = Dinnerplatter_order.objects.create(type=type, size=size, price = type.small, order=order)
    else:
        dinnerorder = Dinnerplatter_order.objects.create(type=type, size=size, price = type.large, order=order)
    return JsonResponse({"succ": True})    

def allorders(request):
    if not request.user.is_superuser:
        return HttpResponseRedirect(reverse("index"))
    superuser = True
    order = Order.objects.filter(user=request.user, status=1).first()
    cart = 0
    if order is not None:
        pizzaorders = order.pizzaorders.all()
        suborders = order.suborders.all()
        saladorders = order.saladorders.all()
        pastaorders = order.pastaorders.all()
        dinnerorders = order.dinnerorders.all()
        cart = len(pizzaorders) + len(suborders) + len(pastaorders) + len(saladorders) + len(dinnerorders) 
    ongoing = Order.objects.filter(user = request.user, status=2).all() 
    myorders = len(ongoing)
    allorders = Order.objects.filter(status=2).all()
    orders = []
    for a in allorders:
        pizzaorders = a.pizzaorders.all()
        suborders = a.suborders.all()
        saladorders = a.saladorders.all()
        pastaorders = a.pastaorders.all()
        dinnerorders = a.dinnerorders.all()
        sum = 0
        for i in pizzaorders:
            sum += i.price
        for i in suborders:
            sum += i.price
        for i in pastaorders:
            sum += i.type.price
        for i in saladorders:
            sum += i.type.price
        for i in dinnerorders:
            sum += i.price
        orders.append(['{:03.2f}'.format(sum), pizzaorders, suborders, pastaorders, saladorders, dinnerorders, a.user, a.id])
    context = {
        "orders": orders,
        "myorders": myorders,
        "cart": cart,
        "superuser": superuser
    }
    return render(request, "orders/allorders.html", context)

def myorders(request):
    if request.user.is_superuser:
        superuser = True
    else:
        superuser = False
    order = Order.objects.filter(user=request.user, status=1).first()
    cart = 0
    if order is not None:
        pizzaorders = order.pizzaorders.all()
        suborders = order.suborders.all()
        saladorders = order.saladorders.all()
        pastaorders = order.pastaorders.all()
        dinnerorders = order.dinnerorders.all()
        cart = len(pizzaorders) + len(suborders) + len(pastaorders) + len(saladorders) + len(dinnerorders) 
    ongoing = Order.objects.filter(user = request.user, status=2).all() 
    myorders = len(ongoing)
    allongoing = []
    for i in ongoing:
        pizzaorders = i.pizzaorders.all()
        suborders = i.suborders.all()
        saladorders = i.saladorders.all()
        pastaorders = i.pastaorders.all()
        dinnerorders = i.dinnerorders.all()
        sum = 0
        for i in pizzaorders:
            sum += i.price
        for i in suborders:
            sum += i.price
        for i in pastaorders:
            sum += i.type.price
        for i in saladorders:
            sum += i.type.price
        for i in dinnerorders:
            sum += i.price
        allongoing.append(['{:03.2f}'.format(sum), pizzaorders, suborders, pastaorders, saladorders, dinnerorders])
    completed = Order.objects.filter(user = request.user, status=3).all()
    allcompleted= []
    for i in completed:
        pizzaorders = i.pizzaorders.all()
        suborders = i.suborders.all()
        saladorders = i.saladorders.all()
        pastaorders = i.pastaorders.all()
        dinnerorders = i.dinnerorders.all()
        sum = 0
        for i in pizzaorders:
            sum += i.price
        for i in suborders:
            sum += i.price
        for i in pastaorders:
            sum += i.type.price
        for i in saladorders:
            sum += i.type.price
        for i in dinnerorders:
            sum += i.price
        allcompleted.append(['{:03.2f}'.format(sum), pizzaorders, suborders, pastaorders, saladorders, dinnerorders])
    context = {
        "superuser": superuser,
        "ongoing": allongoing,
        "completed": allcompleted,
        "myorders": myorders,
        "cart": cart
    }
    return render(request, "orders/myorders.html", context)

def cart(request):
    if request.user.is_superuser:
        superuser = True
    else:
        superuser = False        
    order = Order.objects.filter(user=request.user, status=1).first()
    myorders = Order.objects.filter(user = request.user, status=2).all()
    empty = True
    sum = 0
    cart = 0
    if order is not None:
        pizzaorders = order.pizzaorders.all()
        suborders = order.suborders.all()
        saladorders = order.saladorders.all()
        pastaorders = order.pastaorders.all()
        dinnerorders = order.dinnerorders.all()
        cart = len(pizzaorders) + len(suborders) + len(pastaorders) + len(saladorders) + len(dinnerorders) 
        if cart > 0:
            empty = False
        for i in pizzaorders:
            sum += i.price
        for i in suborders:
            sum += i.price
        for i in pastaorders:
            sum += i.type.price
        for i in saladorders:
            sum += i.type.price
        for i in dinnerorders:
            sum += i.price
    else:
        pizzaorders = None
        suborders = None
        saladorders = None
        pastaorders = None
        dinnerorders = None
    context = {
        "superuser": superuser,
        "empty": empty,
        "myorders": len(myorders),
        "cart": cart,
        "sum": '{:03.2f}'.format(round(sum, 2)), 
        "pizzaorders": pizzaorders,
        "suborders": suborders,
        "saladorders": saladorders,
        "pastaorders": pastaorders,
        "dinnerorders": dinnerorders
    }        
    return render(request, "orders/cart.html", context)

def pizzaprice(request):
    stuff = pizzacheck(request)
    if stuff[0] >0 :
        return JsonResponse({"succ": False, "error": "Invalid order"})
    price = Pizza_price.objects.filter(type=stuff[7], topping=stuff[1]).first()
    if stuff[6] == 1:
        fprice = price.small
    else:
        fprice = price.large
    return JsonResponse({"succ": True, "price": '{:03.2f}'.format(fprice)})

def subprice(request):
    try:
        type = Sub.objects.get(pk=request.POST["type"])
        size = int(request.POST["size"])
    except:
        return JsonResponse({"succ": False, "error": "Invalid order"})
    try:
        extcheese = int(request.POST["extcheese"])
    except:
        extcheese = 0
    try:
        checks = request.POST.getlist('checks[]')
    except:
        checks = []
    if request.POST["type"] != "10" and checks != []:
        return JsonResponse({"succ": False, "error": "Invalid order"})
    extras = [None, None, None, None]
    for n in range(len(checks)):
        extras[n] = Sub_extra.objects.get(pk=checks[n])
    fprice = 0
    if extcheese == 1:
        extras[3] = Sub_extra.objects.get(pk=1)
        fprice = 0.5
    if size == 1:
        fprice += type.small + len(checks)* 0.5
    else:
        fprice += type.large + len(checks)* 0.5
    return JsonResponse({"succ": True, "price": '{:03.2f}'.format(fprice)})

def pastaprice(request):
    try:
        type = Pasta.objects.get(pk=request.POST["type"])
    except:
        return JsonResponse({"succ": False, "error": "Invalid order"})
    return JsonResponse({"succ": True, "price": '{:03.2f}'.format(type.price)})

def saladprice(request):
    try:
        type = Salad.objects.get(pk=request.POST["type"])
    except:
        return JsonResponse({"succ": False, "error": "Invalid order"})
    return JsonResponse({"succ": True, "price": '{:03.2f}'.format(type.price)})

def dinnerprice(request):
    try:
        type = Dinnerplatter.objects.get(pk=request.POST["type"])
        size = int(request.POST["size"])
    except:
        return JsonResponse({"succ": False, "error": "Invalid order"})
    if size == 1:
        price = type.small
    else:
        price = type.large
    return JsonResponse({"succ": True, "price": '{:03.2f}'.format(price)})

def removeorder(request):
    err = 0
    try:
        lista = request.POST["id"].split("-")
        id = int(lista[1])
    except:
        err += 1
    try:
        if lista[0] == 'pi':
            order = Pizza_order.objects.get(pk=id)
        elif lista[0] == "pa":
            order = Pasta_order.objects.get(pk=id)
        elif lista[0] == "su":
            order = Sub_order.objects.get(pk=id)
        elif lista[0] == "sa":
            order = Salad_order.objects.get(pk=id)
        elif lista[0] == "di":
            order = Dinnerplatter_order.objects.get(pk=id)
    except:
        err += 1
    if order.order.user != request.user:
        err += 1
    if err == 0:
        order.delete()
        fullorder = Order.objects.filter(user=request.user, status=1).first()
        sum = 0
        pizzaorders = fullorder.pizzaorders.all()
        suborders = fullorder.suborders.all()
        saladorders = fullorder.saladorders.all()
        pastaorders = fullorder.pastaorders.all()
        dinnerorders = fullorder.dinnerorders.all()
        cart = len(pizzaorders) + len(suborders) + len(pastaorders) + len(saladorders) + len(dinnerorders) 
        if cart > 0:
            empty = False
            for i in pizzaorders:
                sum += i.price
            for i in suborders:
                sum += i.price
            for i in pastaorders:
                sum += i.type.price
            for i in saladorders:
                sum += i.type.price
            for i in dinnerorders:
                sum += i.price
        else:
            empty = True
            fullorder.delete()
        return JsonResponse({"succ": True, "empty": empty, "price": '{:03.2f}'.format(sum)})
    else:
        return JsonResponse({"succ": False, "error": "Invalid request"})

def cancelorder(request):
    order = Order.objects.filter(user = request.user, status = 1)
    if order is None:
        return JsonResponse({"succ": False, "error": "No order to cancel"})
    order.delete()
    return JsonResponse({"succ": True})

def finalizeorder(request):
    order = Order.objects.filter(user = request.user, status = 1).first()
    if order is None:
        return JsonResponse({"succ": False, "error": "No items in cart"})
    order.status = 2
    order.save()
    return JsonResponse({"succ": True})

def completeorder(request):
    if not request.user.is_superuser:
        return JsonResponse({"succ": False, "error": "No authorized"})
    try:
        order = Order.objects.get(pk=request.POST["id"])
    except:
        return JsonResponse({"succ": False, "error": "Invalid order"})
    if order is None:
        return JsonResponse({"succ": False, "error": "No order"})
    if order.user == request.user:
        myorder = True
    else:
        myorder = False
    order.status = 3
    order.save()
    allorders = Order.objects.filter(status = 2).all()
    if len(allorders) == 0:
        empty = True
    else:
        empty = False
    return JsonResponse({"succ": True, "empty": empty, "myorder": myorder})
