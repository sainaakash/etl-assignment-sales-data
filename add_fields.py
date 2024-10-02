from datetime import datetime

def add_fields(df, updater_username):
    df['UPDATED_DATE'] = datetime.now().strftime('%Y-%m-%d')
    df['UPDATED_BY'] = updater_username
    return df
