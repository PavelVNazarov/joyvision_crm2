# urls.py
from django.urls import path
from .views import *

urlpatterns = [
    path('orders/<int:receptionist_id>/', orders, name='orders'),
    path('new_order/<int:receptionist_id>/', new_order, name='new_order'),
    # path('edit_order/<int:order_id>/', edit_order, name='edit_order'),
    path('edit_order/<int:order_id>/<int:receptionist_id>/', edit_order, name='edit_order'),
    path('order_list/<int:receptionist_id>/', order_list, name='order_list'),
    path('order_delete/<int:order_id>/<int:receptionist_id>/', delete_order, name='delete_order'),
]
