from django.db import models
from django.conf import settings
from django.utils import timezone
from django.contrib.auth.models import User

# class Product(models.Model):
#     name = models.CharField(max_length=100)
#     price = models.IntegerField(default=0)  # cents
#     file = models.FileField(upload_to="product_files/", blank=True, null=True)
#     url = models.URLField()

#     def __str__(self):
#         return self.name
    
#     def get_display_price(self):
#         return "{0:.2f}".format(self.price / 100)

class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='')

    def __str__(self):
        return self.name
        
    def get_display_price(self):
        return "{0:.2f}".format(self.price / 100)



class CartItem(models.Model):
	product = models.ForeignKey(Product, on_delete=models.CASCADE)
	quantity = models.PositiveIntegerField(default=0)
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	date_added = models.DateTimeField(default=timezone.now)

	def __str__(self):
		return f'{self.quantity} x {self.product.name}'
