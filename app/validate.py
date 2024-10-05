import pandas as pd
from datetime import datetime
import re
import logging
import os

def validate_data(df):
    errors = []
    null_columns = {}

    try:
        #check for missing or empty fields
        for c in df.columns:
            null_count = df[c].isnull().sum()
            if null_count > 0:
                null_columns[c] = null_count
        if null_columns:
            #convert null_columns values to native python integers
            null_columns_numeric = {col: int(c) for col, c in null_columns.items()}
            error_message = f"There are missing or empty fields in the data: {null_columns_numeric}"
            errors.append(error_message)
            logging.error(error_message)

        #check if QUANTITYORDERED is a positive integer
        if not df['QUANTITYORDERED'].apply(lambda x: isinstance(x, int) and x > 0).all():
            error_message = "QUANTITYORDERED must be a positive integer."
            errors.append(error_message)
            logging.error(error_message)
    
        # Ensure ORDERDATE is less than today
        try:
            df['ORDERDATE'] = pd.to_datetime(df['ORDERDATE'], errors='coerce')
            today = datetime.today()
            if not df['ORDERDATE'].apply(lambda x: x < datetime.now()).all():
                error_message="ORDERDATE must be less than today."
                errors.append(error_message)
                logging.error(error_message)
        except ValueError as e:
            error_message = f"Data format error: {e}"
            errors.append(error_message)
            logging.error(error_message)

        
        # Standardize PHONE format
        if 'PHONE' in df.columns:  # Check if PHONE column exists
            try:
                df['PHONE'] = df['PHONE'].apply(standardize_phone)
                # Optional: Validate phone number length after standardization
                if not df['PHONE'].str.len().eq(12).all():  # Check for 12 characters (3-digit area code, hyphen, 7-digit number)
                    raise ValueError("PHONE number length must be 12 characters after formatting (e.g., XXX-XXX-XXXX)")
            except Exception as e:
                error_message = f"Phone number formatting error: {e}"
                errors.append(error_message)
                logging.error(error_message)
    
        #handle errors if any
        if errors:
            #fill empty fields in STATE column with 'unknown'
            df['STATE'] = df['STATE'].fillna('Unknown')
            logging.info("Filled empty fields in STATE column with 'unknown'")

            #drop column with column fields
            if null_columns:
                columns_to_drop = [c for c in null_columns.keys() if c != 'STATE']
                if columns_to_drop:
                    df.drop(columns=columns_to_drop, inplace=True)
                    drop_message = f"Dropped columns with empty fields (excluding STATE): {columns_to_drop}"
                    logging.info(drop_message)

    except Exception as e:
        error_message = f"An error occured during validation: {e}"
        errors.append(error_message)
        logging.error(error_message)
    
    return True

def standardize_phone(phone):
    try:
        # Remove all non-numeric characters
        phone = re.sub(r'\D', '', phone)
        # Remove extra digits, keep the first 10 digits from the left
        phone = phone[:10]
        # If the number has less than 10 digits, pad with zeros on the left
        phone = phone.zfill(10)
        # Format the phone number
        formatted_phone = f"{phone[:3]}-{phone[3:6]}-{phone[6:]}"
        return formatted_phone
    except Exception as e:
        raise ValueError(f"Error in the phone formatting: {e}")
