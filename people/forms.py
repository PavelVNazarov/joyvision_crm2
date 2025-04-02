# people/forms.py
from django import forms
from .models import *
from django.forms import inlineformset_factory, modelform_factory

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        widgets = {
            'created_at': forms.DateInput(attrs={'type': 'date'}),  # Виджет для выбора даты
        }
        fields = ['order_number', 'created_at', 'client_name', 'client_contact', 'comment']
        help_texts = {
            'order_number': 'Введите номер заказа',
            'created_at': 'Выберите дату создания заказа',
            'client_name': 'Имя клиента',
            'client_contact': 'Контактная информация клиента',
            'comment': 'Комментарий к заказу',
        }

class OrderCommentForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['comment']
        widgets = {
            'comment': forms.Textarea(attrs={'rows': 3})
        }


class CalculationForm(forms.ModelForm):
    class Meta:
        model = Calculation
        fields = ['material', 'quantity', 'discount']
        widgets = {
            'material': forms.Select(attrs={'class': 'material-select'}),
            'quantity': forms.NumberInput(attrs={'min': 1}),
            'discount': forms.NumberInput(attrs={'min': 0})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Убираем фильтрацию по количеству
        self.fields['material'].queryset = WarehouseItem.objects.all()


CalculationFormSet = forms.inlineformset_factory(
    Order,
    Calculation,
    form=CalculationForm,
    extra=1,
    can_delete=True,
    fields=['material', 'quantity', 'discount']
)


class InvoiceForm(forms.ModelForm):
    class Meta:
        model = Invoice
        fields = ['materials_cost', 'prices', 'discounts']  # Указываем необходимые поля
        help_texts = {
            'materials_cost': 'Введите стоимость расходных материалов',
            'prices': 'Введите цены',
            'discounts': 'Введите скидки',
        }

class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ['invoice_number', 'expense_date']
        widgets = {
            'expense_date': forms.DateInput(attrs={'type': 'date'})
        }


class ExpenseItemForm(forms.ModelForm):
    unit_price = forms.DecimalField(
        max_digits=10,
        decimal_places=2,
        widget=forms.TextInput(attrs={'readonly': True}),
        required=False  # Поле необязательно при валидации
    )

    class Meta:
        model = ExpenseItem
        fields = ['warehouse_item', 'quantity', 'unit_price', 'total_price']
        widgets = {
            'total_price': forms.TextInput(attrs={'readonly': True}),
            'warehouse_item': forms.Select(attrs={'class': 'material-select'})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Фильтруем только материалы с положительным количеством
        self.fields['warehouse_item'].queryset = WarehouseItem.objects.filter(quantity__gt=0)

        # Устанавливаем цену только если материал выбран
        if self.instance and self.instance.warehouse_item_id:
            warehouse_item = WarehouseItem.objects.get(id=self.instance.warehouse_item_id)
            self.initial['unit_price'] = warehouse_item.unit_price
        else:
            self.initial['unit_price'] = 0  # Значение по умолчанию


ExpenseItemFormSet = forms.modelformset_factory(
    ExpenseItem,
    form=ExpenseItemForm,
    extra=1,
    can_delete=True,
    validate_min=False  # Разрешаем пустые формы
)


class ReceiptForm(forms.ModelForm):
    class Meta:
        model = Receipt
        fields = ['invoice_number', 'delivery_date', 'supplier', 'total_amount', 'supplier_contact', 'comment']
        widgets = {
            'delivery_date': forms.DateInput(attrs={'type': 'date'}),
        }
        help_texts = {
            'invoice_number': 'Введите номер накладной',
            'delivery_date': 'Выберите дату доставки',
            'supplier': 'Введите имя поставщика',
            'total_amount': 'Введите общую сумму',
            'supplier_contact': 'Введите контакт поставщика',
            'comment': 'Комментарий',
        }


class ReceiptItemForm(forms.ModelForm):
    class Meta:
        model = ReceiptItem
        fields = ['warehouse_item', 'quantity']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Отображаем материалы с артикулом в названии
        self.fields['warehouse_item'].queryset = WarehouseItem.objects.all()
        self.fields['warehouse_item'].label_from_instance = lambda obj: f"{obj.name} ({obj.article})"

        # Валидация минимального количества
        self.fields['quantity'].widget.attrs['min'] = 1

    def clean_quantity(self):
        quantity = self.cleaned_data['quantity']
        if quantity < 1:
            raise forms.ValidationError("Количество не может быть меньше 1")
        return quantity


ReceiptItemFormSet = forms.modelformset_factory(
    ReceiptItem,
    form=ReceiptItemForm,
    extra=1,
    can_delete=True
)

class ProfitDocumentForm(forms.ModelForm):
    class Meta:
        model = Profit_document
        fields = ['created_dat', 'profit_name', 'sum', 'comment', 'comment_add']
        widgets = {
            'created_dat': forms.DateInput(
                format='%Y-%m-%d',
                attrs={'type': 'date'}
            ),
            'comment': forms.Textarea(attrs={'rows': 3}),
            'comment_add': forms.Textarea(attrs={'rows': 3}),
        }

class CostDocumentForm(forms.ModelForm):
    class Meta:
        model = Cost_document
        fields = ['created_dat', 'cost_name', 'sum', 'comment', 'comment_add']
        widgets = {
            'created_dat': forms.DateInput(
                format='%Y-%m-%d',
                attrs={'type': 'date'}
            ),
            'comment': forms.Textarea(attrs={'rows': 3}),
            'comment_add': forms.Textarea(attrs={'rows': 3}),
        }


class WarehouseItemForm(forms.ModelForm):
    class Meta:
        model = WarehouseItem
        fields = '__all__'  # Все поля по умолчанию

    def __init__(self, *args, **kwargs):
        is_editing = kwargs.pop('is_editing', False)
        super().__init__(*args, **kwargs)

        if is_editing:
            # Скрываем поля, которые нельзя редактировать
            self.fields['quantity'].widget = forms.HiddenInput()
            self.fields['purchase_cost'].widget = forms.HiddenInput()
            self.fields['sale_price'].widget = forms.HiddenInput()

class PriceChangeDocumentForm(forms.ModelForm):
    class Meta:
        model = PriceChangeDocument
        fields = ['change_type', 'reason', 'comment']
        widgets = {
            'reason': forms.Textarea(attrs={'rows': 3}),
            'comment': forms.Textarea(attrs={'rows': 3}),
        }

class PriceChangeItemForm(forms.ModelForm):
    class Meta:
        model = PriceChangeItem
        fields = ['material', 'new_price']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['material'].queryset = WarehouseItem.objects.all()
        self.fields['material'].label_from_instance = lambda obj: f"{obj.name} ({obj.article})"

PriceChangeItemFormSet = forms.inlineformset_factory(
    PriceChangeDocument,
    PriceChangeItem,
    form=PriceChangeItemForm,
    extra=1,
    can_delete=True
)


