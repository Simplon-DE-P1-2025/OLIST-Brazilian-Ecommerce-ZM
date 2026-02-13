/* 
   Calcul : Somme des ventes / Nombre de commandes uniques
*/
SELECT 
    strftime('%Y-%m', o.order_purchase_timestamp) as month,
    SUM(oi.price) as total_revenue,
    COUNT(DISTINCT o.order_id) as total_orders,
    -- Le calcul du panier moyen
    ROUND(SUM(oi.price) / COUNT(DISTINCT o.order_id), 2) as average_ticket
FROM orders o
JOIN order_items oi ON o.order_id = oi.order_id
WHERE o.order_status = 'delivered'
GROUP BY 1
ORDER BY 1;