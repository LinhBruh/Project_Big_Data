CREATE INDEX idx_customers_customer_name on dim_customers(customer_name);

CREATE INDEX idx_products_product_name on dim_products(product_name);
CREATE INDEX idx_products_product_rating on dim_products(rating);
CREATE INDEX idx_products_product_quatity on dim_products(quantity);
CREATE INDEX idx_products_product_price on dim_products(price);
CREATE INDEX idx_products_product_brand on dim_products(brand);

CREATE INDEX idx_orders_order_quantity on fact_orders(quantity);
CREATE INDEX idx_orders_order_total_price on fact_orders(total_price);

