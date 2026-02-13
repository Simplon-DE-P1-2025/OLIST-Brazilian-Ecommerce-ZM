WITH first_orders AS (
    SELECT 
        c.customer_unique_id,
        MIN(strftime('%Y-%m', o.order_purchase_timestamp)) as cohort_month
    FROM orders o
    JOIN customers c ON o.customer_id = c.customer_id
    WHERE o.order_status = 'delivered'
    GROUP BY 1
),
cohort_size AS (
    SELECT 
        cohort_month, 
        COUNT(DISTINCT customer_unique_id) as num_customers
    FROM first_orders
    GROUP BY 1
),
order_revenues AS (
    SELECT 
        o.order_id,
        c.customer_unique_id,
        strftime('%Y-%m', o.order_purchase_timestamp) as activity_month,
        SUM(oi.price) as order_revenue
    FROM orders o
    JOIN order_items oi ON o.order_id = oi.order_id
    JOIN customers c ON o.customer_id = c.customer_id
    WHERE o.order_status = 'delivered'
    GROUP BY 1, 2, 3
),
activities AS (
    SELECT 
        fo.cohort_month,
        -- Correction ici : Utilisation de substr() pour extraire l'annee et le mois
        (CAST(substr(r.activity_month, 1, 4) AS INTEGER) - CAST(substr(fo.cohort_month, 1, 4) AS INTEGER)) * 12 + 
        (CAST(substr(r.activity_month, 6, 2) AS INTEGER) - CAST(substr(fo.cohort_month, 6, 2) AS INTEGER)) as month_number,
        r.order_revenue
    FROM order_revenues r
    JOIN first_orders fo ON r.customer_unique_id = fo.customer_unique_id
),
monthly_cohort_revenue AS (
    SELECT 
        cohort_month,
        month_number,
        SUM(order_revenue) as total_revenue
    FROM activities
    GROUP BY 1, 2
),
cumulative_cohort_revenue AS (
    SELECT 
        mcr.cohort_month,
        mcr.month_number,
        mcr.total_revenue,
        SUM(mcr.total_revenue) OVER (PARTITION BY mcr.cohort_month ORDER BY mcr.month_number) as cumulative_revenue
    FROM monthly_cohort_revenue mcr
)
SELECT 
    ccr.cohort_month,
    cs.num_customers as cohort_size,
    ccr.month_number,
    ccr.cumulative_revenue,
    ROUND(ccr.cumulative_revenue / cs.num_customers, 2) as cumulative_ltv_per_customer
FROM cumulative_cohort_revenue ccr
JOIN cohort_size cs ON ccr.cohort_month = cs.cohort_month
WHERE ccr.month_number >= 0
ORDER BY 1, 3;