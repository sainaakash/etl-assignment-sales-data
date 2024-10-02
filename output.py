import pandas as pd
import sqlite3

def format_order_date(df):
    df['ORDERDATE'] = df['ORDERDATE'].dt.strftime('%m-%d-%Y')
    return df

def format_sales(df):
    df['SALES'] = df['SALES'].apply(lambda x: f"${x:,.2f}")
    return df

def output_to_csv(df, high_sales_path, low_sales_path):
    high_sales = df[df['SALES'].apply(lambda x: float(x.replace('$', '').replace(',', '')) > 3000)]
    low_sales = df[df['SALES'].apply(lambda x: float(x.replace('$', '').replace(',', '')) <= 3000)]
    
    high_sales.to_csv(high_sales_path, index=False)
    low_sales.to_csv(low_sales_path, index=False)

def output_to_db(df, db_path):
    conn = sqlite3.connect(db_path)
    df.to_sql('sales_data', conn, if_exists='replace', index=False)
    conn.close()
