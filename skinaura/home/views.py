from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404,redirect
from .models import Product,Order,OrderItem
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib import messages
from .models import Contact

def index(request):
    return render(request, 'home/index.html')

def products(request):
    query = request.GET.get('q')

    if query:
        products = Product.objects.filter(name__icontains=query)
    else:
        products = Product.objects.all()

    return render(request, 'home/products.html', {'products': products})



def product_detail(request, id):
    product = get_object_or_404(Product, id=id)
    return render(request, 'home/product_detail.html', {
        'product': product
    })



def about(request):
    return render(request, 'home/about.html')

def contact(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        message = request.POST.get("message")

        Contact.objects.create(
            name=name,
            email=email,
            message=message
        )

        messages.success(request, "Message sent successfully!")

    return render(request, "home/contact.html")

from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.shortcuts import render, redirect

def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)

            # ✅ Check staff AFTER confirming user exists
            if user.is_staff:
                return redirect("/dashboard/")
            else:
                return redirect("/")
        else:
            messages.error(request, "Invalid username or password")
            return render(request, "home/login.html")

    return render(request, "home/login.html")
def register(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")

        if len(password1) < 6:
            messages.error(request, "Password must be at least 6 characters.")
            return redirect("register")
        
        
        # Password match check
        if password1 != password2:
            messages.error(request, "Passwords do not match.")
            return render("register")

        # Username already exists
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already taken.")
            return render("register")

        # Email already exists
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered.")
            return render("register")

        # Create user
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password1
        )

        messages.success(request, "Account created successfully! Please login.")
        return redirect("login")

    return render(request, "home/register.html")

@login_required
def checkout(request):
    cart = request.session.get('cart', {})

    if not cart:
        return redirect('cart')

    products = Product.objects.filter(id__in=cart.keys())

    total = 0
    cart_items = []

    for product in products:
        quantity = cart[str(product.id)]
        if quantity > product.stock:
           return render(request, 'home/checkout.html', {
            'cart_items': cart_items,
            'total': total,
            'error': f"Not enough stock for {product.name}"
        })

        subtotal = product.price * quantity
        total += subtotal

        cart_items.append({
            'product': product,
            'quantity': quantity,
            'subtotal': subtotal
        })

    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        address = request.POST.get('address')

        # Create Order
        order = Order.objects.create(
            user=request.user,
            customer_name=name,
            email=email,
            address=address,
            total_amount=total
        )

        # Create Order Items
        for item in cart_items:
            OrderItem.objects.create(
                order=order,
                product=item['product'],
                quantity=item['quantity'],
                price=item['product'].price
            )

            # to reduce stock
            product=item['product']
            product.stock -= item['quantity']
            product.save()

        # Clear cart
        request.session['cart'] = {}

        return redirect('order_success',order_id=order.id)

    return render(request, 'home/checkout.html', {
        'cart_items': cart_items,
        'total': total
    })



    

def add_to_cart(request, id):
    cart = request.session.get('cart', {})

    product_id = str(id)

    if product_id in cart:
        cart[product_id] += 1
    else:
        cart[product_id] = 1

    request.session['cart'] = cart
    return redirect('cart')


def cart(request):
    cart = request.session.get('cart', {})
    cart_items = []
    total = 0

    for id, quantity in cart.items():
        product = Product.objects.get(id=id)

        subtotal = product.price * quantity
        total += subtotal

        cart_items.append({
            'product': product,
            'quantity': quantity,
            'subtotal': subtotal
        })

    tax = total * 0.02
    final_total = total + tax

    context = {
        'cart_items': cart_items,
        'total': total,
        'tax': tax,
        'final_total': final_total
    }

    return render(request, 'home/cart.html', context)
    


    
def remove_from_cart(request, id):
    cart = request.session.get('cart', {})
    product_id = str(id)

    if product_id in cart:
        del cart[product_id]

    request.session['cart'] = cart
    return redirect('cart')


def increase_quantity(request, id):
    cart = request.session.get('cart', {})

    if str(id) in cart:
        cart[str(id)] += 1

    request.session['cart'] = cart
    return redirect('cart')


def decrease_quantity(request, id):
    cart = request.session.get('cart', {})

    if str(id) in cart:
        if cart[str(id)] > 1:
            cart[str(id)] -= 1
        else:
            del cart[str(id)]

    request.session['cart'] = cart
    return redirect('cart')

def order_success(request, order_id):
    order = Order.objects.get(id=order_id)
    return render(request, 'home/success.html', {'order': order})

@login_required
def track_order(request, order_id):
    try:
        order = Order.objects.get(id=order_id, user=request.user)
    except Order.DoesNotExist:
        return render(request, 'home/track_order.html', {
            'error': "Order not found or access denied."
        })

    return render(request, 'home/track_order.html', {'order': order})

@login_required
def my_orders(request):
    orders = Order.objects.filter(user=request.user)
    return render(request, 'home/my_orders.html', {'orders': orders})



@staff_member_required
def admin_dashboard(request):
    print("Is staff:", request.user.is_staff)
    print("Is superuser:", request.user.is_superuser)
    print("User:", request.user)
    total_orders = Order.objects.count()

    total_revenue = Order.objects.filter(status='Delivered').aggregate(
        Sum('total_amount')
    )['total_amount__sum'] or 0

    pending_orders = Order.objects.filter(status='Pending').count()
    shipped_orders = Order.objects.filter(status='Shipped').count()
    delivered_orders = Order.objects.filter(status='Delivered').count()

    low_stock_products = Product.objects.filter(stock__lt=5)

    context = {
        'total_orders': total_orders,
        'total_revenue': total_revenue,
        'pending_orders': pending_orders,
        'shipped_orders': shipped_orders,
        'delivered_orders': delivered_orders,
        'low_stock_products': low_stock_products,
    }

    return render(request, 'home/admin_dashboard.html', context)


#increasing quantity


# removing item from cart
def remove_from_cart(request, id):
    cart = request.session.get('cart', {})
    product_id = str(id)

    if product_id in cart:
        del cart[product_id]

    request.session['cart'] = cart
    return redirect('cart')






def logout_view(request):
    auth_logout(request)
    return redirect("/")   # important


















