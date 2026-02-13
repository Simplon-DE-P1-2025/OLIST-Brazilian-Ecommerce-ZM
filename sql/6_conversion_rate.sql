/* Objectif : Taux de Conversion Transactionnel (Approbation des commandes)
   Note : Sans données de trafic web, on analyse le tunnel Commande -> Paiement -> Livraison.
*/
SELECT 
    strftime('%Y-%m', order_purchase_timestamp) as month,
    COUNT(order_id) as total_orders,
    COUNT(order_approved_at) as approved_orders,
    COUNT(CASE WHEN order_status = 'delivered' THEN 1 END) as delivered_orders,
    -- Taux d'approbation (Commandes payées / Commandes totales)
    ROUND(CAST(COUNT(order_approved_at) AS FLOAT) / COUNT(order_id) * 100, 2) as approval_rate,
    -- Taux de livraison (Commandes livrées / Commandes totales)
    ROUND(CAST(COUNT(CASE WHEN order_status = 'delivered' THEN 1 END) AS FLOAT) / COUNT(order_id) * 100, 2) as delivery_rate
FROM orders
GROUP BY 1
ORDER BY 1;