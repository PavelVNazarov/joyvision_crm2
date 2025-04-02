from django.shortcuts import render, redirect, get_object_or_404
from people.models import *
from people.forms import *
from django.utils import timezone
from django.urls import reverse

def reports(request, accountant_id=None):
    if accountant_id:
        # Логика для обработки с accountant_id
        accountant = get_object_or_404(People, id=accountant_id)
        return render(request, 'reports.html', {'name': accountant.name, 'accountant_id': accountant_id})  # Передаем accountant_id
    else:
        # Логика для обработки без id
        return render(request, 'reports.html', {'name': 'аноним'})

def reports_list(request, accountant_id=None):
    accountant = get_object_or_404(People, id=accountant_id)  # Получаем информацию о accountant
    orders = Order.objects.filter(status='reports')  # Фильтруем заказы по статусу
    return render(request, 'reports_list.html', {'orders': orders, 'accountant_id': accountant_id, 'name': accountant.name})

def reports_edit_order(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    accountant_id = request.GET.get('accountant_id')
    accountant = None

    if accountant_id:
        accountant = get_object_or_404(People, id=accountant_id)

    if request.method == 'POST':
        # Используем форму для комментария
        comment_form = OrderCommentForm(request.POST, instance=order)

        if comment_form.is_valid():
            # Сохраняем комментарий
            comment_form.save()

            # Обновляем статус и дату
            order.status = 'completed'
            order.paid_at = timezone.now()

            if accountant:
                order.accountant_name = accountant

            order.save()
            return redirect('reports_list', accountant_id=accountant_id)
    else:
        comment_form = OrderCommentForm(instance=order)

    context_accountant_id = accountant_id or (order.accountant_name.id if order.accountant_name else None)

    return render(request, 'reports_edit_order.html', {
        'comment_form': comment_form,
        'order': order,
        'name': accountant.name if accountant else "Неизвестно",
        'accountant_id': context_accountant_id
    })


# Документы прибылей
def profit_docs_list(request, accountant_id):
    accountant = get_object_or_404(People, id=accountant_id)
    docs = Profit_document.objects.all().order_by('-created_dat')
    return render(request, 'profit_docs_list.html', {
        'docs': docs,
        'accountant_id': accountant_id,
        'name': accountant.name
    })


def profit_doc_create(request, accountant_id):
    accountant = get_object_or_404(People, id=accountant_id)
    if request.method == 'POST':
        form = ProfitDocumentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('profit_docs_list', accountant_id=accountant_id)
    else:
        form = ProfitDocumentForm(initial={'created_dat': timezone.now()})
    return render(request, 'doc_edit.html', {
        'form': form,
        'title': 'Создать документ прибыли',
        'accountant_id': accountant_id,
        'name': accountant.name
    })


def profit_doc_edit(request, pk, accountant_id):
    accountant = get_object_or_404(People, id=accountant_id)
    doc = get_object_or_404(Profit_document, id=pk)
    if request.method == 'POST':
        form = ProfitDocumentForm(request.POST, instance=doc)
        if form.is_valid():
            form.save()
            return redirect('profit_docs_list', accountant_id=accountant_id)
    else:
        form = ProfitDocumentForm(instance=doc)
    return render(request, 'doc_edit.html', {
        'form': form,
        'title': 'Редактировать документ прибыли',
        'accountant_id': accountant_id,
        'name': accountant.name
    })


def profit_doc_delete(request, pk, accountant_id):
    accountant = get_object_or_404(People, id=accountant_id)
    doc = get_object_or_404(Profit_document, id=pk)
    if request.method == 'POST':
        doc.delete()
        return redirect('profit_docs_list', accountant_id=accountant_id)
    return render(request, 'doc_confirm_delete.html', {
        'doc': doc,
        'accountant_id': accountant_id,
        'name': accountant.name,
        'doc_type': 'profit'
    })


# Документы затрат
def cost_docs_list(request, accountant_id):
    accountant = get_object_or_404(People, id=accountant_id)
    docs = Cost_document.objects.all().order_by('-created_dat')
    return render(request, 'cost_docs_list.html', {
        'docs': docs,
        'accountant_id': accountant_id,
        'name': accountant.name
    })


def cost_doc_create(request, accountant_id):
    accountant = get_object_or_404(People, id=accountant_id)
    if request.method == 'POST':
        form = CostDocumentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('cost_docs_list', accountant_id=accountant_id)
    else:
        form = CostDocumentForm(initial={'created_dat': timezone.now()})
    return render(request, 'doc_edit.html', {
        'form': form,
        'title': 'Создать документ затрат',
        'accountant_id': accountant_id,
        'name': accountant.name
    })


def cost_doc_edit(request, pk, accountant_id):
    accountant = get_object_or_404(People, id=accountant_id)
    doc = get_object_or_404(Cost_document, id=pk)
    if request.method == 'POST':
        form = CostDocumentForm(instance=doc)
        if form.is_valid():
            form.save()
            return redirect('cost_docs_list', accountant_id=accountant_id)
    else:
        form = CostDocumentForm(instance=doc)
    return render(request, 'doc_edit.html', {
        'form': form,
        'title': 'Редактировать документ затрат',
        'accountant_id': accountant_id,
        'name': accountant.name
    })


def cost_doc_delete(request, pk, accountant_id):
    accountant = get_object_or_404(People, id=accountant_id)
    doc = get_object_or_404(Cost_document, id=pk)
    if request.method == 'POST':
        doc.delete()
        return redirect('cost_docs_list', accountant_id=accountant_id)
    return render(request, 'doc_confirm_delete.html', {
        'doc': doc,
        'accountant_id': accountant_id,
        'name': accountant.name,
        'doc_type': 'cost'
    })


# Финансовые отчеты
def financial_reports(request, accountant_id):
    accountant = get_object_or_404(People, id=accountant_id)
    if request.method == 'POST':
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')

        profits = Profit_document.objects.filter(
            created_dat__gte=start_date,
            created_dat__lte=end_date
        )
        costs = Cost_document.objects.filter(
            created_dat__gte=start_date,
            created_dat__lte=end_date
        )
        total_profit = sum(p.sum for p in profits)
        total_cost = sum(c.sum for c in costs)

        return render(request, 'financial_report_result.html', {
            'start_date': start_date,
            'end_date': end_date,
            'profits': profits,
            'costs': costs,
            'total_profit': total_profit,
            'total_cost': total_cost,
            'accountant_id': accountant_id,
            'name': accountant.name
        })

    return render(request, 'financial_report_form.html', {
        'accountant_id': accountant_id,
        'name': accountant.name
    })


def price_change_list(request, accountant_id):
    accountant = get_object_or_404(People, id=accountant_id)
    docs = PriceChangeDocument.objects.all().order_by('-created_at')
    return render(request, 'price_change_list.html', {
        'docs': docs,
        'accountant_id': accountant_id,
        'name': accountant.name
    })


def price_change_create(request, accountant_id):
    accountant = get_object_or_404(People, id=accountant_id)

    if request.method == 'POST':
        doc_form = PriceChangeDocumentForm(request.POST)
        item_formset = PriceChangeItemFormSet(request.POST)

        if doc_form.is_valid() and item_formset.is_valid():
            doc = doc_form.save(commit=False)
            doc.accountant = accountant
            doc.save()

            item_formset.instance = doc
            item_formset.save()

            return redirect('price_change_list', accountant_id=accountant_id)
    else:
        doc_form = PriceChangeDocumentForm()
        item_formset = PriceChangeItemFormSet()

    return render(request, 'price_change_edit.html', {
        'doc_form': doc_form,
        'item_formset': item_formset,
        'title': 'Создать документ изменения цен',
        'accountant_id': accountant_id,
        'name': accountant.name
    })


def price_change_delete(request, pk, accountant_id):
    accountant = get_object_or_404(People, id=accountant_id)
    doc = get_object_or_404(PriceChangeDocument, id=pk)

    if request.method == 'POST':
        doc.delete()
        return redirect('price_change_list', accountant_id=accountant_id)

    return render(request, 'price_change_confirm_delete.html', {
        'doc': doc,
        'accountant_id': accountant_id,
        'name': accountant.name
    })


