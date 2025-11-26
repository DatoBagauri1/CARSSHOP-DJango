from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Product, Cart

def home_page(request):
    context = {
        'title': 'ეგზოტიკური მანქანების შოურუმი',
        'intro_text': 'მოგესალმებით ჩვენს ეგზოტიკური მანქანების შოურუმში. ჩვენ ვართ პრემიუმ კლასის სუპერმანქანების იმპორტიორები და დილერები. აღმოაჩინეთ თქვენი ოცნების ავტომობილი ჩვენს კოლექციაში.',
    }
    return render(request, 'shop/home.html', context)

def product_list(request):
    products = Product.objects.all().order_by('name')
    
    context = {
        'products': products,
        'title': 'მანქანების კოლექცია',
    }
    return render(request, 'shop/product_list.html', context)

def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    
    context = {
        'product': product,
        'title': product.name,
    }
    return render(request, 'shop/product_detail.html', context)

@login_required
def add_to_cart(request, pk):
    product = get_object_or_404(Product, pk=pk)
    user = request.user
    
    cart_item, created = Cart.objects.get_or_create(
        user=user, 
        product=product,
        defaults={'quantity': 1}
    )

    if not created:
        cart_item.quantity += 1
        cart_item.save()

    return redirect('cart_detail')

@login_required
def cart_detail(request):
    cart_items = Cart.objects.filter(user=request.user).order_by('-added_at')
    
    cart_total = sum(item.total_item_price() for item in cart_items)
    
    context = {
        'cart_items': cart_items,
        'cart_total': cart_total,
        'title': 'თქვენი კალათა',
    }
    return render(request, 'shop/cart_detail.html', context)

@login_required
def remove_from_cart(request, pk):
    try:
        cart_item = Cart.objects.get(pk=pk, user=request.user)
        
        product_name = cart_item.product.name 
        
        cart_item.delete()
        
        messages.success(request, f"🏎️ **{product_name}** წარმატებით წაიშალა კალათიდან.")
        
    except Cart.DoesNotExist:
        messages.error(request, "კალათის ჩანაწერი ვერ მოიძებნა.")
            
    return redirect('cart_detail')

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    
    return render(request, 'registration/signup.html', {'form': form})