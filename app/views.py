from django.shortcuts import render,redirect
from django.views import View
from django.contrib import messages
from django.contrib.auth.views import LogoutView
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
import json,requests,uuid
from uuid import uuid4
from django.db.models import Q
from django.conf import settings
from .models import Product,Customer,Cart,Payment,OrderPlaced,Wishlist
from .forms import CustomerRegistrationForm,CustomerProfileForm

@login_required
def home(request):
    totalitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user = request.user))
    item_in_wishlist = 0
    if request.user.is_authenticated:
        item_in_wishlist = len(Wishlist.objects.filter(user = request.user))
    return render(request, 'app/home.html',locals())

@login_required
def about(request):
    totalitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user = request.user))
    item_in_wishlist = 0
    if request.user.is_authenticated:
        item_in_wishlist = len(Wishlist.objects.filter(user = request.user))
    return render(request, 'app/about.html',locals())

@login_required
def contact(request):
    totalitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user = request.user))
    item_in_wishlist = 0
    if request.user.is_authenticated:
        item_in_wishlist = len(Wishlist.objects.filter(user = request.user))
    return render(request, 'app/contact.html',locals())

@method_decorator(login_required,name='dispatch')
class CategoryView(View):
    def get(self, request, val):
        totalitem = 0
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user = request.user))
        item_in_wishlist = 0
        if request.user.is_authenticated:
            item_in_wishlist = len(Wishlist.objects.filter(user = request.user))
        product = Product.objects.filter(category=val)
        title = Product.objects.filter(category=val).values('title')
        return render(request, "app/category.html", locals())

@method_decorator(login_required,name='dispatch')
class CategoryTitle(View):
    def get(self, request, val):
        totalitem = 0
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user = request.user))
        item_in_wishlist = 0
        if request.user.is_authenticated:
            item_in_wishlist = len(Wishlist.objects.filter(user = request.user))
        product = Product.objects.filter(title=val)
        title = Product.objects.filter(category=product[0].category).values('title')
        return render(request, "app/category.html", locals())

@method_decorator(login_required,name='dispatch')
class ProductDetail(View):
    def get(self, request, pk):
        product = Product.objects.get(pk=pk)
        wishlist = Wishlist.objects.filter(Q(product=product) & Q(user=request.user))
        totalitem = 0
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user = request.user))
        item_in_wishlist = 0
        if request.user.is_authenticated:
            item_in_wishlist = len(Wishlist.objects.filter(user = request.user))
        return render(request, "app/productdetail.html", locals())


class CustomerRegistrationView(View):
    def get(self, request):
        form = CustomerRegistrationForm()
        totalitem = 0
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user = request.user))
        item_in_wishlist = 0
        if request.user.is_authenticated:
            item_in_wishlist = len(Wishlist.objects.filter(user = request.user))
        return render(request, 'app/customerregistration.html', locals())
    def post(self,request):
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,"Congratulation! User Registration is Successful")
        else:
            messages.warning(request, "Invalid Input Data")
        return render(request, 'app/customerregistration.html',locals())    
 
@method_decorator(login_required,name='dispatch')   
class ProfileView(View):
    def get(self,request):
        form = CustomerProfileForm()
        totalitem = 0
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user = request.user))
        item_in_wishlist = 0
        if request.user.is_authenticated:
            item_in_wishlist = len(Wishlist.objects.filter(user = request.user))
        return render(request, 'app/profile.html',locals())
    def post(self,request):    
        form = CustomerProfileForm(request.POST)
        if form.is_valid():
            user = request.user
            name = form.cleaned_data['name']
            mobile = form.cleaned_data['mobile']
            locality = form.cleaned_data['locality']
            city = form.cleaned_data['city']
            division = form.cleaned_data['division']
            zipcode = form.cleaned_data['zipcode']
            reg = Customer(user=user,name=name,mobile=mobile,locality=locality,city=city,division=division,zipcode=zipcode)
            reg.save()
            messages.success(request,"Congratulations! Profile Saved Successfully")
        else:
            messages.warning(request,"Invalid data Input")
        return render(request, 'app/profile.html',locals())  
 
@login_required      
def address(request):
    totalitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user = request.user))
    item_in_wishlist = 0
    if request.user.is_authenticated:
        item_in_wishlist = len(Wishlist.objects.filter(user = request.user))
    add = Customer.objects.filter(user=request.user)
    return render(request, 'app/address.html',locals())

