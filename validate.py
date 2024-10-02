import pandas as pd
from datetime import datetime
import re

def validate_data(df):
    # Fields that are required and must be non-empty
    required_fields = ['ORDERNUMBER', 'QUANTITYORDERED', 'PRICEEACH', 'ORDERDATE', 'STATUS', 'QTR_ID', 'MONTH_ID', 'YEAR_ID', 'PRODUCTLINE', 'MSRP', 'PRODUCTCODE', 'CUSTOMERNAME', 'PHONE', 'ADDRESSLINE1', 'CITY', 'COUNTRY', 'CONTACTLASTNAME', 'CONTACTFIRSTNAME', 'DEALSIZE', 'SALES']
    
    # Fields that are optional
    optional_fields = ['ADDRESSLINE2', 'POSTALCODE', 'TERRITORY', 'STATE']
    
    # Ensure required fields are present and non-empty
    for field in required_fields:
        if field not in df.columns or df[field].isnull().any():
            raise ValueError(f"Missing or empty field: {field}")
    
    # Ensure optional fields are present (can be empty)
    for field in optional_fields:
        if field not in df.columns:
            raise ValueError(f"Missing field: {field}")
    
    # Ensure QUANTITYORDERED is a positive integer
    if not df['QUANTITYORDERED'].apply(lambda x: isinstance(x, int) and x > 0).all():
        raise ValueError("QUANTITYORDERED must be a positive integer")
    
    # Ensure ORDERDATE is less than today
    df['ORDERDATE'] = pd.to_datetime(df['ORDERDATE'], errors='coerce')
    if not df['ORDERDATE'].apply(lambda x: x < datetime.now()).all():
        raise ValueError("ORDERDATE must be less than today")
    
    # Standardize PHONE format
    if 'PHONE' in df.columns:  # Check if PHONE column exists
        df['PHONE'] = df['PHONE'].apply(standardize_phone)
        # Optional: Validate phone number length after standardization
        if not df['PHONE'].str.len().eq(12).all():  # Check for 12 characters (3-digit area code, hyphen, 7-digit number)
            raise ValueError("PHONE number length must be 12 characters after formatting (e.g., XXX-XXX-XXXX)")

    # Fill null values in the "STATE" column with "in"
    df['STATE'] = df['STATE'].fillna('Unknown')
    
    return df

def standardize_phone(phone):
    # Remove all non-numeric characters
    phone = re.sub(r'\D', '', phone)
    # Remove extra digits, keep the first 10 digits from the left
    phone = phone[:10]
    # If the number has less than 10 digits, pad with zeros on the left
    phone = phone.zfill(10)
    # Format the phone number
    formatted_phone = f"{phone[:3]}-{phone[3:6]}-{phone[6:]}"
    return formatted_phone

