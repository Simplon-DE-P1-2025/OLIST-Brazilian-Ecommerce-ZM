/* Objectif : CA Quotidien (Granularité la plus fine)
   On pourra ensuite agréger par Mois/Année dans Python.
*/
SELECT 
    date(o.order_purchase_timestamp) as sale_date,
    SUM(oi.price) as daily_revenue,
    COUNT(DISTINCT o.order_id) as order_count
FROM orders o
JOIN order_items oi ON o.order_id = oi.order_id
WHERE o.order_status = 'delivered'
GROUP BY 1
ORDER BY 1;