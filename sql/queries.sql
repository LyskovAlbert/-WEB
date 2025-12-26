-- Полезные SQL запросы для работы с базой данных

-- 1. Получить все продажи за определенный год
SELECT * FROM monthly_sales WHERE year = 2024 ORDER BY month;

-- 2. Получить общую выручку по каждому товару
SELECT 
    product_name,
    SUM(quantity) as total_quantity,
    SUM(revenue) as total_revenue
FROM monthly_sales
GROUP BY product_name
ORDER BY total_revenue DESC;

-- 3. Получить помесячную выручку за год
SELECT 
    month,
    SUM(revenue) as monthly_revenue
FROM monthly_sales
WHERE year = 2024
GROUP BY month
ORDER BY month;

-- 4. Получить топ-3 месяца по выручке
SELECT 
    year,
    month,
    SUM(revenue) as total_revenue
FROM monthly_sales
GROUP BY year, month
ORDER BY total_revenue DESC
LIMIT 3;

-- 5. Средняя выручка по месяцам для каждого товара
SELECT 
    product_name,
    AVG(revenue) as avg_monthly_revenue,
    AVG(quantity) as avg_monthly_quantity
FROM monthly_sales
GROUP BY product_name;

-- 6. Динамика продаж конкретного товара
SELECT 
    year,
    month,
    quantity,
    revenue
FROM monthly_sales
WHERE product_name = 'Ноутбук'
ORDER BY year, month;

-- 7. Общая статистика по всем продажам
SELECT 
    COUNT(*) as total_records,
    SUM(quantity) as total_units_sold,
    SUM(revenue) as total_revenue,
    AVG(revenue) as avg_revenue
FROM monthly_sales;

-- 8. Продажи по кварталам
SELECT 
    year,
    CASE 
        WHEN month IN (1,2,3) THEN 'Q1'
        WHEN month IN (4,5,6) THEN 'Q2'
        WHEN month IN (7,8,9) THEN 'Q3'
        ELSE 'Q4'
    END as quarter,
    SUM(revenue) as quarter_revenue
FROM monthly_sales
GROUP BY year, quarter
ORDER BY year, quarter;
