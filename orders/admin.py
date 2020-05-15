from django.contrib import admin
from .models import Pizza_type, Pizza_price, Sub, Dinnerplatter, Pasta, Salad, Topping, Sub_extra, Order, Pizza_order, Sub_order, Dinnerplatter_order, Salad_order, Pasta_order

# Register your models here.
admin.site.register(Pizza_type)
admin.site.register(Pizza_price)
admin.site.register(Sub)
admin.site.register(Sub_extra)
admin.site.register(Dinnerplatter)
admin.site.register(Pasta)
admin.site.register(Salad)
admin.site.register(Topping)
admin.site.register(Order)
admin.site.register(Pizza_order)
admin.site.register(Sub_order)
admin.site.register(Dinnerplatter_order)
admin.site.register(Salad_order)
admin.site.register(Pasta_order)
