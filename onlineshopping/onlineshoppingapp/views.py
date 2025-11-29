from django.shortcuts import render
from onlineshoppingapp.models import Product,Category
from onlineshoppingapp.forms import ProductForm, CategoryForm
from django.shortcuts import redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
# Create your views here.


def home(request):
    from onlineshoppingapp.models import Wishlist, Cart
    # Redirect authenticated users to dashboard
    if request.user.is_authenticated:
        return redirect('dashboard')
    # Fetch all categories
    categories = Category.objects.all()
    context = {'categories': categories}
    
    # Add wishlist and cart counts if user is authenticated
    if request.user.is_authenticated:
        context['wishlist_count'] = Wishlist.objects.filter(user=request.user).count()
        context['cart_count'] = Cart.objects.filter(user=request.user).count()
    
    return render(request, 'home.html', context)


def register(request):
    from onlineshoppingapp.models import Wishlist, Cart
    if request.method == 'POST':
        form = ProductForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            return redirect('admin_panel')
        else:
            return HttpResponse("Invalid request ")
    
    form = ProductForm()
    context = {'form': form}
    if request.user.is_authenticated:
        context['wishlist_count'] = Wishlist.objects.filter(user=request.user).count()
        context['cart_count'] = Cart.objects.filter(user=request.user).count()
    return render(request, 'register.html', context)

def productlist(request):
    from onlineshoppingapp.models import Wishlist, Cart, Review
    pdt = Product.objects.all()
    context = {'products': pdt, 'total_products': pdt.count()}
    
    if request.user.is_authenticated:
        context['wishlist_count'] = Wishlist.objects.filter(user=request.user).count()
        context['cart_count'] = Cart.objects.filter(user=request.user).count()
        # Get list of product IDs in wishlist and cart
        context['wishlist_products'] = list(Wishlist.objects.filter(user=request.user).values_list('product_id', flat=True))
        context['cart_products'] = list(Cart.objects.filter(user=request.user).values_list('product_id', flat=True))
    
    # Include reviews mapping for frontend (latest 3 reviews per product)
    reviews_map = {}
    for p in pdt:
        reviews_map[p.id] = list(p.reviews.all()[:3])
    context['reviews_map'] = reviews_map
    
    return render(request, 'list.html', context)

def category_detail(request, id):
    from onlineshoppingapp.models import Wishlist, Cart
    category = Category.objects.get(id=id)
    # Filter products by the selected category
    products = Product.objects.filter(category=category)
    context = {'products': products, 'category': category, 'total_products': products.count()}
    
    if request.user.is_authenticated:
        context['wishlist_count'] = Wishlist.objects.filter(user=request.user).count()
        context['cart_count'] = Cart.objects.filter(user=request.user).count()
        # Get list of product IDs in wishlist and cart
        context['wishlist_products'] = list(Wishlist.objects.filter(user=request.user).values_list('product_id', flat=True))
        context['cart_products'] = list(Cart.objects.filter(user=request.user).values_list('product_id', flat=True))
    
    return render(request, 'list.html', context)

def edit_product(request, p_id):
    from onlineshoppingapp.models import Wishlist, Cart
    p=Product.objects.get(id=p_id)
    f=ProductForm(request.POST or None, request.FILES or None, instance=p)
    if f.is_valid():
        f.save()
        return redirect('admin_panel')
    context = {'form': f}
    if request.user.is_authenticated:
        context['wishlist_count'] = Wishlist.objects.filter(user=request.user).count()
        context['cart_count'] = Cart.objects.filter(user=request.user).count()
    return render(request,'register.html', context)

def delete_product(request, p_id):
    p=Product.objects.get(id=p_id)
    p.delete()
    return redirect('admin_panel')

# def signup(request):
#     if request.method == 'POST':
#         u=request.POST['username']
#         e=request.POST['email']
#         p=request.POST['password']
#         f=request.POST['first_name']
#         l=request.POST['last_name']
#         user=User.objects.create_user(username=u,email=e,password=p,first_name=f,last_name=l)
#         user.save()
#     return render(request, 'signup.html')

#importing and using UserCreationForm for signup
def signup(request):
    from onlineshoppingapp.models import Wishlist, Cart
    if request.method == 'POST':
        s = UserCreationForm(request.POST)
        if s.is_valid():
            s.save()
            return redirect('signin')
    else:
        s = UserCreationForm()
    
    context = {'form': s}
    if request.user.is_authenticated:
        context['wishlist_count'] = Wishlist.objects.filter(user=request.user).count()
        context['cart_count'] = Cart.objects.filter(user=request.user).count()
    return render(request,'signup.html', context)

# def signin(request):
#     if request.method == 'POST':
#         u=request.POST['username']
#         p=request.POST['password']
#         user=authenticate(username=u,password=p)
#         if user is not None:
#             login(request,user)
#             f=user.first_name
#             l=user.last_name
#             return render(request, 'dashboard.html',{'fname':f,'lname':l})
#         else:
#             return HttpResponse("Invalid credentials")
#     return render(request, 'signin.html')

