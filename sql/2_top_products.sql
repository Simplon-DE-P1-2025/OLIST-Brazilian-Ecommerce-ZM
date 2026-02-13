/* Objectif : Top 10 Produits par CA Global
*/
SELECT 
    p.product_category_name_english,
    COUNT(DISTINCT oi.order_id) as num_sales,
    SUM(oi.price) as total_revenue,
    RANK() OVER (ORDER BY SUM(oi.price) DESC) as rank
FROM order_items oi
JOIN products p ON oi.product_id = p.product_id
JOIN orders o ON oi.order_id = o.order_id
WHERE o.order_status = 'delivered'
GROUP BY p.product_category_name_english
LIMIT 10;