from django.db import models
from django.conf import settings

# Create your models here.
class Pizza_type(models.Model):
    name = models.CharField(max_length=64)

    def __str__(self):
        return self.name

class Pizza_price(models.Model):
    type = models.ForeignKey(Pizza_type, on_delete=models.CASCADE, related_name="prices")
    topping = models.IntegerField()
    small = models.FloatField()
    large = models.FloatField()

    def __str__(self):
        return f"{self.type} with {self.topping} extra topping(s)"

class Sub(models.Model):
    name = models.CharField(max_length=64)
    small = models.FloatField(blank=True, null=True)
    large = models.FloatField()

    def __str__(self):
        return self.name 

class Dinnerplatter(models.Model):
    name = models.CharField(max_length=64)
    small = models.FloatField()
    large = models.FloatField()

    def __str__(self):
        return self.name 

class Pasta(models.Model):
    name = models.CharField(max_length=64)
    price = models.FloatField()

    def __str__(self):
        return self.name

class Salad(models.Model):
    name = models.CharField(max_length=64)
    price = models.FloatField()

    def __str__(self):
        return self.name

class Topping(models.Model):
    name = models.CharField(max_length=64)

    def __str__(self):
        return self.name

class Sub_extra(models.Model):
    name = models.CharField(max_length=64)

    def __str__(self):
        return self.name

class Order(models.Model):
    status = models.IntegerField()
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="orders")

    def __str__(self):
        return f"Order by {self.user} with status {self.status}"

class Pizza_order(models.Model):
    type = models.ForeignKey(Pizza_type, on_delete=models.CASCADE, related_name="porders")
    top1 = models.ForeignKey(Topping, on_delete=models.CASCADE, related_name="t1orders", blank=True, null=True)
    top2 = models.ForeignKey(Topping, on_delete=models.CASCADE, related_name="t2orders", blank=True, null=True)
    top3 = models.ForeignKey(Topping, on_delete=models.CASCADE, related_name="t3orders", blank=True, null=True)
    top4 = models.ForeignKey(Topping, on_delete=models.CASCADE, related_name="t4orders", blank=True, null=True)
    size = models.IntegerField()
    price = models.FloatField()
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="pizzaorders")

    def __str__(self):
        if self.size == 1:
            return f"Small {self.type} with {self.top1}, {self.top2}, {self.top3}, {self.top4}"
        else:
            return f"Large {self.type} with {self.top1}, {self.top2}, {self.top3}, {self.top4}"

class Sub_order(models.Model):
    type = models.ForeignKey(Sub, on_delete=models.CASCADE, related_name="sorders")
    ext1 = models.ForeignKey(Sub_extra, on_delete=models.CASCADE, related_name="e1orders", blank=True, null=True)
    ext2 = models.ForeignKey(Sub_extra, on_delete=models.CASCADE, related_name="e2orders", blank=True, null=True)
    ext3 = models.ForeignKey(Sub_extra, on_delete=models.CASCADE, related_name="e3orders", blank=True, null=True)
    ext4 = models.ForeignKey(Sub_extra, on_delete=models.CASCADE, related_name="e4orders", blank=True, null=True)
    size = models.IntegerField()
    price = models.FloatField()
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="suborders")
    
    def __str__(self):
        if self.size == 1:
            return f"Small {self.type} sub with {self.ext1}, {self.ext2}, {self.ext3}, {self.ext4}"
        else:
            return f"Large {self.type} sub with {self.ext1}, {self.ext2}, {self.ext3}, {self.ext4}"

class Dinnerplatter_order(models.Model):
    type = models.ForeignKey(Dinnerplatter, on_delete=models.CASCADE, related_name="dorders")
    size = models.IntegerField()
    price = models.FloatField()
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="dinnerorders")

    def __str__(self):
        if self.size == 1:
            return f"Small {self.type} dinner platter"
        else:
            return f"Large {self.type} dinner platter"

class Pasta_order(models.Model):
    type = models.ForeignKey(Pasta, on_delete=models.CASCADE, related_name="porders")
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="pastaorders")

    def __str__(self):
        return self.type.name

class Salad_order(models.Model):
    type = models.ForeignKey(Salad, on_delete=models.CASCADE, related_name="saorders")
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="saladorders")

    def __str__(self):
        return self.type.name