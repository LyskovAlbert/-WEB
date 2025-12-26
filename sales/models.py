from django.db import models


class MonthlySales(models.Model):
    """Модель для хранения данных о продажах по месяцам"""
    
    MONTHS = [
        (1, 'Январь'), (2, 'Февраль'), (3, 'Март'), (4, 'Апрель'),
        (5, 'Май'), (6, 'Июнь'), (7, 'Июль'), (8, 'Август'),
        (9, 'Сентябрь'), (10, 'Октябрь'), (11, 'Ноябрь'), (12, 'Декабрь')
    ]
    
    year = models.IntegerField(verbose_name='Год')
    month = models.IntegerField(choices=MONTHS, verbose_name='Месяц')
    product_name = models.CharField(max_length=200, verbose_name='Название товара')
    quantity = models.IntegerField(verbose_name='Количество проданных единиц')
    revenue = models.DecimalField(max_digits=12, decimal_places=2, verbose_name='Выручка')
    
    class Meta:
        db_table = 'monthly_sales'
        verbose_name = 'Продажа по месяцам'
        verbose_name_plural = 'Продажи по месяцам'
        ordering = ['year', 'month']
        unique_together = ['year', 'month', 'product_name']
    
    def __str__(self):
        return f"{self.get_month_display()} {self.year} - {self.product_name}"
    
    def get_month_name(self):
        return dict(self.MONTHS)[self.month]
