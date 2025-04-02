# workshop/views.py

from django.shortcuts import render, redirect, get_object_or_404
from people.models import *
from people.forms import *
from django.utils import timezone

def workshop(request, hard_worker_id=None):
    if hard_worker_id:
        # Логика для обработки с hard_worker_id
        hard_worker = get_object_or_404(People, id=hard_worker_id)
        return render(request, 'workshop.html', {'name': hard_worker.name, 'hard_worker_id': hard_worker_id})  # Передаем hard_worker_id
    else:
        # Логика для обработки без id
        return render(request, 'workshop.html', {'name': 'аноним'})

def workshop_list(request, hard_worker_id=None):
    hard_worker = get_object_or_404(People, id=hard_worker_id)  # Получаем информацию о hard_worker
    orders = Order.objects.filter(status='workshop')  # Фильтруем заказы по статусу
    return render(request, 'workshop_list.html', {'orders': orders, 'hard_worker_id': hard_worker_id, 'name': hard_worker.name})

def invoice_detail(request, invoice_id):
    invoice = get_object_or_404(Invoice, id=invoice_id)
    return render(request, 'invoice_detail.html', {'invoice': invoice})

def receipt_detail(request, receipt_id):
    receipt = get_object_or_404(Receipt, id=receipt_id)
    return render(request, 'receipt_detail.html', {'receipt': receipt})


def workshop_edit_order(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    hard_worker_id = request.GET.get('hard_worker_id')
    hard_worker = None
    if hard_worker_id:
        hard_worker = get_object_or_404(People, id=hard_worker_id)

    if request.method == 'POST':
        comment_form = OrderCommentForm(request.POST, instance=order)

        # Всегда сохраняем комментарий при отправке формы
        if comment_form.is_valid():
            comment_form.save()

            # Обработка завершения заказа
            if 'complete_order' in request.POST:
                order.status = 'reports'
                order.completed_at = timezone.now()
                if hard_worker:
                    order.hard_worker_name = hard_worker
                order.save()
                return redirect('workshop_list', hard_worker_id=hard_worker_id)

    else:
        comment_form = OrderCommentForm(instance=order)

    context_hard_worker_id = hard_worker_id or (order.hard_worker_name.id if order.hard_worker_name else None)
    return render(request, 'workshop_edit_order.html', {
        'comment_form': comment_form,
        'order': order,
        'name': hard_worker.name if hard_worker else "Неизвестно",
        'hard_worker_id': context_hard_worker_id
    })

