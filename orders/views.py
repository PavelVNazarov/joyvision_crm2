# orders/views.py
from django.shortcuts import render, redirect, get_object_or_404
from people.models import *
from people.forms import *

def orders(request, receptionist_id=None):
    if receptionist_id:
        receptionist = get_object_or_404(People, id=receptionist_id)
        return render(request, 'orders.html', {'name': receptionist.name, 'receptionist_id': receptionist_id})  # Передаем receptionist_id
    else:
        return render(request, 'orders.html', {'name': 'аноним', 'receptionist_id': None})

def order(request):
    return render(request, 'order.html')

def order_list(request, receptionist_id=None):
    receptionist = get_object_or_404(People, id=receptionist_id)  # Получаем информацию о receptionist
    orders = Order.objects.filter(status='orders')  # Фильтруем заказы по статусу
    return render(request, 'order_list.html', {
        'orders': orders,
        'receptionist_id': receptionist_id,  # ← Важно!
        'name': receptionist.name
    })

def new_order(request, receptionist_id):
    receptionist = get_object_or_404(People, id=receptionist_id)

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.receptionist = receptionist  # Устанавливаем приемщика
            order.status = 'orders'  # Статус по умолчанию

            # Если заказ сразу принимается
            if request.POST.get('action') == 'accept':
                order.status = 'calculation'
                order.sent_to_calculation_at = timezone.now()  # Фиксируем время перевода к расчетам

            order.save()
            return redirect('order_list', receptionist_id=receptionist_id)
    else:
        # Устанавливаем текущую дату по умолчанию
        form = OrderForm(initial={'created_at': timezone.now().date()})

    return render(request, 'new_order.html', {
        'form': form,
        'name': receptionist.name,
        'receptionist_id': receptionist_id
    })


def edit_order(request, order_id, receptionist_id):
    order = get_object_or_404(Order, id=order_id)
    current_receptionist = get_object_or_404(People, id=receptionist_id)

    if request.method == 'POST':
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            order = form.save(commit=False)

            if request.POST.get('action') == 'accept':
                order.status = 'calculation'
                order.sent_to_calculation_at = timezone.now()
                order.receptionist = current_receptionist

            order.save()
            return redirect('order_list', receptionist_id=receptionist_id)
    else:
        form = OrderForm(instance=order)

    return render(request, 'edit_order.html', {
        'form': form,
        'receptionist_id': receptionist_id,
        'receptionist_name': current_receptionist.name
    })

def delete_order(request, order_id, receptionist_id):
    order = get_object_or_404(Order, id=order_id)
    order.delete()
    return redirect('order_list', receptionist_id=receptionist_id)

