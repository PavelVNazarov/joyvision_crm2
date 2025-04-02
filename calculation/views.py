# calculation/views.py
from django.shortcuts import render, redirect, get_object_or_404
from people.models import *
from people.forms import *
from django.utils import timezone

def calculation(request, calculator_id=None):
    if calculator_id:
        calculator = get_object_or_404(People, id=calculator_id)
        return render(request, 'calculation.html',{'name': calculator.name, 'calculator_id': calculator_id})  # Передаем calculator_id
    else:
        # Логика для обработки без id
        return render(request, 'calculation.html', {'name': 'аноним'})

def calculation_list(request, calculator_id=None):
    calculator = get_object_or_404(People, id=calculator_id)  # Получаем информацию о calculator
    orders = Order.objects.filter(status='calculation')  # Фильтруем заказы по статусу
    return render(request, 'calculation_list.html', {'orders': orders, 'calculator_id': calculator_id, 'name': calculator.name})


def edit_calculation(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    calculator_id = request.GET.get('calculator_id')
    calculator = get_object_or_404(People, id=calculator_id) if calculator_id else None

    # Настройка формсета
    CalculationFormSet = forms.inlineformset_factory(
        Order,
        Calculation,
        form=CalculationForm,
        extra=1,
        can_delete=True  # Разрешаем удаление материалов
    )

    if request.method == 'POST':
        formset = CalculationFormSet(request.POST, instance=order)
        comment_form = OrderCommentForm(request.POST, instance=order)

        if 'calculate' in request.POST or 'save' in request.POST:
            if formset.is_valid() and comment_form.is_valid():
                # Сохраняем комментарий в любом случае
                comment_form.save()

        # Обработка кнопки "Рассчитать"
        if 'calculate' in request.POST:
            if formset.is_valid() and comment_form.is_valid():
                total = 0
                order.calculator_name = calculator
                order.sent_to_warehouse_at = timezone.now()
                order.save()
                for form in formset:
                    if form.cleaned_data.get('material'):
                        quantity = form.cleaned_data['quantity']
                        discount = form.cleaned_data['discount']
                        price = form.cleaned_data['material'].sale_price
                        total += (quantity * price) - discount
                return render(request, 'edit_calculation.html', {
                    'order': order,
                    'formset': formset,
                    'comment_form': comment_form,
                    'calculator_id': calculator_id,
                    'name': calculator.name if calculator else "Неизвестно",
                    'preview_total': total
                })

        # Обработка кнопки "Сохранить"
        elif 'save' in request.POST:
            if formset.is_valid() and comment_form.is_valid():
                comment_form.save()
                instances = formset.save(commit=False)
                total = 0
                for instance in instances:
                    if instance.material:
                        instance.price = instance.material.sale_price
                        total += (instance.quantity * instance.price) - instance.discount
                        instance.save()
                order.total_sum = total
                order.status = 'warehouse'  # Меняем статус на 'warehouse'
                order.calculator_name = calculator  # Сохраняем имя расчетчика
                order.sent_to_warehouse_at = timezone.now()  # Сохраняем дату отправки на склад
                order.save()
                return redirect('calculation_list', calculator_id=calculator_id)

    else:
        formset = CalculationFormSet(instance=order)
        comment_form = OrderCommentForm(instance=order)

    return render(request, 'edit_calculation.html', {
        'order': order,
        'formset': formset,
        'comment_form': comment_form,
        'calculator_id': calculator_id,
        'name': calculator.name if calculator else "Неизвестно",
    })
