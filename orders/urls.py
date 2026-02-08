from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('public-home/', views.public_home, name='public_home'),  # anyone can view

    path('orders/', views.order_summary, name='order_summary'),
    path('add_order/', views.add_order, name='add_order'),
    path('remove_order/<int:order_id>/', views.remove_order, name='remove_order'),
    path('update_order/<int:order_id>/', views.update_order, name='update_order'),
    path('place_order/', views.place_order, name='place_order'),

    # Food details page
    path('food/<str:food_name>/', views.food_detail, name='food_detail'),

    # User accounts
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='orders/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),

    path("admin-dashboard/", views.admin_dashboard, name="admin_dashboard"),
    path("order/<int:order_id>/<str:status>/", views.update_order_status, name="update_order_status"),
    path("add-food/", views.add_food, name="add_food"),
    path("delete-food/<int:food_id>/", views.delete_food, name="delete_food"),
    path("delete-user/<int:user_id>/", views.delete_user, name="delete_user"),

]

