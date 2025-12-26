from django.contrib import admin
from .models import MonthlySales


@admin.register(MonthlySales)
class MonthlySalesAdmin(admin.ModelAdmin):
    list_display = ['year', 'get_month_display', 'product_name', 'quantity', 'revenue', 'edit_link']
    list_filter = ['year', 'month', 'product_name']
    search_fields = ['product_name', 'year']  # Поиск по товару и году
    ordering = ['-year', '-month']
    
    # Поля для формы добавления/редактирования
    fields = ['year', 'month', 'product_name', 'quantity', 'revenue']
    
    # Делаем поля кликабельными для редактирования
    list_display_links = ['year', 'get_month_display', 'product_name']
    
    # Отображение названия месяца вместо числа в списке
    def get_month_display(self, obj):
        return obj.get_month_display()
    get_month_display.short_description = 'Месяц'
    get_month_display.admin_order_field = 'month'
    
    # Добавляем явную ссылку "Изменить"
    def edit_link(self, obj):
        from django.urls import reverse
        from django.utils.html import format_html
        url = reverse('admin:sales_monthlysales_change', args=[obj.pk])
        return format_html('<a href="{}">Изменить</a>', url)
    edit_link.short_description = 'Действия'
