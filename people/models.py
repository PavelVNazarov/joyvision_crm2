# people/models.py
from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError


class Invoice(models.Model):
    # Поля для накладной (пример)
    materials_cost = models.DecimalField(max_digits=10, decimal_places=2)  # Стоимость расходных материалов
    prices = models.DecimalField(max_digits=10, decimal_places=2)          # Цены
    discounts = models.DecimalField(max_digits=10, decimal_places=2)       # Скидки
    total_sum = models.DecimalField(max_digits=10, decimal_places=2)       # Итоговая сумма

    def __str__(self):
        return f"Накладная на сумму {self.total_sum}"


class People(models.Model):  # Люди в базе данных
    login = models.CharField(max_length=10)  # Логин для входа
    password = models.CharField(max_length=10)  # Пароль для входа
    name = models.CharField(max_length=100)  # Имя для документов
    email = models.EmailField(max_length=254) # Email для связи
    role = models.CharField(max_length=10)  # Роль

    def __str__(self):
        return self.name

class Order(models.Model):
    order_number = models.IntegerField(unique=True)
    created_at = models.DateField(default=timezone.now)
    client_name = models.CharField(max_length=255, default='Не указано')
    client_contact = models.CharField(max_length=255, default='Не указано')
    comment = models.TextField(blank=True, null=True)

    STATUS_CHOICES = [
        ('orders', 'Приемка'),
        ('calculation', 'Расчет'),
        ('warehouse', 'Склад'),
        ('workshop', 'Цех'),
        ('reports', 'К оплате'),
        ('completed', 'Завершен'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='orders')
    receptionist = models.ForeignKey(People, on_delete=models.SET_NULL, null=True, related_name='orders_created')
    sent_to_calculation_at = models.DateTimeField(blank=True, null=True)
    calculator_name = models.ForeignKey(People, on_delete=models.SET_NULL, null=True, related_name='orders_calculated')
    invoice = models.OneToOneField(Invoice, on_delete=models.SET_NULL, null=True, related_name='order')
    sent_to_warehouse_at = models.DateTimeField(blank=True, null=True)
    storekeeper_name = models.ForeignKey(People, on_delete=models.SET_NULL, null=True, related_name='orders_stored')
    sent_to_workshop_at = models.DateTimeField(blank=True, null=True)
    completed_at = models.DateTimeField(blank=True, null=True)
    hard_worker_name = models.ForeignKey(People, on_delete=models.SET_NULL, null=True,
                                         related_name='orders_hard_worked')
    paid_at = models.DateTimeField(blank=True, null=True)
    total_sum = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    accountant_name = models.ForeignKey(People, on_delete=models.SET_NULL, null=True, related_name='orders_accounted')

    def __str__(self):
        return f"Заказ №{self.order_number} от {self.created_at.strftime('%Y-%m-%d')} - {self.client_name}"


class Supplier(models.Model):
    name = models.CharField(max_length=255)

class Receipt(models.Model):
    invoice_number = models.CharField(max_length=20)  # номер накладной
    delivery_date = models.DateField()   # дата поставки
    supplier = models.CharField(max_length=255)     # поставщик
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)    # сумма
    supplier_contact = models.CharField(max_length=255, blank=True)     # контакт поставщика
    comment = models.TextField(blank=True)    # комментарий
    storekeeper_name = models.ForeignKey(People, on_delete=models.SET_NULL, null=True)

    def clean(self):
        super().clean()
        year = self.delivery_date.year
        if Receipt.objects.filter(invoice_number=self.invoice_number, delivery_date__year=year).exists():
            raise ValidationError(f'Накладная с номером {self.invoice_number} уже существует для года {year}.')

    def save(self, *args, **kwargs):
        self.full_clean()  # Вызываем валидацию перед сохранением
        super().save(*args, **kwargs)

class Item(models.Model):
    name = models.CharField(max_length=255)
    quantity = models.PositiveIntegerField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)


