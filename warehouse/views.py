# warehouse/views.py
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from people.models import *
from people.forms import *
from django.utils import timezone
from django.shortcuts import render, redirect
from django.forms import modelform_factory
from django.contrib import messages
from .models import PurchaseRequirement

def warehouse(request, storekeeper_id=None):
    if storekeeper_id:
        # Логика для обработки с storekeeper_id
        storekeeper = get_object_or_404(People, id=storekeeper_id)
        return render(request, 'warehouse.html',{'name': storekeeper.name, 'storekeeper_id': storekeeper_id})  # Передаем storekeeper_id
    else:
        # Логика для обработки без id
        return render(request, 'warehouse.html', {'name': 'аноним'})

def warehouse_list(request, storekeeper_id=None):
    storekeeper = get_object_or_404(People, id=storekeeper_id)  # Получаем информацию о storekeeper_
    orders = Order.objects.filter(status='warehouse')  # Фильтруем заказы по статусу
    return render(request, 'warehouse_list.html', {'orders': orders, 'storekeeper_id': storekeeper_id, 'name': storekeeper.name})


def create_expense_receipt(request, storekeeper_id, order_id):
    storekeeper = get_object_or_404(People, id=storekeeper_id)
    order = get_object_or_404(Order, id=order_id)

    if request.method == 'POST':
        expense_form = ExpenseForm(request.POST)
        item_formset = ExpenseItemFormSet(
            request.POST,
            prefix='items',
            queryset=ExpenseItem.objects.none()
        )
        comment_form = OrderCommentForm(request.POST, instance=order)

        if all([expense_form.is_valid(), item_formset.is_valid(), comment_form.is_valid()]):
            try:
                # Сохраняем накладную с временной суммой
                expense = expense_form.save(commit=False)
                expense.total_amount = 0
                expense.save()

                total_amount = 0  # Общая сумма накладной

                # Обработка элементов
                for form in item_formset:
                    if form.cleaned_data and not form.cleaned_data.get('DELETE', False):
                        item = form.save(commit=False)
                        item.expense = expense

                        if not item.warehouse_item:
                            continue

                        warehouse_item = item.warehouse_item

                        # Проверка остатков
                        if warehouse_item.quantity < item.quantity:
                            raise ValidationError(
                                f"Недостаточно {warehouse_item.name} (доступно: {warehouse_item.quantity})")

                        # Расчет цен
                        item.unit_price = warehouse_item.sale_price
                        item.total_price = item.quantity * warehouse_item.sale_price
                        item.save()

                        # Списание
                        warehouse_item.quantity -= item.quantity
                        warehouse_item.save()

                        total_amount += item.total_price  # Суммируем

                # Обновляем общую сумму
                expense.total_amount = total_amount
                expense.save()

                # Обновление заказа
                order.status = 'workshop'
                order.sent_to_workshop_at = timezone.now()
                order.storekeeper_name = storekeeper
                order.save()
                comment_form.save()

                messages.success(request, "✅ Накладная сохранена! Заказ передан в цех.")
                return redirect('warehouse_list', storekeeper_id=storekeeper_id)

            except ValidationError as e:
                messages.error(request, str(e))
        else:
            # Вывод ошибок валидации
            for form in item_formset:
                if form.errors:
                    messages.error(request, f"Ошибка в строке: {form.errors}")
    else:
        # GET-запрос
        expense_form = ExpenseForm()
        item_formset = ExpenseItemFormSet(prefix='items', queryset=ExpenseItem.objects.none())
        comment_form = OrderCommentForm(instance=order)

    return render(request, 'create_expense_receipt.html', {
        'expense_form': expense_form,
        'item_formset': item_formset,
        'comment_form': comment_form,
        'storekeeper_id': storekeeper_id,
        'order_id': order_id,
        'name': storekeeper.name
    })



