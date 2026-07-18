from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import logout
from .forms import RegisterForm, FoodForm
from .models import Food, Cart, Order, OrderItem


# Register
def register_view(request):
    form = RegisterForm(request.POST or None)       #Create a form. If user submitted data, fill it with that data. Otherwise, keep it empty.

    if form.is_valid():
        user = form.save()      #Create a new user in the database and give me that user back
        login(request, user)    #Start a session for this user (log them in immediately)
        return redirect('food_list')

    return render(request, 'register.html', {'form': form})


# Login
def login_view(request):
    form = AuthenticationForm(request, data=request.POST or None)

    if form.is_valid():
        login(request, form.get_user())
        return redirect('food_list')

    return render(request, 'login.html', {'form': form})


# Logout
def logout_view(request):
    logout(request)
    return redirect('login')


# Food List
def food_list(request):
    foods = Food.objects.all()

    query = request.GET.get('q')   #Checks if user searched something in URL
    if query:
        foods = foods.filter(name__icontains=query)

    return render(request, 'food_list.html', {'foods': foods})


# Add Food4
@login_required
def add_food(request):
    form = FoodForm(request.POST or None,request.FILES or None)

    if form.is_valid():
        form.save()
        return redirect('food_list')

    return render(request, 'food_form.html', {'form': form})


# Edit Food
@login_required
def edit_food(request, pk):
    food = get_object_or_404(Food, pk=pk)

    form = FoodForm(
        request.POST or None,
        request.FILES or None,
        instance=food
    )

    if form.is_valid():
        form.save()
        return redirect('food_list')

    return render(request, 'food_form.html', {'form': form})


# Delete Food
@login_required
def delete_food(request, pk):
    food = get_object_or_404(Food, pk=pk)

    if request.method == 'POST':
        food.delete()
        return redirect('food_list')

    return render(request, 'delete.html', {'food': food})


# Add To Cart
@login_required
def add_to_cart(request, food_id):
    food = get_object_or_404(Food, id=food_id)

    cart_item, created = Cart.objects.get_or_create(user=request.user,food=food)

    if not created:
        cart_item.quantity += 1
        cart_item.save()

    return redirect('cart')


# View Cart
@login_required
def cart_view(request):
    items = Cart.objects.filter(user=request.user)

    total = sum(item.subtotal for item in items)

    return render(request, 'cart.html', {'items': items,'total': total})


# Place Order
@login_required
def place_order(request):
    cart_items = Cart.objects.filter(user=request.user)

    total = sum(item.subtotal for item in cart_items)

    order = Order.objects.create( user=request.user, total_amount=total)

    for item in cart_items:
        OrderItem.objects.create(
            order=order,
            food=item.food,
            quantity=item.quantity,
            price=item.food.price
        )

    cart_items.delete()
    return redirect('order_history')


@login_required
def order_history(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')

    return render(request, 'order_history.html', {'orders': orders})


@login_required
def order_detail(request, order_id):
    order = get_object_or_404(Order,id=order_id, user=request.user)

    items = OrderItem.objects.filter(order=order)

    return render(request, 'order_detail.html', { 'order': order,'items': items})




