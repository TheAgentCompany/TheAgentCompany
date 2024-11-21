FROM base-image

RUN apt-get update && \
    apt-get install -y sqlite3 && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN mkdir -p /data
RUN sqlite3 /data/coffee_shop.db

COPY eval_data/customers.csv /data
COPY eval_data/inventory.csv /data
COPY eval_data/order_items.csv /data
COPY eval_data/orders.csv /data
COPY eval_data/products.csv /data
COPY eval_data/average_sales.csv /utils
COPY eval_data/short_stock.csv /utils
COPY analysis.txt /workspace


RUN pip install pandas