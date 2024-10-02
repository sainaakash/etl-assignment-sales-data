import os
import pandas as pd
from validate import validate_data
from sort import sort_data
from add_fields import add_fields
from output import format_order_date, format_sales, output_to_csv, output_to_db

def main():
    # File paths
    file_path = 'sales_data_sample.csv'  # Change to the correct path of the input CSV
    output_dir = './output'  # Directory to save the output files
    high_sales_path = os.path.join(output_dir, 'high_sales.csv')
    low_sales_path = os.path.join(output_dir, 'low_sales.csv')
    db_path = os.path.join(output_dir, 'sales_data.db')

    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Load the data
    data = pd.read_csv(file_path, encoding='ISO 8859-1')
    
    # Define the updater username
    updater_username = 'admin_user'  # Replace with the actual username
    
    # Validate data
    data = validate_data(data)
    
    # Add additional fields
    data = add_fields(data, updater_username)
    
    # Sorting the data
    data = sort_data(data)
    
    # Formatting ORDERDATE and SALES
    data = format_order_date(data)
    data = format_sales(data)
    
    # Output to CSV
    output_to_csv(data, high_sales_path, low_sales_path)
    
    # Write to SQLite database
    output_to_db(data, db_path)
    
    print("Data processing complete. Files and database updated.")

if __name__ == "__main__":
    main()
