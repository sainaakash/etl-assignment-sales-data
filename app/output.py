import pandas as pd
import sqlite3
import logging
import os

# Function to format the ORDERDATE column in the dataframe
def format_order_date(df):
    try:
        df['ORDERDATE'] = df['ORDERDATE'].dt.strftime('%m-%d-%Y')
        
        return df
    except Exception as e:
        error_message = f"An error occurred while formatting ORDERDATE: {e}" 
        logging.error(error_message)
        raise

# function to format the SALES column in the dataframe
def format_sales(df):
    try:
        df['SALES'] = df['SALES'].apply(lambda x: f"${x:,.2f}")
        
        return df
    except Exception as e:
        error_message = f"An error occurred while formatting SALES: {e}" 
        logging.error(error_message)
        raise

# Function to output the dataframe to CSV files based on SALES value
def output_to_csv(df, high_sales_path, low_sales_path):
    try:
        #filter rows with SALES greater than $3000
        high_sales = df[df['SALES'].apply(lambda x: float(x.replace('$', '').replace(',', '')) > 3000)]
    
        #filter rows with SALES less than or equal to $3000
        low_sales = df[df['SALES'].apply(lambda x: float(x.replace('$', '').replace(',', '')) <= 3000)]
    
        #Output high sales data to CSV
        high_sales.to_csv(high_sales_path, index=False)
        
        #Output low sales data to CSV
        low_sales.to_csv(low_sales_path, index=False)
        
    except Exception as e:
        error_message - f"An error occurred while outputting to CSV: {e}"
        logging.error(error_message)
        raise

#function to output the dataframe to a SQLite database
def output_to_db(df, db_path):
    try:
        #connect to SQLite database
        conn = sqlite3.connect(db_path)

        # Write the dataframe to the database table 'sales_data'
        df.to_sql('sales_data', conn, if_exists='replace', index=False)
        
        # Close the database connection
        conn.close()
        

    except Exception as e:
        error_message = f"An error occurred while outputting to the database: {e}"
        logging.error(error_message)    
        raise