@method_decorator(login_required,name='dispatch')
class updateAddress(View):
    def get(self,request,pk):
        totalitem = 0
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user = request.user))
        item_in_wishlist = 0
        if request.user.is_authenticated:
            item_in_wishlist = len(Wishlist.objects.filter(user = request.user))
        add = Customer.objects.get(pk=pk)
        form = CustomerProfileForm(instance=add)
        return render(request, 'app/updateAddress.html',locals())
    def post(self,request,pk):
        form = CustomerProfileForm(request.POST)
        if form.is_valid():
            add = Customer.objects.get(pk=pk)
            add.name = form.cleaned_data['name']
            add.mobile = form.cleaned_data['mobile']
            add.locality = form.cleaned_data['locality']
            add.city = form.cleaned_data['city']
            add.division = form.cleaned_data['division']
            add.zipcode = form.cleaned_data['zipcode']
            add.save()
            messages.success(request,"Congratulations! Profile Updated successfully")
        else:
            messages.warning(request, "Invalid Input data")
        return redirect('address')
 
@login_required       
def add_to_cart(request):
    user = request.user
    product_id = request.GET.get('prod_id')
    product = Product.objects.get(id=product_id)
    Cart(user=user, product=product).save()
    return redirect('showcart')  

@login_required
def show_cart(request):
    user = request.user
    cart = Cart.objects.filter(user = user)
    amount = 0
    for p in cart:
        value = p.quantity * p.product.discounted_price
        amount = amount + value
    totalamount = amount + 100
    totalitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user = request.user))
    item_in_wishlist = 0
    if request.user.is_authenticated:
        item_in_wishlist = len(Wishlist.objects.filter(user = request.user))
    return render(request, 'app/addtocart.html',locals())

@login_required
def plus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product = prod_id) & Q(user = request.user))
        c.quantity +=1
        c.save()
        user = request.user
        cart = Cart.objects.filter(user = user)
        amount = 0
        for p in cart:
            value = p.quantity * p.product.discounted_price
            amount = amount + value
        totalamount = amount + 100
        data={
            'quantity':c.quantity,
            'amount': amount,
            'totalamount': totalamount
        }
        return JsonResponse(data)

@login_required
def minus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product = prod_id) & Q(user = request.user))
        c.quantity -=1
        c.save()
        user = request.user
        cart = Cart.objects.filter(user = user)
        amount = 0
        for p in cart:
            value = p.quantity * p.product.discounted_price
            amount = amount + value
        totalamount = amount + 100
        data={
            'quantity':c.quantity,
            'amount': amount,
            'totalamount': totalamount
        }
        return JsonResponse(data)

@login_required
def remove_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product = prod_id) & Q(user = request.user))
        c.delete()
        user = request.user
        cart = Cart.objects.filter(user = user)
        amount = 0
        for p in cart:
            value = p.quantity * p.product.discounted_price
            amount = amount + value
        totalamount = amount + 100
        data={
            'quantity':c.quantity,
            'amount': amount,
            'totalamount': totalamount
        }
        return redirect('showcart')

@method_decorator(login_required,name='dispatch')
class checkout(View):
    def get(self, request):
        user = request.user
        cart_items = Cart.objects.filter(user=user)
        if not cart_items.exists():
            messages.warning(request, "Your cart is empty. Add items to proceed to checkout.")
            return redirect("cart")
        totalitem = 0
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=user))
        item_in_wishlist = 0
        if request.user.is_authenticated:
            item_in_wishlist = len(Wishlist.objects.filter(user = request.user))
        add = Customer.objects.filter(user=user)
        cart_items = Cart.objects.filter(user=user)
        famount = 0
        for p in cart_items:
            value = p.quantity * p.product.discounted_price
            famount += value
        totalamount = famount + 100  

        
        mock_order_id = str(uuid.uuid4())
        mock_payment_id = str(uuid.uuid4())
        mock_payment_status = "created"

       
        payment = Payment(
            user=user,
            amount=totalamount,
            transaction_id=mock_order_id,
            payment_status=mock_payment_status,
            payment_id=mock_payment_id,
            paid=False,  
        )
        payment.save()
        return render(request, 'app/checkout.html', locals())
    


from .models import Payment

