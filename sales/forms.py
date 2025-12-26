from django import forms
from .models import MonthlySales
import datetime


class MonthlySalesForm(forms.ModelForm):
    """Форма для добавления/редактирования продаж"""
    
    class Meta:
        current_year = datetime.datetime.now().year
        max_year = current_year
        model = MonthlySales
        fields = ['year', 'month', 'product_name', 'quantity', 'revenue']
        widgets = {
            'year': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': f'Например: {current_year}',
                'min': '2020',
                'max':  str(max_year)
            }),
            'month': forms.Select(attrs={'class': 'form-select'}),
            'product_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Например: Ноутбук'
            }),
            'quantity': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Например: 100',
                'min': '1'
            }),
            'revenue': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Например: 500000.00',
                'min': '0.01',
                'step': '0.01'
            }),
        }
        labels = {
            'year': 'Год',
            'month': 'Месяц',
            'product_name': 'Название товара',
            'quantity': 'Количество проданных единиц',
            'revenue': 'Выручка (руб.)',
        }