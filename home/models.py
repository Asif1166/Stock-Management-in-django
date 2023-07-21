from django.db import models



class Category(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
       return self.name

class Stock(models.Model):
   category = models.ForeignKey(Category, on_delete=models.CASCADE ,blank=True, null=True)
   item_name = models.CharField(max_length=100, blank=True, null=True)
   quantity = models.CharField(max_length=100, blank=True, null=True)
   receive_quantity = models.CharField(max_length=100, blank=True, null=True)
   issue_quantity = models.CharField(max_length=100, blank=True, null=True)
   price = models.CharField(max_length=100, blank=True, null=True)
   vendor = models.CharField(max_length=100, blank=True, null=True)
   image = models.ImageField(upload_to="media/products")
   last_update = models.DateTimeField(auto_now_add=False, auto_now=True)
   export_to_CSV = models.BooleanField(default=False)

   def __str__(self):
       return self.item_name


class StockHistory(models.Model):
	category = models.ForeignKey(
	    Category, on_delete=models.CASCADE, blank=True, null=True)
	item_name = models.CharField(max_length=50, blank=True, null=True)
	quantity = models.IntegerField(default='0', blank=True, null=True)
	receive_quantity = models.IntegerField(default='0', blank=True, null=True)
	issue_quantity = models.IntegerField(default='0', blank=True, null=True)
	price = models.CharField(max_length=50, blank=True, null=True)
	created_by = models.CharField(max_length=50, blank=True, null=True)
	vendor = models.IntegerField(default='0', blank=True, null=True)
	last_updated = models.DateTimeField(
	    auto_now_add=False, auto_now=False, null=True)