def payment_view(request):
    if not request.user.is_authenticated:
        messages.error(request, 'You need to be logged in to proceed with payment.')
        return redirect('login')

    user = request.user
    cart_items = Cart.objects.filter(user=user)

    if not cart_items.exists():
        messages.warning(request, 'Your cart is empty. Please add items to the cart.')
        return redirect('index')

    amount = sum(item.quantity * item.product.discounted_price for item in cart_items)
    total_amount = amount + 1200

    customer = Customer.objects.filter(user=user).first()
    if not customer:
        messages.warning(request, 'Please update your profile before proceeding with payment.')
        return redirect('profile')

    transaction_id = uuid4().hex  

 
    payment = Payment.objects.create(
        user=user,
        amount=total_amount,
        transaction_id=transaction_id,
        payment_status='Initiated',
    )

    data = {
        'store_id': settings.SSL_COMMERZ['store_id'],
        'store_passwd': settings.SSL_COMMERZ['store_passwd'],
        'total_amount': str(total_amount),
        'currency': 'BDT',
        'tran_id': transaction_id,
        'success_url': request.build_absolute_uri('/payment-success/?tran_id=' + transaction_id),
        'fail_url': request.build_absolute_uri('/payment-fail/'),
        'cancel_url': request.build_absolute_uri('/payment-cancel/'),
        'cus_name': customer.name,
        'cus_email': user.email,
        'cus_phone': customer.mobile,
        'cus_add1': customer.locality,
        'cus_add2': customer.city,
        'product_name': 'Cart Items',
        'product_category': 'Products',
        'product_profile': 'general',
    }

    
    url = 'https://sandbox.sslcommerz.com/gwprocess/v3/api.php'
    response = requests.post(url, data=data)
    response_data = response.json()

    if response_data.get('status') == 'SUCCESS':
        return redirect(response_data['GatewayPageURL'])
    else:
        messages.error(request, 'Payment initiation failed. Please try again.')
        return redirect('checkout')


@csrf_exempt
def payment_success(request):
    transaction_id = request.GET.get('tran_id')  # Retrieve transaction ID from URL

    # Query the Payment model
    payment = Payment.objects.filter(transaction_id=transaction_id).first()

    if payment:
        # Update payment status
        payment.payment_status = 'Success'
        payment.paid = True
        payment.save()

        # Move items from the cart to OrderPlaced
        user = payment.user
        customer = Customer.objects.filter(user=user).first()
        cart = Cart.objects.filter(user=user)

        for c in cart:
            OrderPlaced.objects.create(
                user=user,
                customer=customer,
                product=c.product,
                quantity=c.quantity,
                payment=payment
            )
            c.delete()  # Clear cart after placing the order

        messages.success(request, 'Payment Successful! Your order has been placed.')

        # Pass transaction details to the template
        context = {
            'transaction_id': payment.transaction_id,
            'amount': payment.amount,
        }
        return render(request, 'app/payment_success.html', context)
    else:
        messages.error(request, 'Transaction not found or payment failed.')
        return redirect('checkout')


def payment_fail(request):
    messages.error(request, 'Payment Failed. Please try again or contact support.')
    return redirect('cart')

@csrf_exempt
def process_cod_order(request):
    try:
        order_id = request.GET.get('order_id')
        payment_id = request.GET.get('payment_id')
        cust_id = request.GET.get('cust_id')
        user = request.user
        
        # Validate inputs
        if not (order_id and payment_id and cust_id):
            messages.error(request, "Invalid request. Please try again.")
            return redirect("checkout")
        
        # Verify customer and payment
        customer = Customer.objects.get(id=cust_id, user=user)
        payment = Payment.objects.get(transaction_id=order_id, user=user)
        
        # Update payment and process the order
        payment.paid = False
        payment.payment_id = payment_id
        payment.save()
        
        cart = Cart.objects.filter(user=user)
        for c in cart:
            OrderPlaced(user=user, customer=customer, product=c.product, quantity=c.quantity, payment=payment).save()
            c.delete()  # Remove items from the cart after order placement
        
        messages.success(request, "Order placed successfully!")
        return redirect("orders")
    
    except Customer.DoesNotExist:
        messages.error(request, "Invalid customer details.")
    except Payment.DoesNotExist:
        messages.error(request, "Invalid payment details.")
    except Exception as e:
        messages.error(request, f"An error occurred: {e}")
    
    return redirect("checkout")

@login_required
def orders(request):
    totalitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user = request.user))
    item_in_wishlist = 0
    if request.user.is_authenticated:
        item_in_wishlist = len(Wishlist.objects.filter(user = request.user))
    order_placed = OrderPlaced.objects.filter(user = request.user)
    return render(request, 'app/orders.html',locals())

@login_required
def search(request):
    query = request.GET.get('search', '') 
    product = Product.objects.filter(Q(title__icontains=query))
    return render(request, 'app/search.html', locals())

@login_required
def wishlist(request):
    totalitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
    wishlist_items = Wishlist.objects.filter(user=request.user)
    return render(request, 'app/wishlist.html', {'wishlist_items': wishlist_items, 'totalitem': totalitem})
@login_required
def plus_wishlist(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        product = Product.objects.get(id=prod_id)
        user = request.user
        Wishlist(user=user, product=product).save()
        data = {
            'message': 'Wishlist Added Successfully',
        }
        return JsonResponse(data)
@login_required
def minus_wishlist(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        product = Product.objects.get(id=prod_id)
        user = request.user
        Wishlist.objects.filter(user=user, product=product).delete()
        data = {
            'message': 'Wishlist Remove Successfully',
        }
        return JsonResponse(data)