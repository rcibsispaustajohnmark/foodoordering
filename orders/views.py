from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .models import Order, Food
import pickle
from ml_model.recommender import recommend_food

# Load food data
with open("ml_model/food_data.pkl", "rb") as f:
    food = pickle.load(f)

# Prices dictionary
prices = {
    "Chicken Adobo": 120,
    "Sinigang na Baboy": 130,
    "Lechon Kawali": 150
}

# Check if user is admin
def is_admin(user):
    return user.is_staff

# -------------------- User Views --------------------
@login_required
def home(request):
    if request.user.is_staff:
        return redirect("admin_dashboard")  # redirect admin to dashboard

    # Get available foods from database
    food_items = Food.objects.filter(is_available=True).values("id", "name", "price")
    
    return render(request, "orders/home.html", {"food_items": food_items})


@login_required
def food_detail(request, food_name):
    if request.user.is_staff:
        return redirect("admin_dashboard")
    food_item = food[food["name"] == food_name]
    if food_item.empty:
        return render(request, "orders/food_not_found.html", {"food_name": food_name})
    food_info = food_item.iloc[0]
    recommended_names = recommend_food(food_name)
    recommended_foods = [{"name": name, "price": prices.get(name, 100)} for name in recommended_names]
    return render(request, "orders/food_detail.html", {
        "food_name": food_info["name"],
        "price": food_info.get("price", 100),
        "recommended_foods": recommended_foods
    })

@login_required
def add_order(request):
    if request.user.is_staff:
        return redirect("admin_dashboard")
    if request.method == "POST":
        food_name = request.POST.get("food_name")
        quantity = int(request.POST.get("quantity", 1))
        order = Order.objects.filter(user=request.user, food_name=food_name).first()
        if order:
            order.quantity += quantity
            order.save()
        else:
            Order.objects.create(food_name=food_name, quantity=quantity, user=request.user)
    return redirect('order_summary')

@login_required
def order_summary(request):
    if request.user.is_staff:
        return redirect("admin_dashboard")
    orders = Order.objects.filter(user=request.user)
    total_price = sum(order.quantity * prices.get(order.food_name, 100) for order in orders)
    return render(request, "orders/order_summary.html", {
        "orders": orders,
        "total_price": total_price,
        "prices": prices
    })

@login_required
def remove_order(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    order.delete()
    return redirect("order_summary")

@login_required
def update_order(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    if request.method == "POST":
        quantity = int(request.POST.get("quantity", 1))
        order.quantity = quantity
        order.save()
    return redirect("order_summary")

@login_required
def place_order(request):
    orders = Order.objects.filter(user=request.user, status='PENDING')
    orders.update(status='PENDING')  # keep status pending
    return redirect("order_summary")

# -------------------- Admin Views --------------------
@user_passes_test(is_admin)
def admin_dashboard(request):
    orders = Order.objects.all().order_by('-created_at')
    foods = Food.objects.all()
    users = User.objects.all()
    return render(request, "orders/admin.html", {  # ← FIXED
    "orders": orders,
    "foods": foods,
    "users": users
    })

@user_passes_test(is_admin)
def update_order_status(request, order_id, status):
    order = get_object_or_404(Order, id=order_id)
    order.status = status
    order.save()
    return redirect("admin_dashboard")

@user_passes_test(is_admin)
def add_food(request):
    if request.method == "POST":
        Food.objects.create(
            name=request.POST["name"],
            price=request.POST["price"],
            is_available=True
        )
    return redirect("admin_dashboard")

@user_passes_test(is_admin)
def delete_food(request, food_id):
    food = get_object_or_404(Food, id=food_id)
    food.delete()
    return redirect("admin_dashboard")

@user_passes_test(is_admin)
def delete_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    user.delete()
    return redirect("admin_dashboard")

# -------------------- Registration --------------------
def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Account created successfully! You can now log in.")
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, "orders/register.html", {"form": form})





def public_home(request):
    # Food list and prices (same as home)
    food_list = ["Chicken Adobo", "Sinigang na Baboy", "Lechon Kawali"]
    prices = {
        "Chicken Adobo": 120,
        "Sinigang na Baboy": 130,
        "Lechon Kawali": 150
    }
    food_items = [{"name": name, "price": prices.get(name, 100)} for name in food_list]

    return render(request, "orders/public_home.html", {"food_items": food_items})
