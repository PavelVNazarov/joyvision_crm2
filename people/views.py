# people/views.py
from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from .forms import *

def home(request):
    return render(request, 'home.html')

def login_view(request):
    if request.method == 'POST':
        login = request.POST['login']
        password = request.POST['password']
        if login == 'superadmin' and password == '1234':
            return redirect('personnel_officer_dashboard')
        try:
            user = People.objects.get(login=login)
            if user.password == password:
                role = user.role
                if role == 'accountant':
                    return redirect('reports', accountant_id=user.id)  # Передаем ID учетчика
                elif role == 'receptionist':
                    return redirect('orders', receptionist_id=user.id)  # Передаем ID приемщика
                elif role == 'storekeeper':
                    return redirect('warehouse', storekeeper_id=user.id)  # Передаем ID кладовщика
                elif role == 'hard_worker':
                    return redirect('workshop', hard_worker_id=user.id)  # Передаем ID работяги
                elif role == 'calculator':
                    return redirect('calculation', calculator_id=user.id)  # Передаем ID расчетчика
            return render(request, 'login.html', {'error': 'Неверный логин или пароль'})
        except People.DoesNotExist:
            return render(request, 'login.html', {'error': 'Неверный логин или пароль'})
    return render(request, 'login.html')

def add_receptionist(request):
    if request.method == 'POST':
        login = request.POST['login']
        password = request.POST['password']
        name = request.POST['name']
        email = request.POST['email']
        People.objects.create(login=login, name=name, email=email, password=password, role='receptionist')
        return redirect('personnel_officer_dashboard')
    return render(request, 'add_receptionist.html')

def edit_receptionist(request, receptionist_id):
    user = get_object_or_404(People, id=receptionist_id, role='receptionist')
    if request.method == 'POST':
        user.login = request.POST['login']
        user.email = request.POST['email']
        user.password = request.POST['password']
        user.name = request.POST['name']
        user.role = request.POST['role']
        user.save()
        return redirect('personnel_officer_dashboard')
    return render(request, 'edit_receptionist.html', {'receptionist': user})

def add_accountant(request):
    if request.method == 'POST':
        login = request.POST['login']
        password = request.POST['password']
        name = request.POST['name']
        email = request.POST['email']
        People.objects.create(login=login, name=name, email=email, password=password, role='accountant')
        return redirect('personnel_officer_dashboard')
    return render(request, 'add_accountant.html')

def edit_accountant(request, accountant_id):
    user = get_object_or_404(People, id=accountant_id, role='accountant')
    if request.method == 'POST':
        user.login = request.POST['login']
        user.email = request.POST['email']
        user.password = request.POST['password']
        user.name = request.POST['name']
        user.role = request.POST['role']
        user.save()
        return redirect('personnel_officer_dashboard')
    return render(request, 'edit_accountant.html', {'accountant': user})

def delete_accountant(request, accountant_id):
    people = get_object_or_404(People, id=accountant_id, role='accountant')
    people.delete()
    return redirect('personnel_officer_dashboard')

def delete_receptionist(request, receptionist_id):
    people = get_object_or_404(People, id=receptionist_id, role='receptionist')
    people.delete()
    return redirect('personnel_officer_dashboard')

def personnel_officer_receptionist(request):
    receptionists = People.objects.filter(role='receptionist')
    return render(request, 'personnel_officer_receptionist.html', {'receptionists': receptionists})

def personnel_officer_accountant(request):
    accountants = People.objects.filter(role='accountant')
    return render(request, 'personnel_officer_accountant.html', {'accountants': accountants})


def personnel_officer_dashboard(request):
    return render(request, 'personnel_officer_dashboard.html')

def personnel_officer_calculator(request):
    calculators = People.objects.filter(role='calculator')
    return render(request, 'personnel_officer_calculator.html', {'calculators': calculators})

def personnel_officer_hard_worker(request):
    hard_workers = People.objects.filter(role='hard_worker')
    return render(request, 'personnel_officer_hard_worker.html', {'hard_workers': hard_workers})

def personnel_officer_storekeeper(request):
    storekeepers = People.objects.filter(role='storekeeper')
    return render(request, 'personnel_officer_storekeeper.html', {'storekeepers': storekeepers})


def personnel_officer_order(request):
    selected_statuses = request.GET.getlist('statuses')  # Получаем выбранные статусы
    start_date = request.GET.get('start_date')  # Получаем начальную дату
    end_date = request.GET.get('end_date')  # Получаем конечную дату

    # Фильтруем заказы по статусам и датам
    orders = Order.objects.all()

    if selected_statuses:
        orders = orders.filter(status__in=selected_statuses)

    if start_date:
        orders = orders.filter(created_at__gte=start_date)

    if end_date:
        orders = orders.filter(created_at__lte=end_date)

    # Если нет выбранных статусов и нет заказов, возвращаем пустой список
    if not selected_statuses:
        orders = []

    # Подсчет общей суммы только если есть заказы
    total_sum = sum(order.total_sum for order in orders if order.total_sum is not None)

    return render(request, 'personnel_officer_order.html', {
        'orders': orders,
        'selected_statuses': selected_statuses,
        'total_sum': total_sum,
    })