#importing and using authenticate for signin
def signin(request):
    from onlineshoppingapp.models import Wishlist, Cart
    if request.method == 'POST':
        a = AuthenticationForm(request, data=request.POST)
        if a.is_valid():
            user = a.get_user()
            login(request, user)
            return redirect('dashboard')
    else:
        a = AuthenticationForm()
    
    context = {'form': a}
    if request.user.is_authenticated:
        context['wishlist_count'] = Wishlist.objects.filter(user=request.user).count()
        context['cart_count'] = Cart.objects.filter(user=request.user).count()
    return render(request, 'signin.html', context)

def signout(request):
    logout(request)
    return redirect('home')

def dashboard(request):
    from onlineshoppingapp.models import Wishlist, Cart
    if request.user.is_authenticated:
        f = request.user.first_name
        l = request.user.last_name
        categories = Category.objects.all()
        context = {
            'fname': f,
            'lname': l,
            'user': request.user,
            'categories': categories,
            'wishlist_count': Wishlist.objects.filter(user=request.user).count(),
            'cart_count': Cart.objects.filter(user=request.user).count()
        }
        return render(request, 'dashboard.html', context)
    else:
        return redirect('signin')

def search(request):
    from onlineshoppingapp.models import Wishlist, Cart
    if request.method == 'POST':
        n = request.POST.get('n1', '')
        # Case-insensitive search using icontains
        products = Product.objects.filter(name__icontains=n)
    else:
        # If GET request, show all products
        products = Product.objects.all()
    
    context = {'products': products, 'total_products': products.count()}
    
    if request.user.is_authenticated:
        context['wishlist_count'] = Wishlist.objects.filter(user=request.user).count()
        context['cart_count'] = Cart.objects.filter(user=request.user).count()
        # Get list of product IDs in wishlist and cart
        context['wishlist_products'] = list(Wishlist.objects.filter(user=request.user).values_list('product_id', flat=True))
        context['cart_products'] = list(Cart.objects.filter(user=request.user).values_list('product_id', flat=True))
    
    return render(request, 'list.html', context)

def admin_panel(request):
    from onlineshoppingapp.models import Review
    # Get all products, categories, and users
    products = Product.objects.all()
    categories = Category.objects.all()
    users = User.objects.all()
    total_users = users.count()
    
    # Get all reviews with related product and user data
    reviews = Review.objects.select_related('product', 'user').all()
    
    context = {
        'products': products,
        'categories': categories,
        'users': users,
        'reviews': reviews,
        'total_products': products.count(),
        'total_categories': categories.count(),
        'total_users': total_users,
        'total_reviews': reviews.count(),
        'show_login': False
    }
    
    return render(request, 'admin_panel.html', context)

def add_category(request):
    from onlineshoppingapp.models import Wishlist, Cart
    if request.method == 'POST':
        form = CategoryForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('admin_panel')
        else:
            return HttpResponse("Invalid request")
    
    form = CategoryForm()
    context = {'form': form}
    if request.user.is_authenticated:
        context['wishlist_count'] = Wishlist.objects.filter(user=request.user).count()
        context['cart_count'] = Cart.objects.filter(user=request.user).count()
    return render(request, 'add_category.html', context)

def edit_category(request, c_id):
    from onlineshoppingapp.models import Wishlist, Cart
    c = Category.objects.get(id=c_id)
    f = CategoryForm(request.POST or None, request.FILES or None, instance=c)
    if f.is_valid():
        f.save()
        return redirect('admin_panel')
    context = {'form': f}
    if request.user.is_authenticated:
        context['wishlist_count'] = Wishlist.objects.filter(user=request.user).count()
        context['cart_count'] = Cart.objects.filter(user=request.user).count()
    return render(request, 'add_category.html', context)

def delete_category(request, c_id):
    c = Category.objects.get(id=c_id)
    c.delete()
    return redirect('admin_panel')

@login_required(login_url='signin')
def add_to_wishlist(request, p_id):
    from onlineshoppingapp.models import Wishlist
    product = Product.objects.get(id=p_id)
    wishlist_item = Wishlist.objects.filter(user=request.user, product=product).first()
    
    if wishlist_item:
        # If already in wishlist, remove it (toggle off)
        wishlist_item.delete()
    else:
        # If not in wishlist, add it (toggle on)
        Wishlist.objects.create(user=request.user, product=product)
    
    return redirect('list')

@login_required(login_url='signin')
def remove_from_wishlist(request, p_id):
    from onlineshoppingapp.models import Wishlist
    Wishlist.objects.filter(user=request.user, product_id=p_id).delete()
    return redirect('wishlist')

