from datetime import datetime
import pandas as pd
import logging
import os

# function to add UPDATE_DATE and UPDATED_BY fields
def add_fields(df, updater_username):
    try:
        #check if the DataFrame is None
        if df is None:
            raise ValueError("The DataFrame is None. Please provide a valid DataFrame.")

        # Check if the DataFrame is empty
        if df.empty:
            raise ValueError("The DataFrame is empty. Please provide a DataFrame with data.")

        #Add UPDATE_DATE field with the current date
        try:
            df['UPDATED_DATE'] = datetime.now()
            
        except Exception as e:
            error_message = f"An error occurred while adding UPDATED_DATE: {e}"
            logging.error(error_message)
            raise

        # Add UPDATED_BY field with the username of the updater
        try:
            df['UPDATED_BY'] = updater_username
            
        except Exception as e:
            error_message = f"An error occurred while adding UPDATED_BY: {e}"
            logging.error(error_message)
            raise

        return df

    except Exception as e:
        error_message = f"An error occurred in add_fields function: {e}"
        logging.error(error_message)
        raise
