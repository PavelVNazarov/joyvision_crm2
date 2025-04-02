# warehouse/urls.py
# from django.urls import path
# from .views import *
#
# urlpatterns = [
#     path('materials/<int:storekeeper_id>/', warehouse_materials, name='warehouse_materials'),
#     path('add-material/<int:storekeeper_id>/', add_material, name='add_material'),
#     path('adjust-material/<int:storekeeper_id>/<int:material_id>/', adjust_material, name='adjust_material'),
#     path('warehouse_edit_order/<int:order_id>/', warehouse_edit_order, name='warehouse_edit_order'),
#     path('warehouse/<int:storekeeper_id>/', warehouse, name='warehouse'),
#     path('warehouse_list/<int:storekeeper_id>/', warehouse_list, name='warehouse_list'),
#     path('warehouse_list_receipt/<int:storekeeper_id>/', warehouse_list_receipt, name='warehouse_list_receipt'),
#     path('create_expense_receipt/<int:storekeeper_id>/<int:order_id>/', create_expense_receipt, name='create_expense_receipt'),
#     path('warehouse/receipts/<int:storekeeper_id>/', warehouse_list_receipt, name='warehouse_list_receipt'),
#     path('warehouse/create_receipt/<int:storekeeper_id>/', create_receipt, name='create_receipt'),
# ]
from django.urls import path
from .views import *

urlpatterns = [
    path('materials/<int:storekeeper_id>/', warehouse_materials, name='warehouse_materials'),
    path('add-material/<int:storekeeper_id>/', add_material, name='add_material'),
    path('adjust-material/<int:storekeeper_id>/<int:material_id>/', adjust_material, name='adjust_material'),
    path('warehouse_edit_order/<int:order_id>/', warehouse_edit_order, name='warehouse_edit_order'),
    path('warehouse/<int:storekeeper_id>/', warehouse, name='warehouse'),
    path('warehouse_list/<int:storekeeper_id>/', warehouse_list, name='warehouse_list'),
    path('warehouse_list_receipt/<int:storekeeper_id>/', warehouse_list_receipt, name='warehouse_list_receipt'),
    path('create_expense_receipt/<int:storekeeper_id>/<int:order_id>/', create_expense_receipt, name='create_expense_receipt'),
    path('warehouse/receipts/<int:storekeeper_id>/', warehouse_list_receipt, name='warehouse_list_receipt'),
    path('warehouse/create_receipt/<int:storekeeper_id>/', create_receipt, name='create_receipt'),
]