@login_required(login_url='signin')
def view_wishlist(request):
    from onlineshoppingapp.models import Wishlist, Cart
    wishlist_items = Wishlist.objects.filter(user=request.user)
    context = {
        'wishlist_items': wishlist_items,
        'wishlist_count': wishlist_items.count(),
        'cart_count': Cart.objects.filter(user=request.user).count(),
        'cart_products': list(Cart.objects.filter(user=request.user).values_list('product_id', flat=True))
    }
    return render(request, 'wishlist.html', context)

@login_required(login_url='signin')
def add_to_cart(request, p_id):
    from onlineshoppingapp.models import Cart
    product = Product.objects.get(id=p_id)
    cart_item = Cart.objects.filter(user=request.user, product=product).first()
    
    if cart_item:
        # If already in cart, remove it (toggle off)
        cart_item.delete()
    else:
        # If not in cart, add it (toggle on)
        Cart.objects.create(user=request.user, product=product)
    
    return redirect('list')

@login_required(login_url='signin')
def remove_from_cart(request, p_id):
    from onlineshoppingapp.models import Cart
    Cart.objects.filter(user=request.user, product_id=p_id).delete()
    return redirect('cart')

@login_required(login_url='signin')
def update_cart_quantity(request, p_id):
    from onlineshoppingapp.models import Cart
    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 1))
        cart_item = Cart.objects.get(user=request.user, product_id=p_id)
        if quantity > 0:
            cart_item.quantity = quantity
            cart_item.save()
        else:
            cart_item.delete()
    return redirect('cart')

@login_required(login_url='signin')
def view_cart(request):
    from onlineshoppingapp.models import Cart, Wishlist
    cart_items = Cart.objects.filter(user=request.user)
    total_price = sum(item.get_total_price() for item in cart_items)
    context = {
        'cart_items': cart_items,
        'total_price': total_price,
        'cart_count': cart_items.count(),
        'wishlist_count': Wishlist.objects.filter(user=request.user).count(),
        'wishlist_products': list(Wishlist.objects.filter(user=request.user).values_list('product_id', flat=True))
    }
    return render(request, 'cart.html', context)


@login_required(login_url='signin')
def buy_now(request, p_id):
    from onlineshoppingapp.models import Product, Order, OrderItem, Cart
    product = Product.objects.get(id=p_id)
    if request.method == 'POST':
        try:
            quantity = int(request.POST.get('quantity', 1))
        except ValueError:
            quantity = 1

        total = product.price * quantity
        order = Order.objects.create(user=request.user, total_amount=total)
        OrderItem.objects.create(order=order, product=product, quantity=quantity, price=product.price)

        # remove from cart if it exists
        Cart.objects.filter(user=request.user, product=product).delete()

        return redirect('bill', order_id=order.id)

    return redirect('cart')


@login_required(login_url='signin')
def bill(request, order_id):
    from onlineshoppingapp.models import Order, OrderItem
    order = Order.objects.get(id=order_id, user=request.user)
    items = OrderItem.objects.filter(order=order)
    context = {'order': order, 'items': items}
    return render(request, 'bill.html', context)


@login_required(login_url='signin')
def checkout(request):
    from onlineshoppingapp.models import Cart, Order, OrderItem
    if request.method == 'POST':
        cart_items = Cart.objects.filter(user=request.user)
        if not cart_items.exists():
            return redirect('cart')

        total = sum(item.get_total_price() for item in cart_items)
        order = Order.objects.create(user=request.user, total_amount=total)

        for item in cart_items:
            OrderItem.objects.create(order=order, product=item.product, quantity=item.quantity, price=item.product.price)

        # clear cart
        cart_items.delete()

        return redirect('bill', order_id=order.id)

    return redirect('cart')

@login_required(login_url='signin')
def submit_review(request, p_id):
    from onlineshoppingapp.models import Review
    product = Product.objects.get(id=p_id)
    if request.method == 'POST':
        rating = int(request.POST.get('rating', 0))
        comment = request.POST.get('comment', '').strip()
        if rating >= 1 and rating <= 5:
            # update or create review by this user for this product
            Review.objects.update_or_create(
                user=request.user,
                product=product,
                defaults={'rating': rating, 'comment': comment}
            )
    return redirect('list')

def reply_to_review(request, review_id):
    from onlineshoppingapp.models import Review
    review = Review.objects.get(id=review_id)
    if request.method == 'POST':
        reply = request.POST.get('admin_reply', '').strip()
        review.admin_reply = reply
        review.save()
        return redirect('admin_panel')
    # If GET, render a tiny form (optional)
    context = {'review': review}
    return render(request, 'admin_reply.html', context)

@login_required(login_url='signin')
@staff_member_required
def delete_review(request, review_id):
    from onlineshoppingapp.models import Review
    review = Review.objects.get(id=review_id)
    review.delete()
    return redirect('admin_panel')