def create_receipt(request, storekeeper_id):
    storekeeper = get_object_or_404(People, id=storekeeper_id)

    if request.method == 'POST':
        receipt_form = ReceiptForm(request.POST)
        item_formset = ReceiptItemFormSet(request.POST)

        if receipt_form.is_valid() and item_formset.is_valid():
            receipt = receipt_form.save(commit=False)
            receipt.storekeeper_name = storekeeper

            # Рассчитываем общую сумму по стоимости закупки
            total = sum(
                form.cleaned_data['quantity'] * form.cleaned_data['warehouse_item'].purchase_cost
                for form in item_formset
                if form.cleaned_data and not form.cleaned_data.get('DELETE', False)
            )
            receipt.total_amount = total
            receipt.save()

            # Сохраняем элементы накладной
            for form in item_formset:
                if form.cleaned_data and not form.cleaned_data.get('DELETE', False):
                    item = form.save(commit=False)
                    item.receipt = receipt
                    item.total_price = item.quantity * item.warehouse_item.purchase_cost
                    item.save()

                    # Обновляем складские запасы
                    warehouse_item = item.warehouse_item
                    warehouse_item.quantity += item.quantity
                    warehouse_item.save()

            return redirect('warehouse_list_receipt', storekeeper_id=storekeeper_id)
    else:
        receipt_form = ReceiptForm()
        item_formset = ReceiptItemFormSet(queryset=ReceiptItem.objects.none())

    return render(request, 'create_receipt.html', {
        'receipt_form': receipt_form,
        'item_formset': item_formset,
        'storekeeper_id': storekeeper_id,
        'name': storekeeper.name
    })


def warehouse_list_receipt(request, storekeeper_id):
    storekeeper = get_object_or_404(People, id=storekeeper_id)  # Получаем информацию о кладовщике
    receipts = Receipt.objects.all()  # Получаем все накладные
    return render(request, 'warehouse_list_receipt.html', {
        'receipts': receipts,
        'storekeeper_id': storekeeper_id,
        'name': storekeeper.name
    })


def warehouse_edit_order(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    storekeeper_id = request.GET.get('storekeeper_id')
    storekeeper = None
    if storekeeper_id:
        storekeeper = get_object_or_404(People, id=storekeeper_id)

    materials = order.calculations.all()
    insufficient_materials = []
    sufficient_materials = []

    # Проверяем наличие материалов на складе
    for material in materials:
        if material.material.quantity >= material.quantity:
            sufficient_materials.append(material)
        else:
            insufficient_materials.append({
                'name': material.material.name,
                'article': material.material.article,
                'needed': material.quantity - material.material.quantity
            })

    if request.method == 'POST':
        # Сохраняем комментарий ДО проверки выполнения заказа
        new_comment = request.POST.get('comment', '')
        if new_comment != order.comment:
            order.comment = new_comment
            order.save()

        # Обработка выполнения заказа
        if 'execute_order' in request.POST and not insufficient_materials:
            for material in sufficient_materials:
                material.material.quantity -= material.quantity
                material.material.save()

            order.status = 'workshop'
            order.sent_to_workshop_at = timezone.now()
            if storekeeper:
                order.storekeeper_name = storekeeper
            order.save()
            return redirect('warehouse_list', storekeeper_id=storekeeper_id)

    context_storekeeper_id = storekeeper_id or (order.storekeeper_name.id if order.storekeeper_name else None)
    return render(request, 'warehouse_edit_order.html', {
        'order': order,
        'name': storekeeper.name if storekeeper else "Неизвестно",
        'storekeeper_id': context_storekeeper_id,
        'sufficient_materials': sufficient_materials,
        'insufficient_materials': insufficient_materials,
    })


def warehouse_materials(request, storekeeper_id):
    """Список материалов на складе"""
    storekeeper = get_object_or_404(People, id=storekeeper_id)
    materials = WarehouseItem.objects.all()
    return render(request, 'warehouse_materials.html', {
        'materials': materials,
        'storekeeper_id': storekeeper_id,
        'name': storekeeper.name
    })


def add_material(request, storekeeper_id):
    storekeeper = get_object_or_404(People, id=storekeeper_id)

    if request.method == 'POST':
        form = WarehouseItemForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('warehouse_materials', storekeeper_id=storekeeper_id)
    else:
        form = WarehouseItemForm()  # Показываем все поля

    return render(request, 'add_material.html', {
        'form': form,
        'storekeeper_id': storekeeper_id,
        'name': storekeeper.name
    })


def adjust_material(request, storekeeper_id, material_id):
    storekeeper = get_object_or_404(People, id=storekeeper_id)
    material = get_object_or_404(WarehouseItem, id=material_id)

    if request.method == 'POST':
        form = WarehouseItemForm(request.POST, instance=material, is_editing=True)
        if form.is_valid():
            form.save()
            messages.success(request, "✅ Изменения сохранены!")
            return redirect('warehouse_materials', storekeeper_id=storekeeper_id)
    else:
        form = WarehouseItemForm(instance=material, is_editing=True)  # Скрываем ненужные поля

    return render(request, 'adjust_material.html', {
        'form': form,
        'material': material,
        'storekeeper_id': storekeeper_id,
        'name': storekeeper.name
    })


