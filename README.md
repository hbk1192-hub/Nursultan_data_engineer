# Проект: Аналитика данных для сети салонов красоты

В этом репозитории я демонстрирую навыки работы с данными, объединяя технический стек с опытом управления бизнесом.

### Что внутри:
1. **beauty_analytics1.sql**: Сложные запросы для расчета прибыли мастеров. Использую CTE и Window Functions (Rank, Partition By).
2. **data_cleaning_script.py**: Скрипт на Python (Pandas) для очистки "сырых" данных из CRM. Реализована нормализация телефонов, дат и имен.

### Мой стек:
- **SQL**: PostgreSQL / MySQL (Advanced SELECTs)
- **Python**: Pandas, NumPy, Regular Expressions
- **Инструменты**: Git, GitHub, VS Code

-- Задача: Разбить клиентов на когорты по месяцу первого визита 
-- и рассчитать Retention (возвращаемость) на 2-й и 3-й месяцы.

WITH first_visits AS (
    -- Находим дату первого визита для каждого клиента
    SELECT 
        client_id, 
        DATE_TRUNC('month', MIN(visit_date)) AS cohort_month
    FROM visits
    GROUP BY 1
),
visit_logs AS (
    -- Сопоставляем каждый визит с месяцем когорты
    SELECT 
        v.client_id,
        fv.cohort_month,
        DATE_TRUNC('month', v.visit_date) AS visit_month,
        -- Оконная функция: считаем порядковый номер месяца активности клиента
        DENSE_RANK() OVER (PARTITION BY v.client_id ORDER BY DATE_TRUNC('month', v.visit_date)) AS month_number
    FROM visits v
    JOIN first_visits fv ON v.client_id = fv.client_id
)
SELECT 
    cohort_month,
    COUNT(DISTINCT client_id) AS total_clients,
    -- Считаем возвращаемость через условную агрегацию
    ROUND(COUNT(DISTINCT CASE WHEN month_number = 2 THEN client_id END) * 100.0 / COUNT(DISTINCT client_id), 2) AS retention_month_2,
    ROUND(COUNT(DISTINCT CASE WHEN month_number = 3 THEN client_id END) * 100.0 / COUNT(DISTINCT client_id), 2) AS retention_month_3
FROM visit_logs
GROUP BY 1
ORDER BY 1;


-- Задача: Найти ТОП-3 мастеров по выручке в каждом месяце 
-- и их долю в общей выручке салона.

WITH master_revenue AS (
    SELECT 
        DATE_TRUNC('month', visit_date) AS report_month,
        master_name,
        SUM(service_price) AS monthly_revenue
    FROM visits
    GROUP BY 1, 2
),
ranked_masters AS (
    SELECT 
        report_month,
        master_name,
        monthly_revenue,
        -- Оконная функция для ранжирования
        RANK() OVER (PARTITION BY report_month ORDER BY monthly_revenue DESC) as master_rank,
        -- Процент от общей выручки месяца
        ROUND(monthly_revenue * 100.0 / SUM(monthly_revenue) OVER (PARTITION BY report_month), 2) as revenue_share
    FROM master_revenue
)
SELECT * 
FROM ranked_masters 
WHERE master_rank <= 3;
