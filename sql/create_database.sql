-- Скрипт для создания базы данных PostgreSQL
-- Выполните этот скрипт от имени пользователя postgres

-- Создание базы данных
CREATE DATABASE sales_charts_db
    WITH 
    OWNER = postgres
    ENCODING = 'UTF8'
    LC_COLLATE = 'Russian_Russia.1251'
    LC_CTYPE = 'Russian_Russia.1251'
    TABLESPACE = pg_default
    CONNECTION LIMIT = -1;

COMMENT ON DATABASE sales_charts_db IS 'База данных для системы построения диаграмм продаж';

-- Подключение к созданной базе данных
\c sales_charts_db;

-- Создание таблицы monthly_sales
CREATE TABLE IF NOT EXISTS monthly_sales (
    id SERIAL PRIMARY KEY,
    year INTEGER NOT NULL,
    month INTEGER NOT NULL CHECK (month >= 1 AND month <= 12),
    product_name VARCHAR(200) NOT NULL,
    quantity INTEGER NOT NULL CHECK (quantity >= 0),
    revenue NUMERIC(12, 2) NOT NULL CHECK (revenue >= 0),
    UNIQUE (year, month, product_name)
);

COMMENT ON TABLE monthly_sales IS 'Таблица с данными о продажах по месяцам';
COMMENT ON COLUMN monthly_sales.year IS 'Год продажи';
COMMENT ON COLUMN monthly_sales.month IS 'Месяц продажи (1-12)';
COMMENT ON COLUMN monthly_sales.product_name IS 'Название товара';
COMMENT ON COLUMN monthly_sales.quantity IS 'Количество проданных единиц';
COMMENT ON COLUMN monthly_sales.revenue IS 'Выручка в рублях';

-- Создание индексов для оптимизации запросов
CREATE INDEX idx_monthly_sales_year ON monthly_sales(year);
CREATE INDEX idx_monthly_sales_product ON monthly_sales(product_name);
CREATE INDEX idx_monthly_sales_year_month ON monthly_sales(year, month);

-- Вставка тестовых данных
INSERT INTO monthly_sales (year, month, product_name, quantity, revenue) VALUES
(2025, 1, 'Ноутбук', 45, 2250000.00),
(2025, 2, 'Ноутбук', 52, 2600000.00),
(2025, 3, 'Ноутбук', 48, 2400000.00),
(2025, 4, 'Ноутбук', 55, 2750000.00),
(2025, 5, 'Ноутбук', 60, 3000000.00),
(2025, 6, 'Ноутбук', 58, 2900000.00),
(2025, 7, 'Ноутбук', 62, 3100000.00),
(2025, 8, 'Ноутбук', 50, 2500000.00),
(2025, 9, 'Ноутбук', 65, 3250000.00),
(2025, 10, 'Ноутбук', 70, 3500000.00),
(2025, 11, 'Ноутбук', 68, 3400000.00),
(2025, 12, 'Ноутбук', 75, 3750000.00),

-- Ноутбуки за 2024 год
(2024, 1, 'Ноутбук', 45, 2250000.00),
(2024, 2, 'Ноутбук', 52, 2600000.00),
(2024, 3, 'Ноутбук', 48, 2400000.00),
(2024, 4, 'Ноутбук', 55, 2750000.00),
(2024, 5, 'Ноутбук', 60, 3000000.00),
(2024, 6, 'Ноутбук', 58, 2900000.00),
(2024, 7, 'Ноутбук', 62, 3100000.00),
(2024, 8, 'Ноутбук', 50, 2500000.00),
(2024, 9, 'Ноутбук', 65, 3250000.00),
(2024, 10, 'Ноутбук', 70, 3500000.00),
(2024, 11, 'Ноутбук', 68, 3400000.00),
(2024, 12, 'Ноутбук', 75, 3750000.00),

-- Смартфоны за 2024 год
(2024, 1, 'Смартфон', 120, 3600000.00),
(2024, 2, 'Смартфон', 135, 4050000.00),
(2024, 3, 'Смартфон', 140, 4200000.00),
(2024, 4, 'Смартфон', 130, 3900000.00),
(2024, 5, 'Смартфон', 145, 4350000.00),
(2024, 6, 'Смартфон', 150, 4500000.00),
(2024, 7, 'Смартфон', 155, 4650000.00),
(2024, 8, 'Смартфон', 148, 4440000.00),
(2024, 9, 'Смартфон', 160, 4800000.00),
(2024, 10, 'Смартфон', 165, 4950000.00),
(2024, 11, 'Смартфон', 170, 5100000.00),
(2024, 12, 'Смартфон', 180, 5400000.00),

-- Планшеты за 2024 год
(2024, 1, 'Планшет', 30, 900000.00),
(2024, 2, 'Планшет', 35, 1050000.00),
(2024, 3, 'Планшет', 32, 960000.00),
(2024, 4, 'Планшет', 38, 1140000.00),
(2024, 5, 'Планшет', 40, 1200000.00),
(2024, 6, 'Планшет', 42, 1260000.00),
(2024, 7, 'Планшет', 45, 1350000.00),
(2024, 8, 'Планшет', 38, 1140000.00),
(2024, 9, 'Планшет', 48, 1440000.00),
(2024, 10, 'Планшет', 50, 1500000.00),
(2024, 11, 'Планшет', 52, 1560000.00),
(2024, 12, 'Планшет', 55, 1650000.00);

-- Проверка данных
SELECT COUNT(*) as total_records FROM monthly_sales;
SELECT product_name, SUM(quantity) as total_quantity, SUM(revenue) as total_revenue 
FROM monthly_sales 
GROUP BY product_name;
