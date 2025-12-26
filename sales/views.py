from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.db.models import Sum, Count
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from .models import MonthlySales
from .forms import MonthlySalesForm


def index(request):
    """Главная страница с диаграммами"""
    years = MonthlySales.objects.values_list('year', flat=True).distinct().order_by('-year')
    products = MonthlySales.objects.values_list('product_name', flat=True).distinct().order_by('product_name')
    
    context = {
        'years': years,
        'products': products,
    }
    return render(request, 'sales/index.html', context)


def get_chart_data(request):
    """API для получения данных для диаграмм"""
    chart_type = request.GET.get('type', 'line')
    year = request.GET.get('year')
    products = request.GET.getlist('products[]')  # Множественный выбор товаров
    
    # Фильтрация данных
    queryset = MonthlySales.objects.all()
    if year:
        queryset = queryset.filter(year=int(year))
    if products:
        queryset = queryset.filter(product_name__in=products)
    
    if chart_type == 'line':
        # Линейный график - выручка по месяцам
        # Словарь для названий месяцев
        month_names = {
            1: 'Январь', 2: 'Февраль', 3: 'Март', 4: 'Апрель',
            5: 'Май', 6: 'Июнь', 7: 'Июль', 8: 'Август',
            9: 'Сентябрь', 10: 'Октябрь', 11: 'Ноябрь', 12: 'Декабрь'
        }
        
        # Получаем данные из БД
        data = queryset.values('month', 'year').annotate(
            total_revenue=Sum('revenue')
        ).order_by('year', 'month')
        
        if year:
            # Если выбран конкретный год - показываем все 12 месяцев этого года
            # Создаём словарь для быстрого поиска
            data_dict = {item['month']: float(item['total_revenue']) for item in data}
            
            labels = []
            values = []
            for m in range(1, 13):
                labels.append(f"{month_names[m]} {year}")
                # Если данных нет - ставим 0
                values.append(data_dict.get(m, 0))
        else:
            # Если год не выбран - показываем от первого до последнего месяца с данными
            if data:
                # Создаём словарь для быстрого поиска
                data_dict = {(item['year'], item['month']): float(item['total_revenue']) for item in data}
                
                # Находим первый и последний месяц с данными
                first_item = data[0]
                last_item = data[len(data) - 1]
                
                start_year = first_item['year']
                start_month = first_item['month']
                end_year = last_item['year']
                end_month = last_item['month']
                
                # Формируем все месяцы от первого до последнего
                labels = []
                values = []
                
                current_year = start_year
                current_month = start_month
                
                while (current_year < end_year) or (current_year == end_year and current_month <= end_month):
                    labels.append(f"{month_names[current_month]} {current_year}")
                    values.append(data_dict.get((current_year, current_month), 0))
                    
                    # Переход к следующему месяцу
                    current_month += 1
                    if current_month > 12:
                        current_month = 1
                        current_year += 1
            else:
                labels = []
                values = []
        
        return JsonResponse({
            'labels': labels,
            'datasets': [{
                'label': 'Выручка (руб.)',
                'data': values,
                'borderColor': 'rgb(75, 192, 192)',
                'backgroundColor': 'rgba(75, 192, 192, 0.2)',
                'tension': 0.1
            }]
        })
    
    elif chart_type == 'bar':
        # Гистограмма - количество продаж по товарам
        data = queryset.values('product_name').annotate(
            total_quantity=Sum('quantity')
        ).order_by('-total_quantity')
        
        labels = [item['product_name'] for item in data]
        values = [item['total_quantity'] for item in data]
        
        return JsonResponse({
            'labels': labels,
            'datasets': [{
                'label': 'Количество проданных единиц',
                'data': values,
                'backgroundColor': [
                    'rgba(255, 99, 132, 0.7)',
                    'rgba(54, 162, 235, 0.7)',
                    'rgba(255, 206, 86, 0.7)',
                    'rgba(75, 192, 192, 0.7)',
                    'rgba(153, 102, 255, 0.7)',
                ],
                'borderColor': [
                    'rgba(255, 99, 132, 1)',
                    'rgba(54, 162, 235, 1)',
                    'rgba(255, 206, 86, 1)',
                    'rgba(75, 192, 192, 1)',
                    'rgba(153, 102, 255, 1)',
                ],
                'borderWidth': 1
            }]
        })
    
    elif chart_type == 'pie':
        # Круговая диаграмма - доля выручки по товарам
        data = queryset.values('product_name').annotate(
            total_revenue=Sum('revenue')
        ).order_by('-total_revenue')
        
        labels = [item['product_name'] for item in data]
        values = [float(item['total_revenue']) for item in data]
        
        return JsonResponse({
            'labels': labels,
            'datasets': [{
                'label': 'Выручка (руб.)',
                'data': values,
                'backgroundColor': [
                    'rgba(255, 99, 132, 0.8)',
                    'rgba(54, 162, 235, 0.8)',
                    'rgba(255, 206, 86, 0.8)',
                    'rgba(75, 192, 192, 0.8)',
                    'rgba(153, 102, 255, 0.8)',
                    'rgba(255, 159, 64, 0.8)',
                ],
                'borderWidth': 2
            }]
        })
    
    return JsonResponse({'error': 'Invalid chart type'}, status=400)


