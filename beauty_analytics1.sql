/* 
ЦЕЛЬ ЗАПРОСА: Анализ эффективности работы персонала и расчет чистой прибыли с учетом операционных расходов.
Используемые инструменты: CTE, JOIN, Агрегатные и Оконные функции (Window Functions).
*/
WITH StaffPerformance AS (
    SELECT 
        s.staff_id,
        s.name AS staff_name,
        s.specialization,
        v.visit_date,
        ser.price AS revenue,
        -- Расчет чистой прибыли: цена минус расходники (10%) и минус комиссия мастера (40%)
        (ser.price * 0.5) AS net_profit 
    FROM Staff s
    JOIN Visits v ON s.staff_id = v.staff_id
    JOIN Services ser ON v.service_id = ser.id
    WHERE v.visit_date >= '2024-01-01'
)

SELECT 
    staff_name,
    specialization,
    SUM(revenue) AS total_revenue,
    ROUND(SUM(net_profit), 2) AS total_net_profit,
    -- Средний чек мастера относительно его коллег по той же специализации
    ROUND(AVG(revenue) OVER(PARTITION BY specialization), 2) AS avg_specialization_check,
    -- Ранжирование мастеров по прибыли внутри их категории
    DENSE_RANK() OVER(PARTITION BY specialization ORDER BY SUM(net_profit) DESC) AS rank_in_category
FROM StaffPerformance
GROUP BY staff_id, staff_name, specialization
ORDER BY total_net_profit DESC;
