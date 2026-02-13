/* Objectif : Calculer R, F, M pour chaque client unique
   Reference Date : La date maximale du dataset + 1 jour
*/
WITH max_date_dataset AS (
    SELECT DATE(MAX(order_purchase_timestamp), '+1 day') as ref_date
    FROM orders
),
customer_stats AS (
    SELECT 
        c.customer_unique_id,
        MAX(o.order_purchase_timestamp) as last_order_date,
        COUNT(DISTINCT o.order_id) as frequency,
        SUM(oi.price) as monetary
    FROM orders o
    JOIN order_items oi ON o.order_id = oi.order_id
    JOIN customers c ON o.customer_id = c.customer_id
    WHERE o.order_status = 'delivered'
    GROUP BY 1
)
SELECT 
    cs.customer_unique_id,
    
    CAST(julianday((SELECT ref_date FROM max_date_dataset)) - julianday(cs.last_order_date) AS INTEGER) as recency,
    cs.frequency,
    cs.monetary
FROM customer_stats cs;