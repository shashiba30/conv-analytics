import pandas as pd 

# Generate a Date Dimension Table
def generate_date_dimension(start_date, end_date):
    dates = pd.date_range(start_date, end_date, freq='D')
    date_dim = pd.DataFrame(dates, columns=['Date'])
    
    # Extract additional date-related features
    date_dim['DayOfWeek'] = date_dim['Date'].dt.day_name()
    date_dim['Month'] = date_dim['Date'].dt.month_name()
    date_dim['Quarter'] = date_dim['Date'].dt.to_period('Q')
    date_dim['Year'] = date_dim['Date'].dt.year
    date_dim['WeekOfYear'] = date_dim['Date'].dt.isocalendar().week
    date_dim['DayOfMonth'] = date_dim['Date'].dt.day
    
    date_dim['DateKey'] = date_dim['Date'].dt.strftime('%Y%m%d')
    
    return date_dim[['DateKey', 'Date', 'DayOfWeek', 'Month', 'Quarter', 'Year', 'WeekOfYear', 'DayOfMonth']]

# Generate Date Table from Jan 2024 to Dec 2024
df = pd.read_excel('sdv/online+retail/Online Retail.xlsx')
df['InvoiceDate'] = df['InvoiceDate'].apply(lambda x: x.replace(year = x.year + 13))
print(df.head())

print(min(df['InvoiceDate']),max(df['InvoiceDate']))
# date_dimension = generate_date_dimension('2024-01-01', '2024-12-31')
date_dimension = generate_date_dimension(min(df['InvoiceDate']),max(df['InvoiceDate']))
date_dimension.head()
date_dimension.to_csv('data/date_dimension.csv',index=False)