def sales_table(request):
    """Страница с таблицей данных"""
    year = request.GET.get('year')
    month = request.GET.get('month')
    products = request.GET.getlist('products')  # Множественный выбор товаров
    
    queryset = MonthlySales.objects.all()
    if year:
        queryset = queryset.filter(year=int(year))
    if month:
        queryset = queryset.filter(month=int(month))
    if products:
        queryset = queryset.filter(product_name__in=products)
    
    # Добавляем пагинацию
    sales_list = queryset.order_by('-year', '-month')
    paginator = Paginator(sales_list, 20)  # 20 записей на страницу
    
    page_number = request.GET.get('page')
    sales_data = paginator.get_page(page_number)
    
    years = MonthlySales.objects.values_list('year', flat=True).distinct().order_by('-year')
    all_products = MonthlySales.objects.values_list('product_name', flat=True).distinct().order_by('product_name')
    
    # Список месяцев для фильтра
    months = [
        (1, 'Январь'), (2, 'Февраль'), (3, 'Март'), (4, 'Апрель'),
        (5, 'Май'), (6, 'Июнь'), (7, 'Июль'), (8, 'Август'),
        (9, 'Сентябрь'), (10, 'Октябрь'), (11, 'Ноябрь'), (12, 'Декабрь')
    ]
    
    context = {
        'sales_data': sales_data,
        'years': years,
        'products': all_products,
        'months': months,
        'selected_year': year,
        'selected_month': month,
        'selected_products': products,
    }
    return render(request, 'sales/table.html', context)


@login_required
def manage_sales(request):
    """Страница управления данными о продажах"""
    # Получаем параметры фильтрации
    year = request.GET.get('year')
    month = request.GET.get('month')
    products = request.GET.getlist('products')
    
    # Фильтруем данные
    queryset = MonthlySales.objects.all()
    if year:
        queryset = queryset.filter(year=int(year))
    if month:
        queryset = queryset.filter(month=int(month))
    if products:
        queryset = queryset.filter(product_name__in=products)
    
    # Получаем отфильтрованные записи с пагинацией
    sales_list = queryset.order_by('-year', '-month', 'product_name')
    paginator = Paginator(sales_list, 10)  # 10 записей на страницу
    
    page_number = request.GET.get('page')
    sales_data = paginator.get_page(page_number)
    
    # Данные для фильтров
    years = MonthlySales.objects.values_list('year', flat=True).distinct().order_by('-year')
    all_products = MonthlySales.objects.values_list('product_name', flat=True).distinct().order_by('product_name')
    
    # Список месяцев для фильтра
    months = [
        (1, 'Январь'), (2, 'Февраль'), (3, 'Март'), (4, 'Апрель'),
        (5, 'Май'), (6, 'Июнь'), (7, 'Июль'), (8, 'Август'),
        (9, 'Сентябрь'), (10, 'Октябрь'), (11, 'Ноябрь'), (12, 'Декабрь')
    ]
    
    context = {
        'sales_data': sales_data,
        'years': years,
        'products': all_products,
        'months': months,
        'selected_year': year,
        'selected_month': month,
        'selected_products': products,
    }
    return render(request, 'sales/manage.html', context)


@login_required
def add_sale(request):
    """Добавление новой записи о продажах"""
    if request.method == 'POST':
        form = MonthlySalesForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Запись успешно добавлена!')
            return redirect('sales:manage')
        else:
            messages.error(request, 'Ошибка при добавлении записи. Проверьте данные.')
    else:
        form = MonthlySalesForm()
    
    context = {
        'form': form,
        'title': 'Добавить запись',
        'action': 'add'
    }
    return render(request, 'sales/form.html', context)


@login_required
def edit_sale(request, pk):
    """Редактирование записи о продажах"""
    sale = get_object_or_404(MonthlySales, pk=pk)
    
    if request.method == 'POST':
        form = MonthlySalesForm(request.POST, instance=sale)
        if form.is_valid():
            form.save()
            messages.success(request, 'Запись успешно обновлена!')
            return redirect('sales:manage')
        else:
            messages.error(request, 'Ошибка при обновлении записи. Проверьте данные.')
    else:
        form = MonthlySalesForm(instance=sale)
    
    context = {
        'form': form,
        'title': 'Редактировать запись',
        'action': 'edit',
        'sale': sale
    }
    return render(request, 'sales/form.html', context)


@login_required
def delete_sale(request, pk):
    """Удаление записи о продажах"""
    sale = get_object_or_404(MonthlySales, pk=pk)
    
    if request.method == 'POST':
        sale.delete()
        messages.success(request, 'Запись успешно удалена!')
        return redirect('sales:manage')
    
    context = {
        'sale': sale
    }
    return render(request, 'sales/confirm_delete.html', context)


def user_login(request):
    """Страница входа в систему"""
    if request.user.is_authenticated:
        return redirect('sales:index')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            next_url = request.GET.get('next', 'sales:index')
            return redirect(next_url)
        else:
            messages.error(request, 'Неверное имя пользователя или пароль.')
    
    return render(request, 'sales/login.html')


def user_logout(request):
    """Выход из системы"""
    logout(request)
    return redirect('sales:index')
