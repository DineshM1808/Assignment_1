import streamlit as st
import mysql.connector
import pandas as pd


# Database Connection
def get_connection():
    return mysql.connector.connect(
        host="gateway01.ap-southeast-1.prod.aws.tidbcloud.com",
        port=4000,
        user="emKpcWuiv3AJdP2.root",
        password="j6dK5WPpxaoY3gov",
        database="project1"
    )

# Function to execute SQL queries
def execute_query(query):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(query)
    result = cursor.fetchall()
    columns = [desc[0] for desc in cursor.description]
    conn.close()
    return pd.DataFrame(result, columns=columns)


# Streamlit UI
st.title(" Retail Order Data Analysis ")

# Section 1: Retail Order Queries
st.header("Retail Order Queries")
retail_queries = {
    "1. Top 10 Highest Revenue Generating Products": """
        SELECT product_id, SUM(sale_price) AS sale 
        FROM project1.retailorders 
        GROUP BY product_id 
        ORDER BY sale DESC 
        LIMIT 10;
    """,
    "2. Top 5 Cities with Highest Profit Margins": """
        SELECT city AS cities, SUM(profit) AS profit_margins 
        FROM project1.retailorders 
        GROUP BY city 
        ORDER BY profit_margins DESC 
        LIMIT 5;
    """,
    "3. Total Discount Given for Each Category": """
        SELECT category, SUM(discount) AS total_discount 
        FROM project1.retailorders 
        GROUP BY category;
    """,
    "4. Average Sale Price Per Product Category": """
        SELECT category AS product_category, AVG(sale_price) AS avg_sale_price 
        FROM project1.retailorders 
        GROUP BY category;
    """,
    "5. Region with Highest Average Sale Price": """
        SELECT region, AVG(sale_price) AS avg_sale_price 
        FROM project1.retailorders 
        GROUP BY region 
        ORDER BY avg_sale_price DESC 
        LIMIT 1;
    """,
    "6. Total Profit Per Category": """
        SELECT category, SUM(profit) AS total_profit 
        FROM project1.retailorders 
        GROUP BY category;
    """,
    "7. Top 3 Segments with Highest Order Quantity": """
        SELECT segment, SUM(quantity) AS total_quantity 
        FROM project1.retailorders 
        GROUP BY segment 
        ORDER BY total_quantity DESC 
        LIMIT 3;
    """,
    "8. Average Discount Percentage Per Region": """
        SELECT region, AVG(discount_percent) AS avg_discount 
        FROM project1.retailorders 
        GROUP BY region;
    """,
    "9. Product Category with Highest Total Profit": """
        SELECT sub_category, SUM(profit) AS total_profit 
        FROM project1.retailorders 
        GROUP BY sub_category 
        ORDER BY total_profit DESC 
        LIMIT 1;
    """,
    "10. Total Revenue Generated Per Year": """
        SELECT YEAR(order_date) AS year, SUM(sale_price) AS total_revenue 
        FROM project1.retailorders 
        GROUP BY year;
    """
}

selected_retail_query = st.selectbox("Select a Retail Order Query", list(retail_queries.keys()))
if st.button("Run Retail order Query"):
    query = retail_queries[selected_retail_query]
    df = execute_query(query)
    st.dataframe(df)

# Section 2: Retail Orders Using JOIN Queries
st.header("Retail Orders Using JOIN Queries")
join_queries = {
    "1. Inner Join - Order Details": """
        SELECT o1.order_id, o1.order_date, o2.product_id, o2.quantity 
        FROM orders1 o1 
        INNER JOIN orders2 o2 ON o1.order_id = o2.order_id;
    """,
    "2. Left Join - All Orders": """
        SELECT o1.order_id, o1.order_date, o1.segment, o2.sub_category, o2.quantity 
        FROM orders1 o1 
        LEFT JOIN orders2 o2 ON o1.order_id = o2.order_id;
    """,
    "3. Right Join - All Products": """
        SELECT o1.order_id, o1.ship_mode, o1.state, o2.product_id, o2.quantity, o2.sale_price, o2.profit
        FROM orders1 o1 
        RIGHT JOIN orders2 o2 ON o1.order_id = o2.order_id;
    """,
    "4. Filtering Join - High Profit US Orders": """
        SELECT o1.order_date, o1.order_id, o1.region
        FROM orders1 o1 
        RIGHT JOIN orders2 o2 ON o1.order_id = o2.order_id
        WHERE o2.profit > 500 AND o1.country = 'United States';
    """,
    "5. Aggregation - Total Sales & Profit Per Region": """
        SELECT SUM(o2.sale_price) AS total_sales, SUM(o2.profit) AS total_profit, o1.region
        FROM orders1 o1 
        INNER JOIN orders2 o2 ON o1.order_id = o2.order_id 
        GROUP BY o1.region 
        ORDER BY total_sales DESC;
    """,
    "6. Top 5 Cities by Revenue": """
        SELECT o1.city, SUM(o2.sale_price) AS total_revenue
        FROM orders1 o1
        INNER JOIN orders2 o2 ON o1.order_id = o2.order_id
        GROUP BY o1.city
        ORDER BY total_revenue DESC
        LIMIT 5;
    """,
    "7. Average Discount Per Category": """
        SELECT AVG(o2.discount_percent) AS avg_discount, o1.category 
        FROM orders1 o1 
        INNER JOIN orders2 o2 ON o1.order_id = o2.order_id 
        GROUP BY o1.category 
        ORDER BY avg_discount DESC;
    """,
    "8. Unique Products Sold Per Category": """
        SELECT o1.category, COUNT(DISTINCT o2.product_id) AS unique_products
        FROM orders1 o1 
        INNER JOIN orders2 o2 ON o1.order_id = o2.order_id
        GROUP BY o1.category
        ORDER BY unique_products;
    """,
    "9. High Discount Orders": """
        SELECT o2.order_id, o2.product_id, o2.sale_price, o2.profit 
        FROM orders2 o2
        WHERE o2.discount_percent > 4;
    """,
    "10. Consumer Segment Products": """
        SELECT o2.product_id, o2.sale_price, o2.profit
        FROM orders1 o1
        JOIN orders2 o2 ON o1.order_id = o2.order_id
        WHERE o1.segment = 'Consumer'
        ORDER BY sale_price DESC
        LIMIT 10;
    """
}

selected_join_query = st.selectbox("Select a JOIN Query", list(join_queries.keys()))
if st.button("Run JOIN Query"):
    query = join_queries[selected_join_query]
    df = execute_query(query)
    st.dataframe(df)
