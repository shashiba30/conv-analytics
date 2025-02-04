from clickhouse_driver import Client
import pandas as pd

Client = Client('localhost')


## customer dimension
customer_df = pd.read_csv('dataset/data/customer_dimension.csv')
customer_df.head()
Client.execute('CREATE DATABASE IF NOT EXISTS hackathon')
Client.execute('USE hackathon')
Client.execute('DROP TABLE IF EXISTS hackathon.customer_dimension')
Client.execute(
    '''
    CREATE TABLE hackathon.customer_dimension
    (
        CustomerKey UInt32,
        CustomerID Int32,
        CustomerName String,
        CustomerAge Int32,
        CustomerGender String,
        Country String
    ) 
    ENGINE = MergeTree()
    ORDER BY CustomerKey
    '''
)
cust_prg = Client.execute('INSERT INTO hackathon.customer_dimension VALUES', customer_df.to_dict('records'))
print(cust_prg)

## date dimension
date_df = pd.read_csv('dataset/data/date_dimension.csv')
# date_df['DateKey'] = pd.to_datetime(date_df['DateKey'], format='%Y-%m-%d')
date_df['Date'] = pd.to_datetime(date_df['Date'], format='%Y-%m-%d %H:%M:%S')
date_df['DateKey'] = date_df['DateKey'].astype(int)

date_df.head()
Client.execute('DROP TABLE IF EXISTS hackathon.date_dimension')
Client.execute(
    '''
       CREATE TABLE hackathon.date_dimension
        (
            DateKey UInt32,                     -- A unique identifier for each date
            Date DateTime,      -- The full datetime of the day
            DayOfWeek String,                   -- The day of the week (e.g., Monday, Tuesday)
            Month String,                       -- The month (e.g., January, February)
            Quarter String,                     -- The quarter (e.g., 2020Q1, 2020Q2)
            Year Int64,                         -- The year (e.g., 2020)
            WeekOfYear Int64,                   -- The week of the year (e.g., 1 to 52)
            DayOfMonth Int64                    -- The day of the month (e.g., 1 to 31)
        ) 
        ENGINE = MergeTree()
        ORDER BY DateKey;
    '''
)

date_prg = Client.execute('INSERT INTO hackathon.date_dimension VALUES', date_df.to_dict('records'))
print(date_prg)


### product dimension
product_df = pd.read_csv('dataset/data/product_dimension.csv')
product_df.fillna('Unknown', inplace=True)
Client.execute('DROP TABLE IF EXISTS hackathon.product_dimension')
Client.execute(
    '''
    CREATE TABLE IF NOT EXISTS hackathon.product_dimension
    (
        ProductKey UInt32,                     -- A unique identifier for each product
        StockCode String,                      -- The stock code (unique identifier for the product)
        Description String,                    -- The name or description of the product
        Category String,                       -- The category of the product
        Subcategory String,                    -- The subcategory of the product
        Cleaned_Description String            -- Cleaned description for processing
    ) 
    ENGINE = MergeTree()
    ORDER BY ProductKey
    '''
)
prod_prg = Client.execute('INSERT INTO hackathon.product_dimension VALUES', product_df.to_dict('records'))
print(prod_prg)

sales_fact = pd.read_excel('sdv/online+retail/Online Retail.xlsx')
print(sales_fact.head())
# sales_fact['Description'].fillna('Unknown', inplace=True)
# sales_fact['CustomerID'].fillna('00000', inplace=True)
# sales_fact.fillna('00000', inplace=True)
sales_fact['InvoiceNo'].fillna('Unknown', inplace=True)  # Fill NaN in 'InvoiceNo' with 'Unknown'
sales_fact['StockCode'].fillna('Unknown', inplace=True)  # Fill NaN in 'StockCode' with 'Unknown'
sales_fact['Quantity'].fillna(0, inplace=True)           # Fill NaN in 'Quantity' with 0
sales_fact['UnitPrice'].fillna(0.0, inplace=True)         # Fill NaN in 'UnitPrice' with 0.0
sales_fact['CustomerID'].fillna(-1, inplace=True)         # Fill NaN in 'CustomerID' with -1
sales_fact['Country'].fillna('Unknown', inplace=True)
# sales_fact['CustomerID'] = sales_fact['CustomerID'].astype(int)
# sales_fact['CustomerID'] = sales_fact['CustomerID'].astype('UInt32')  # Ensure CustomerID is unsigned integer

sales_fact['InvoiceDate'] = pd.to_datetime(sales_fact['InvoiceDate'], format='%Y-%m-%d %H:%M:%S')
sales_fact['InvoiceNo'] = sales_fact['InvoiceNo'].astype(str)  # Ensure InvoiceNo is string
sales_fact['StockCode'] = sales_fact['StockCode'].astype(str)  # Ensure StockCode is string
sales_fact['Quantity'] = sales_fact['Quantity'].astype('Int32')  # Ensure Quantity is integer (nullable)
sales_fact['UnitPrice'] = sales_fact['UnitPrice'].astype('Float32')  # Ensure UnitPrice is float
sales_fact['CustomerID'] = sales_fact['CustomerID'].astype('Int64')  # Ensure CustomerID is integer
sales_fact['Country'] = sales_fact['Country'].astype(str) 
sales_fact['Description'] = sales_fact['Description'].astype(str)
sales_fact['CustomerID'] = sales_fact['CustomerID'].astype('UInt32')

# df['Date'] = df['Date'].apply(lambda x: x.replace(year = x.year + 1))
sales_fact['InvoiceDate'] = sales_fact['InvoiceDate'].apply(lambda x: x.replace(year = x.year + 13))
print(sales_fact['InvoiceDate'])


Client.execute('DROP TABLE IF EXISTS hackathon.sales_fact')
Client.execute( 
    '''
    CREATE TABLE IF NOT EXISTS hackathon.sales_fact
    (
        InvoiceNo String,               -- Invoice number, typically a string because it may contain alphanumeric characters
        StockCode String,               -- Product unique identifier
        Description String,             -- Product description
        Quantity Int64,                 -- Quantity of items sold in the transaction
        InvoiceDate DateTime,           -- Date and time of the transaction
        UnitPrice Float32,              -- Price per unit of the product
        CustomerID UInt32,              -- Unique customer identifier
        Country String ,                 -- Country where the transaction took place
    ) 
    ENGINE = MergeTree()
    ORDER BY InvoiceNo
    '''
)
sls_prg = Client.execute('INSERT INTO hackathon.sales_fact VALUES', sales_fact.to_dict('records'))
print(sls_prg)
