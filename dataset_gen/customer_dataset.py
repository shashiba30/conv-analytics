import pandas as pd 
from faker import Faker
import gender_guesser.detector as gender

Faker.seed(0)
fake = Faker()
d = gender.Detector()

def get_gender_and_age(name):
    # Gender prediction
    gender_prediction = d.get_gender(name.split()[0])  # Get gender based on first name
    
    # Assign gender
    if gender_prediction == 'male':
        gender = 'Male'
        age = fake.random_int(min=18, max=60)  # Adjusted age range for male
    elif gender_prediction == 'female':
        gender = 'Female'
        age = fake.random_int(min=18, max=60)  # Adjusted age range for female
    else:
        gender = 'Other'
        age = fake.random_int(min=18, max=60)  # Default age range
    
    return gender, age

def generate_customer_dimension(sales_data):
    customer_dim = []
    for customer_id in sales_data['CustomerID'].unique():
        name = fake.name()  # Generate a random name
        gender, age = get_gender_and_age(name)  # Get gender and age based on the name
        customer = {
            'CustomerKey': customer_id,  # Use CustomerID as the key
            'CustomerID': customer_id,
            'CustomerName': name,  # Generate a fake name
            'CustomerAge': age,  # Random age between 18 and 80
            'CustomerGender': gender,  # Random gender
            'Country': sales_data[sales_data['CustomerID'] == customer_id]['Country'].values[0]  # Country from sales data
        }
        customer_dim.append(customer)
    
    return pd.DataFrame(customer_dim)

df = pd.read_excel('sdv/online+retail/Online Retail.xlsx')
print(df.head())

customer_df = df[['CustomerID','Country']].drop_duplicates()

customer_df = customer_df.dropna(subset=['CustomerID'])

customer_df['CustomerID'] = customer_df['CustomerID'].astype(int)


# Generate Customer Dimension Table
customer_dimension = generate_customer_dimension(customer_df)


customer_dimension.to_csv('data/customer_dimension.csv',index=False)

 

