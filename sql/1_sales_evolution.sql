/* Objectif : CA Mensuel et Évolution vs M-1 (Month over Month)*/

WITH monthly_sales AS (
    -- 1. Agrégation des ventes par mois
    SELECT 
        strftime('%Y-%m', o.order_purchase_timestamp) as sales_month,
        SUM(oi.price) as monthly_revenue,
        COUNT(DISTINCT o.order_id) as total_orders
    FROM orders o
    JOIN order_items oi ON o.order_id = oi.order_id
    WHERE o.order_status = 'delivered'
    GROUP BY 1
),
sales_growth AS (
    -- 2. Calcul de la variation avec LAG (Window Function)
    SELECT 
        sales_month,
        monthly_revenue,
        LAG(monthly_revenue) OVER (ORDER BY sales_month) as prev_month_revenue,
        total_orders
    FROM monthly_sales
)
-- 3. Calcul final du % d'évolution
SELECT 
    sales_month,
    monthly_revenue,
    prev_month_revenue,
    ROUND((monthly_revenue - prev_month_revenue) / prev_month_revenue * 100, 2) as growth_percent
FROM sales_growth
ORDER BY sales_month;