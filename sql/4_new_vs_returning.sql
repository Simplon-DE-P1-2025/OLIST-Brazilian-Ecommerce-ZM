WITH orders_with_rank AS (
    SELECT 
        o.order_id,
        c.customer_unique_id,
        o.order_purchase_timestamp,
        RANK() OVER (PARTITION BY c.customer_unique_id ORDER BY o.order_purchase_timestamp) as order_rank
    FROM orders o
    JOIN customers c ON o.customer_id = c.customer_id
    WHERE o.order_status = 'delivered'
)
SELECT 
    strftime('%Y-%m', order_purchase_timestamp) as month,
    CASE 
        WHEN order_rank = 1 THEN 'Nouveau' 
        ELSE 'Récurrent' 
    END as customer_type,
    COUNT(DISTINCT order_id) as total_orders
FROM orders_with_rank
GROUP BY 1, 2
ORDER BY 1;