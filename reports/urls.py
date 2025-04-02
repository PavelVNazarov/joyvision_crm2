# reports/urls.py
from django.urls import path
from .views import *

urlpatterns = [
    path('reports_edit_order/<int:order_id>/', reports_edit_order, name='reports_edit_order'),
    path('reports/<int:accountant_id>/', reports, name='reports'),
    path('reports_list/<int:accountant_id>/', reports_list, name='reports_list'),
    # Новые пути для документов
    path('profit_docs/<int:accountant_id>/', profit_docs_list, name='profit_docs_list'),
    path('profit_create/<int:accountant_id>/', profit_doc_create, name='profit_doc_create'),
    path('profit_edit/<int:pk>/<int:accountant_id>/', profit_doc_edit, name='profit_doc_edit'),
    path('profit_delete/<int:pk>/<int:accountant_id>/', profit_doc_delete, name='profit_doc_delete'),
    path('cost_docs/<int:accountant_id>/', cost_docs_list, name='cost_docs_list'),
    path('cost_create/<int:accountant_id>/', cost_doc_create, name='cost_doc_create'),
    path('cost_edit/<int:pk>/<int:accountant_id>/', cost_doc_edit, name='cost_doc_edit'),
    path('cost_delete/<int:pk>/<int:accountant_id>/', cost_doc_delete, name='cost_doc_delete'),
    path('financial_reports/<int:accountant_id>/', financial_reports, name='financial_reports'),
    path('price_changes/<int:accountant_id>/', price_change_list, name='price_change_list'),
    path('price_change_create/<int:accountant_id>/', price_change_create, name='price_change_create'),
    path('price_change_delete/<int:pk>/<int:accountant_id>/', price_change_delete, name='price_change_delete'),
]