class WarehouseItem(models.Model):
    name = models.CharField(max_length=255, verbose_name='Название')
    article = models.CharField(max_length=50, unique=True, verbose_name='Артикул')
    category = models.CharField(max_length=100, blank=True, verbose_name='Категория')
    system_type = models.CharField( max_length=100, blank=True, verbose_name='Тип системы')
    unit = models.CharField(max_length=10, blank=True, verbose_name='Единица измерения')
    quantity = models.PositiveIntegerField(verbose_name='Количество')
    purchase_cost = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Стоимость закупки')
    sale_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена продажи')
    notes = models.TextField(blank=True, verbose_name='Примечания')

    def __str__(self):
        return f"{self.name} ({self.article})"


# Приходные накладные
class ReceiptItem(models.Model):
    receipt = models.ForeignKey(Receipt, related_name='items', on_delete=models.CASCADE)
    warehouse_item = models.ForeignKey(WarehouseItem, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)

    def save(self, *args, **kwargs):
        # Заменяем unit_price на sale_price
        self.total_price = self.quantity * self.warehouse_item.sale_price
        super().save(*args, **kwargs)



# Расходные накладные
class Expense(models.Model):
    invoice_number = models.CharField(max_length=100)
    expense_date = models.DateField()
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)

class ExpenseItem(models.Model):
    expense = models.ForeignKey(Expense, related_name='items', on_delete=models.CASCADE)
    warehouse_item = models.ForeignKey(WarehouseItem, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)

    def save(self, *args, **kwargs):
        # Заменяем unit_price на sale_price
        self.total_price = self.quantity * self.warehouse_item.sale_price
        super().save(*args, **kwargs)



class Profit_document (models.Model): #  документ о прибылях
    created_dat = models.DateField(null=True, blank=True) # дата создания документа
    profit_name = models.CharField(max_length=255, blank=True, null=True) # вид платежа
    sum = models.DecimalField(max_digits=10, decimal_places=2)  # сумма
    comment = models.TextField(blank=True, null=True) # комментарий
    comment_add = models.TextField(blank=True, null=True)  # дополнение

class Cost_document (models.Model): #  документ о прибылях
    created_dat = models.DateField(null=True, blank=True) # дата создания документа
    cost_name = models.CharField(max_length=255, blank=True, null=True) # вид платежа
    sum = models.DecimalField(max_digits=10, decimal_places=2)  # сумма
    comment = models.TextField(blank=True, null=True) # комментарий
    comment_add = models.TextField(blank=True, null=True)  # дополнение


class PriceChangeDocument(models.Model):
    CHANGE_TYPE_CHOICES = [
        ('markup', 'Наценка'),
        ('discount', 'Уценка'),
    ]

    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    change_type = models.CharField(
        max_length=10,
        choices=CHANGE_TYPE_CHOICES,
        verbose_name='Тип изменения'
    )
    reason = models.TextField(verbose_name='Основание')
    comment = models.TextField(blank=True, verbose_name='Комментарий')
    accountant = models.ForeignKey(
        People,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='Учетчик'
    )

    def __str__(self):
        return f"Док. №{self.id} от {self.created_at.strftime('%d.%m.%Y')}"


class PriceChangeItem(models.Model):
    document = models.ForeignKey(
        PriceChangeDocument,
        related_name='items',
        on_delete=models.CASCADE
    )
    material = models.ForeignKey(
        WarehouseItem,
        on_delete=models.CASCADE,
        verbose_name='Материал'
    )
    new_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='Новая цена'
    )

    def save(self, *args, **kwargs):
        # Обновляем цену материала при сохранении
        self.material.sale_price = self.new_price
        self.material.save()
        super().save(*args, **kwargs)


class Calculation(models.Model):
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='calculations',
        verbose_name='Заказ'
    )
    material = models.ForeignKey(
        WarehouseItem,
        on_delete=models.SET_NULL,  # Разрешаем null временно
        null=True,
        blank=True,
        verbose_name='Материал'
    )
    quantity = models.PositiveIntegerField(
        default=1,
        verbose_name='Количество'
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        editable=False,
        default=0  # Временное значение
    )
    discount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name='Скидка на позицию'
    )

    def save(self, *args, **kwargs):
        if self.material:  # Автоматически устанавливаем цену только при наличии материала
            self.price = self.material.sale_price
        super().save(*args, **kwargs)

    @property
    def total(self):
        return (self.quantity * self.price) - self.discount