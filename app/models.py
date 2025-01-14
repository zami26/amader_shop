from django.db import models
from django.contrib.auth.models import User

CATEGORY_CHOICE = (
    ('CR','Curd'),
    ('MK','Milk'),
    ('LS','Lassi'),
    ('MS','Milkshake'),
    ('PN','Panner'),
    ('GH','Ghee'),
    ('CZ','Cheese'),
    ('IC','Ice-creams'),

)
class Product(models.Model):
    title = models.CharField(max_length=100)
    selling_price = models.FloatField()
    discounted_price = models.FloatField()
    description = models.TextField()
    composition = models.TextField(default='')
    prodapp = models.TextField(default='')
    category = models.CharField(choices=CATEGORY_CHOICE, max_length=5)
    product_image = models.ImageField(upload_to='product')

    def __str__(self):
        return self.title


DIVISION_CHOICES = (
    ('Dhaka', 'Dhaka'),
    ('Chattogram', 'Chattogram'),
    ('Rajshahi', 'Rajshahi'),
    ('Khulna', 'Khulna'),
    ('Barishal', 'Barishal'),
    ('Sylhet', 'Sylhet'),
    ('Rangpur', 'Rangpur'),
    ('Mymensingh', 'Mymensingh'),
)

class Customer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    mobile = models.CharField(max_length=15)  # Changed to CharField to store phone numbers with leading zeros
    locality = models.CharField(max_length=200)
    city = models.CharField(max_length=200)
    zipcode = models.IntegerField()
    division = models.CharField(choices=DIVISION_CHOICES, max_length=100)

    def __str__(self):
        return self.name


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)  # Changed to PositiveIntegerField

    @property
    def total_cost(self):
        return self.quantity * self.product.discounted_price


STATUS_CHOICE = (
    ('Accepted', 'Accepted'),
    ('Packed', 'Packed'),
    ('On The Way', 'On The Way'),
    ('Delivered', 'Delivered'),
    ('Cancel', 'Cancel'),
    ('Pending', 'Pending'),
)

class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.FloatField()
    transaction_id = models.CharField(max_length=100, blank=True, null=True)  # Renamed
    payment_status = models.CharField(max_length=100, blank=True, null=True)
    payment_id = models.CharField(max_length=100, blank=True, null=True)
    currency = models.CharField(max_length=10, default='BDT')  # Added
    paid = models.BooleanField(default=False)


class OrderPlaced(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    ordered_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, choices=STATUS_CHOICE, default='Pending')
    payment = models.ForeignKey(Payment, on_delete=models.CASCADE, null=True, blank=True)
    @property
    def total_cost(self):
        return self.quantity * self.product.discounted_price

class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)