/* 
   Problème : Sous-requête corrélée exécutée pour chaque ligne + Pas de filtre précoce
*/

SELECT 
    strftime('%Y-%m', o.order_purchase_timestamp) as sales_month,
    SUM(oi.price) as monthly_revenue,
    (
        SELECT SUM(oi2.price) 
        FROM order_items oi2 
        JOIN orders o2 ON oi2.order_id = o2.order_id
        WHERE strftime('%Y-%m', o2.order_purchase_timestamp) = 
              strftime('%Y-%m', date(o.order_purchase_timestamp, '-1 month'))
    ) as prev_month_revenue
FROM orders o
JOIN order_items oi ON o.order_id = oi.order_id
GROUP BY 1
ORDER BY 1;