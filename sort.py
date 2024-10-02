def sort_data(df):
    return df.sort_values(by=['STATE', 'CITY', 'ORDERNUMBER'])
