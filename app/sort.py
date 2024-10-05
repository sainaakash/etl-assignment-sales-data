import pandas as pd
import logging
import os

# function to sort the data on STATE, CITY, and ORDER_NO fields
def sort_data(df):
    try:
        #check if the DataFrame is None
        if df is None:
            raise ValueError("The DataFrame is None. Please provide a valid DataFrame.")

        # Check if the DataFrame is empty
        if df.empty:
            raise ValueError("The DataFrame is empty. Please provide a DataFrame with data.")

        # Sort the DataFrame based on STATE, CITY, and ORDER_NO fields in ascending order
        df.sort_values(by=['STATE', 'CITY', 'ORDERNUMBER'], inplace=True) 
        
        return df

    except KeyError as e:
        error_message = f"KeyError: One or more columns are missing: {e}"
        logging.error(error_message)
        raise

    except Exception as e:
        error_message = f"An error occurred during sorting: {e}"
        logging.error(error_message)
        raise