def personnel_officer_edit_order(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    receptionist = order.receptionist  # Получаем объект People (может быть None)
    receptionist_name = receptionist.name if receptionist else "Неизвестно"  # Проверка на None
    return render(request, 'personnel_officer_edit_order.html', {
        'order': order,
        'receptionist_name': receptionist_name,  # Передаем строку, а не объект
    })

def admin_delete_order(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    order.delete()
    return redirect('personnel_officer_order')

def add_calculator(request):
    if request.method == 'POST':
        login = request.POST['login']
        password = request.POST['password']
        name = request.POST['name']
        email = request.POST['email']
        People.objects.create(login=login, name=name, email=email, password=password, role='calculator')
        return redirect('personnel_officer_dashboard')
    return render(request, 'add_calculator.html')

def edit_calculator(request, calculator_id):
    user = get_object_or_404(People, id=calculator_id, role='calculator')
    if request.method == 'POST':
        user.login = request.POST['login']
        user.email = request.POST['email']
        user.password = request.POST['password']
        user.name = request.POST['name']
        user.role = request.POST['role']
        user.save()
        return redirect('personnel_officer_dashboard')
    return render(request, 'edit_calculator.html', {'calculator': user})

def delete_calculator(request, calculator_id):
    people = get_object_or_404(People, id=calculator_id, role='calculator')
    people.delete()
    return redirect('personnel_officer_dashboard')

def add_storekeeper(request):
    if request.method == 'POST':
        login = request.POST['login']
        password = request.POST['password']
        name = request.POST['name']
        email = request.POST['email']
        People.objects.create(login=login, name=name, email=email, password=password, role='storekeeper')
        return redirect('personnel_officer_dashboard')
    return render(request, 'add_storekeeper.html')

def edit_storekeeper(request, storekeeper_id):
    user = get_object_or_404(People, id=storekeeper_id, role='storekeeper')
    if request.method == 'POST':
        user.login = request.POST['login']
        user.email = request.POST['email']
        user.password = request.POST['password']
        user.name = request.POST['name']
        user.role = request.POST['role']
        user.save()
        return redirect('personnel_officer_dashboard')
    return render(request, 'edit_storekeeper.html', {'storekeeper': user})

def delete_storekeeper(request, storekeeper_id):
    people = get_object_or_404(People, id=storekeeper_id, role='storekeeper')
    people.delete()
    return redirect('personnel_officer_dashboard')

def add_hard_worker(request):
    if request.method == 'POST':
        login = request.POST['login']
        password = request.POST['password']
        name = request.POST['name']
        email = request.POST['email']
        People.objects.create(login=login, name=name, email=email, password=password, role='hard_worker')
        return redirect('personnel_officer_dashboard')
    return render(request, 'add_hard_worker.html')

def edit_hard_worker(request, hard_worker_id):
    user = get_object_or_404(People, id=hard_worker_id, role='hard_worker')
    if request.method == 'POST':
        user.login = request.POST['login']
        user.email = request.POST['email']
        user.password = request.POST['password']
        user.name = request.POST['name']
        user.role = request.POST['role']
        user.save()
        return redirect('personnel_officer_dashboard')
    return render(request, 'edit_hard_worker.html', {'hard_worker': user})

def delete_hard_worker(request, hard_worker_id):
    people = get_object_or_404(People, id=hard_worker_id, role='hard_worker')
    people.delete()
    return redirect('personnel_officer_dashboard')

def personnel_officer_receipt(request):
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    receipts = Receipt.objects.all()

    if start_date:
        receipts = receipts.filter(delivery_date__gte=start_date)

    if end_date:
        receipts = receipts.filter(delivery_date__lte=end_date)

    if not start_date and not end_date:
        receipts = []

    total_sum = sum(receipt.total_amount for receipt in receipts)

    return render(request, 'personnel_officer_receipt.html', {
        'receipts': receipts,
        'total_sum': total_sum,
        'start_date': start_date,
        'end_date': end_date,
    })


def personnel_officer_edit_receipt(request, receipt_id):
    receipt = get_object_or_404(Receipt, id=receipt_id)
    # receptionist = receipt.receptionist  # Получаем объект People (может быть None)
    # receptionist_name = receptionist.name if receptionist else "Неизвестно"  # Проверка на None
    return render(request, 'personnel_officer_edit_receipt.html', {
        'receipt': receipt,
        # 'receptionist_name': receptionist_name,  # Передаем строку, а не объект
    })

def admin_delete_receipt(request, receipt_id):
    receipt = get_object_or_404(Receipt, id=receipt_id)
    receipt.delete()
    return redirect('personnel_officer_receipt')
