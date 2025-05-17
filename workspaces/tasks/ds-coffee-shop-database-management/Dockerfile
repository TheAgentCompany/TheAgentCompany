FROM ghcr.io/li-boxuan/task-base-image:1.0.0

RUN apt-get update && \
    apt-get install -y sqlite3 && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN mkdir -p /data
RUN sqlite3 /data/coffee_shop.db

COPY eval_data/customers.csv /utils
COPY eval_data/inventory.csv /utils
COPY eval_data/order_items.csv /utils
COPY eval_data/orders.csv /utils
COPY eval_data/products.csv /utils
COPY eval_data/average_sales.csv /utils
COPY eval_data/short_stock.csv /utils


RUN pip install pandas