CREATE TABLE dim_customers(
	customer_key SERIAL PRIMARY KEY,
	customer_id VARCHAR(50) NOT NULL,
	customer_name VARCHAR(200) NOT NULL,
	sex VARCHAR(10) NOT NULL,
	phone_number VARCHAR(30) NOT NULL,
	email VARCHAR(50) NOT NULL,
	city VARCHAR(30) NOT NULL,
	create_at DATE NOT NULL,
	end_date DATE DEFAULT NOW()
);

CREATE TABLE dim_products(
	product_key SERIAL PRIMARY KEY,
	product_id VARCHAR(50) NOT NULL,
	product_name VARCHAR(100) NOT NULL,
	rating DECIMAL(4,2) NOT NULL,
	quantity INT NOT NULL,
	price DECIMAL(10,2) NOT NULL,
	brand VARCHAR(50) NOT NULL,
	create_at DATE NOT NULL,
	end_date DATE DEFAULT NOW()
);

CREATE TABLE dim_categories(
	category_key SERIAL PRIMARY KEY,
	category_name  VARCHAR(50) NOT NULL UNIQUE,
	create_at DATE NOT NULL,
	end_date DATE DEFAULT NOW()
);

CREATE TABLE dim_date(
	date_key INT PRIMARY KEY,
	full_date DATE NOT NULL UNIQUE,
	day_of_week INT NOT NULL,
	day_name VARCHAR(10) NOT NULL,
	day_of_month  INT  NOT NULL,
	day_of_year INT NOT NULL,
	week_of_year INT NOT NULL,
	month_number INT NOT NULL,
	month_name VARCHAR(10) NOT NULL,
	quarter_number INT NOT NULL,
	quarter_name VARCHAR(6) NOT NULL,
	year INT NOT NULL,
	is_weekend BOOLEAN NOT NULL,
	is_holiday BOOLEAN NOT NULL DEFAULT FALSE,
	holiday_name VARCHAR(50)
);

CREATE TABLE fact_orders(
	order_key BIGSERIAL PRIMARY KEY,
	order_id VARCHAR(50) NOT NULL,
	customer_key INT NOT NULL,
	product_key INT NOT NULL,
	category_key INT NOT NULL,
	date_key INT NOT NULL,
	quantity INT NOT NULL,
	total_price DECIMAL(15,2) NOT NULL,
	method VARCHAR(20) NOT NULL,
	payment_method VARCHAR(20) NOT NULL,
	status VARCHAR(20) NOT NULL,
	create_at DATE DEFAULT NOW(),
	end_date DATE DEFAULT NOW()
);

ALTER TABLE fact_orders
ADD FOREIGN KEY (customer_key) REFERENCES dim_customers(customer_key),
ADD FOREIGN KEY (product_key) REFERENCES dim_products(product_key),
ADD FOREIGN KEY (category_key) REFERENCES dim_categories(category_key),
ADD FOREIGN KEY (date_key) REFERENCES dim_date(date_key);

	
	