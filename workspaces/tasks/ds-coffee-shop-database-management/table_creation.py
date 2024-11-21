import pandas as pd
import sqlite3
import os

def pandas_to_sqlite(csv_file, db_file, table_name=None, index=False):
    """
    Import CSV to pandas and save as SQLite table

    Args:
        csv_file (str): Path to CSV file
        db_file (str): Path to SQLite database
        table_name (str): Name for the table (default: CSV filename without extension)
        index (bool): Whether to include the DataFrame index as a column
    """
    # Read CSV into pandas
    df = pd.read_csv(csv_file)

    # If table_name not provided, use CSV filename
    if table_name is None:
        table_name = csv_file.split('.')[0]

    # Create SQLite connection
    conn = sqlite3.connect(db_file)

    # Write DataFrame to SQLite
    df.to_sql(table_name, conn, if_exists='replace', index=index)

    # Close connection
    conn.close()

    print(f"Created table '{table_name}' with {len(df)} rows")
    return df


# Example usage
if __name__ == "__main__":
    # Example with basic usage
    for file in os.listdir('/data'):
        if '.csv' in file:
            pandas_to_sqlite(os.path.join('/data',file),'/data/coffee_shop.db',file.split('.')[0])
"""
create view v_short_stock as select product_id, quantity_in_stock, reorder_point from inventory where quantity_in_stock<=reorder_point;
"""

"""
create view v_sales as select * from (with rev as (select p.product_id as product_id, sum(oi.quantity) as quantity, sum(quantity*p.unit_price) as revenue_generated, sum(quantity*p.unit_price) - sum(quantity*p.unit_cost) as profit_generated from orders o,order_items oi, products p where o.order_id = oi.order_id and oi.product_id = p.product_id group by p.product_id),
dates  as (select julianday(max(order_date)) - julianday(min(order_date))+1 as days from orders) select product_id, round(quantity/days,2) as average_sales, revenue_generated, profit_generated from rev,dates);
"""