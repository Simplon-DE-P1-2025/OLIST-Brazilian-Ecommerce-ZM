WITH first_orders AS (
    SELECT 
        c.customer_unique_id,
        MIN(strftime('%Y-%m', o.order_purchase_timestamp)) as cohort_month
    FROM orders o
    JOIN customers c ON o.customer_id = c.customer_id
    WHERE o.order_status = 'delivered'
    GROUP BY 1
),
activities AS (
    SELECT 
        fo.cohort_month,
        strftime('%Y-%m', o.order_purchase_timestamp) as activity_month,
        fo.customer_unique_id
    FROM orders o
    JOIN customers c ON o.customer_id = c.customer_id
    JOIN first_orders fo ON c.customer_unique_id = fo.customer_unique_id
    WHERE o.order_status = 'delivered'
),
cohort_size AS (
    SELECT cohort_month, COUNT(DISTINCT customer_unique_id) as num_users
    FROM first_orders
    GROUP BY 1
),
retention_data AS (
    SELECT 
        a.cohort_month,
        -- Correction ici : Utilisation de substr() pour extraire l'annee et le mois
        (CAST(substr(a.activity_month, 1, 4) AS INTEGER) - CAST(substr(a.cohort_month, 1, 4) AS INTEGER)) * 12 + 
        (CAST(substr(a.activity_month, 6, 2) AS INTEGER) - CAST(substr(a.cohort_month, 6, 2) AS INTEGER)) as month_number,
        COUNT(DISTINCT a.customer_unique_id) as num_active_users
    FROM activities a
    GROUP BY 1, 2
)
SELECT 
    r.cohort_month,
    s.num_users as cohort_size,
    r.month_number,
    r.num_active_users,
    ROUND(CAST(r.num_active_users AS FLOAT) / s.num_users * 100, 2) as retention_rate
FROM retention_data r
JOIN cohort_size s ON r.cohort_month = s.cohort_month
WHERE r.month_number >= 0
ORDER BY 1, 3;