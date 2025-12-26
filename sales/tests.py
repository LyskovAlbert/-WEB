from django.test import TestCase, Client
from django.urls import reverse
from .models import MonthlySales
import json


class MonthlySalesModelTest(TestCase):
    """Тесты модели MonthlySales"""
    
    def setUp(self):
        self.sales = MonthlySales.objects.create(
            year=2024,
            month=1,
            product_name='Тестовый товар',
            quantity=100,
            revenue=50000.00
        )
    
    def test_model_creation(self):
        """Тест создания записи"""
        self.assertEqual(self.sales.year, 2024)
        self.assertEqual(self.sales.month, 1)
        self.assertEqual(self.sales.product_name, 'Тестовый товар')
        self.assertEqual(self.sales.quantity, 100)
        self.assertEqual(float(self.sales.revenue), 50000.00)
    
    def test_model_str(self):
        """Тест строкового представления"""
        expected = "Январь 2024 - Тестовый товар"
        self.assertEqual(str(self.sales), expected)
    
    def test_get_month_name(self):
        """Тест получения названия месяца"""
        self.assertEqual(self.sales.get_month_name(), 'Январь')


class SalesViewsTest(TestCase):
    """Тесты представлений"""
    
    def setUp(self):
        self.client = Client()
        # Создаем тестовые данные
        MonthlySales.objects.create(
            year=2024, month=1, product_name='Ноутбук',
            quantity=10, revenue=500000.00
        )
        MonthlySales.objects.create(
            year=2024, month=2, product_name='Смартфон',
            quantity=20, revenue=600000.00
        )
    
    def test_index_page_status(self):
        """Тест доступности главной страницы"""
        response = self.client.get(reverse('sales:index'))
        self.assertEqual(response.status_code, 200)
    
    def test_index_page_template(self):
        """Тест использования правильного шаблона"""
        response = self.client.get(reverse('sales:index'))
        self.assertTemplateUsed(response, 'sales/index.html')
    
    def test_table_page_status(self):
        """Тест доступности страницы таблицы"""
        response = self.client.get(reverse('sales:table'))
        self.assertEqual(response.status_code, 200)
    
    def test_table_page_template(self):
        """Тест использования правильного шаблона для таблицы"""
        response = self.client.get(reverse('sales:table'))
        self.assertTemplateUsed(response, 'sales/table.html')


class ChartAPITest(TestCase):
    """Тесты API для диаграмм"""
    
    def setUp(self):
        self.client = Client()
        # Создаем тестовые данные
        MonthlySales.objects.create(
            year=2024, month=1, product_name='Ноутбук',
            quantity=10, revenue=500000.00
        )
        MonthlySales.objects.create(
            year=2024, month=2, product_name='Ноутбук',
            quantity=15, revenue=750000.00
        )
        MonthlySales.objects.create(
            year=2024, month=1, product_name='Смартфон',
            quantity=20, revenue=600000.00
        )
    
    def test_line_chart_api(self):
        """Тест API линейного графика"""
        response = self.client.get('/api/chart-data/?type=line')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertIn('labels', data)
        self.assertIn('datasets', data)
        self.assertTrue(len(data['datasets']) > 0)
    
    def test_bar_chart_api(self):
        """Тест API гистограммы"""
        response = self.client.get('/api/chart-data/?type=bar')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertIn('labels', data)
        self.assertIn('datasets', data)
    
    def test_pie_chart_api(self):
        """Тест API круговой диаграммы"""
        response = self.client.get('/api/chart-data/?type=pie')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertIn('labels', data)
        self.assertIn('datasets', data)
    
    def test_invalid_chart_type(self):
        """Тест неверного типа диаграммы"""
        response = self.client.get('/api/chart-data/?type=invalid')
        self.assertEqual(response.status_code, 400)
    
    def test_api_with_year_filter(self):
        """Тест API с фильтром по году"""
        response = self.client.get('/api/chart-data/?type=line&year=2024')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertIn('labels', data)
    
    def test_api_with_product_filter(self):
        """Тест API с фильтром по товару"""
        response = self.client.get('/api/chart-data/?type=bar&product=Ноутбук')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertIn('labels', data)


class DatabaseQueryTest(TestCase):
    """Тесты запросов к базе данных"""
    
    def setUp(self):
        # Создаем тестовые данные
        for month in range(1, 13):
            MonthlySales.objects.create(
                year=2024, month=month, product_name='Ноутбук',
                quantity=10 * month, revenue=500000.00 * month
            )
    
    def test_total_records(self):
        """Тест подсчета записей"""
        count = MonthlySales.objects.count()
        self.assertEqual(count, 12)
    
    def test_filter_by_year(self):
        """Тест фильтрации по году"""
        sales = MonthlySales.objects.filter(year=2024)
        self.assertEqual(sales.count(), 12)
    
    def test_filter_by_product(self):
        """Тест фильтрации по товару"""
        sales = MonthlySales.objects.filter(product_name='Ноутбук')
        self.assertEqual(sales.count(), 12)
    
    def test_aggregate_revenue(self):
        """Тест агрегации выручки"""
        from django.db.models import Sum
        total = MonthlySales.objects.aggregate(total=Sum('revenue'))
        self.assertIsNotNone(total['total'])
        self.assertGreater(float(total['total']), 0)
