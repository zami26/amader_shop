from django.contrib import admin
from .models import Product, Customer, Cart, Payment, OrderPlaced
from django.utils.html import format_html
from django.urls import reverse
from django.contrib.auth.models import Group

admin.site.site_header = "Dairy Baba"
admin.site.site_title = "This is Dairy Baba"
admin.site.index_title = "Welcome to Dairy Baba's Custom Admin Panel"

@admin.register(Product)
class ProductModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'discounted_price', 'category', 'product_image']

@admin.register(Customer)
class CustomerModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'mobile', 'locality', 'city', 'division', 'zipcode']

@admin.register(Cart)
class CartModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'product', 'quantity']
    def product(self, obj):
        if obj.product is None:
            return "No product"
        link = reverse("admin:app_product_change", args=[obj.product.pk])
        return format_html('<a href="{}">{}</a>', link, obj.product.title)

@admin.register(Payment)
class PaymentModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'amount', 'payment_status', 'payment_id', 'paid']

@admin.register(OrderPlaced)
class OrderPlacedModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'customer', 'product', 'quantity', 'ordered_date', 'status', 'payment']
    def customer(self, obj):
        if obj.customer is None:
            return "No customer"
        link = reverse("admin:app_customer_change", args=[obj.customer.pk])
        return format_html('<a href="{}">{}</a>', link, obj.customer.name)

    def product(self, obj):
        if obj.product is None:
            return "No product"
        link = reverse("admin:app_product_change", args=[obj.product.pk])
        return format_html('<a href="{}">{}</a>', link, obj.product.title)

    def payment(self, obj):
        if obj.payment is None:
            return "No payment"
        link = reverse("admin:app_payment_change", args=[obj.payment.pk])
        return format_html('<a href="{}">{}</a>', link, obj.payment_id)

admin.site.unregister(Group)