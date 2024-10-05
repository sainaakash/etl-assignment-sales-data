import os
import pandas as pd
import logging
from app.validate import validate_data
from app.sort import sort_data
from app.add_fields import add_fields
from app.output import format_order_date, format_sales, output_to_csv, output_to_db

if not os.path.exists('log'):
    os.makedirs('log')

# Configure logging
logging.basicConfig(
    filename='log/main.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def main():
    # File paths
    file_path = './input/sales_data_sample.csv'  # Change to the correct path of the input CSV
    output_dir = './output'  # Directory to save the output files
    high_sales_path = os.path.join(output_dir, 'high_sales.csv')
    low_sales_path = os.path.join(output_dir, 'low_sales.csv')
    db_path = os.path.join(output_dir, 'sales_data.db')

    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    # Load the data
    try:
        data = pd.read_csv(file_path, encoding='ISO 8859-1')
        logging.info("CSV file read successfully.")
    except FileNotFoundError as e:
        logging.error(f"File not found: {e}")
        return
    except pd.errors.EmptyDataError as e:
        logging.error(f"No data: {e}")
        return
    except Exception as e:
        logging.error(f"An error occurred while reading the CSV file: {e}")
        return

    try:
        # Define the updater username
        updater_username = 'admin_user'  # Replace with the actual username

        # Validate data
        if validate_data(data):
            try:
                # add UPDATE_DATE and UPDATED_BY fields
                data = add_fields(data, updater_username)
                logging.info("Fields UPDATE_DATE and UPDATED_BY added.")
            except Exception as e:
                logging.error(f"An error occurred while adding fields: {e}")
                return

            try:
                # Sorting the data
                data = sort_data(data)
                logging.info("Data sorted successfully on the columns: STATE, CITY, ORDERNUMBER")
            except Exception as e:
                logging.error(f"An error occurred while sorting the data: {e}")

            try:
                # Formatting ORDERDATE and SALES
                data = format_order_date(data)
                data = format_sales(data)
                logging.info("Data formatting completed")
            except Exception as e:
                logging.error(f"An error occurred while formatting the data: {e}")
                return

            try:
                # Output to CSV
                output_to_csv(data, high_sales_path, low_sales_path)
                logging.info(f"Data output to CSV: {high_sales_path}, {low_sales_path}")
            except Exception as e:
                logging.error(f"An error occurred while formatting the data: {e}")
                return

            try:
                # Write to SQLite database
                output_to_db(data, db_path)
                logging.info(f"Data written to database at {db_path}")
            except Exception as e:
                logging.error(f"An error occurred while formatting the data: {e}")
                return

            print("Data processing complete. Files and database updated.")
        else:
            logging.error("Data Validation failed.")
    except Exception as e:
        logging.error(f"An error occurred during data processing: {e}")

if __name__ == "__main__":
    main()
