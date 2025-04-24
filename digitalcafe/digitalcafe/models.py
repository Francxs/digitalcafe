from django.db import models
from django.utils import timezone

# Create your models here.
class item(models.Model):
    app_label = 'digitalcafe'
    item_name = models.CharField(max_length=100)
    item_price = models.DecimalField(max_digits=6, decimal_places=2)
    stock_quantity = models.IntegerField()
    objects = models.Manager()

    def getPrice(self):
       return self.item_price

    def getName(self):
       return self.item_name
    
    def getQuantity(self):
        return self.stock_quantity
    
    def __str__(self):
       return str(self.pk) + ": " + self.item_name
    
class order(models.Model):
    app_label = 'digitalcafe'
    total_amount = models.DecimalField(max_digits=12, decimal_places=2)
    order_date = models.DateField(default=timezone.now)
    class PaymentType(models.TextChoices):
        CASH = '1', ('CASH')
        CARD = '2', ('Credit Card')
    payment_type = models.CharField(
        max_length=1, 
        choices=PaymentType.choices, 
        default=PaymentType.CASH,
    )
    objects = models.Manager()

    def getPaymentType(self):
        return self.payment_type

    def getDate(self): 
        return self.order_date

    def getTotal(self):
        return str(self.total_amount)   # Changed from self.item_price

    def __str__(self):
        return str(self.pk)+": "+str(self.order_date)+", "+self.payment_type+". "+str(self.total_amount)+"."

class order_item(models.Model):
    app_label = 'digitalcafe'
    item_id = models.ForeignKey(item, on_delete = models.CASCADE)
    order_id = models.ForeignKey(order, on_delete = models.CASCADE)
    line_total = models.DecimalField(max_digits=12, decimal_places=2)
    quantity = models.IntegerField()
    objects = models.Manager()

    def getLineTotal(self):
        return str(self.line_total)  # Changed from self.item_price

    def getQuantity(self):
        return str(self.quantity)

    def __str__(self):
        return str(self.pk)+": "+str(self.order_id.pk)+", "+self.item_id.item_name
