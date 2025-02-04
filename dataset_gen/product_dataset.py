import pandas as pd 

df = pd.read_excel('sdv/online+retail/Online Retail.xlsx')
print(df.head())

# Extract unique StockCodes and Descriptions
unique_products = df[['StockCode', 'Description']].drop_duplicates()

# Show the first few rows to confirm
unique_products.head()

import pandas as pd
import random
import re 

# # Define keyword sets for categories and subcategories
# category_keywords = {
#     'Electronics': ['phone', 'laptop', 'headphones', 'tablet', 'camera'],
#     'Appliances': ['blender', 'microwave', 'washing machine', 'toaster', 'vacuum'],
#     'Clothing': ['t-shirt', 'jeans', 'jacket', 'dress', 'sweater'],
#     'Kitchen': ['coffee maker', 'microwave', 'blender', 'toaster'],
#     'Furniture': ['sofa', 'chair', 'table', 'bookshelf', 'bed']
# }

# subcategory_keywords = {
#     'Computers': ['laptop', 'desktop', 'computer'],
#     'Phones': ['smartphone', 'cell phone', 'mobile'],
#     'Wearable Tech': ['headphones', 'watch', 'fitness band'],
#     'Home Appliances': ['blender', 'microwave', 'washing machine'],
#     'Small Appliances': ['toaster', 'vacuum'],
#     'Furniture': ['sofa', 'chair', 'table'],
#     'Apparel': ['t-shirt', 'jeans', 'jacket', 'dress', 'sweater']
# }

# def classify_product(description):
#     # If the description is NaN or empty, assign a default value
#     if pd.isna(description) or description == '':
#         description = 'No Description'
    
#     # If the description contains numbers, we convert them to strings
#     description = str(description).lower()
    
#     # Check for categories
#     category = None
#     for cat, keywords in category_keywords.items():
#         if any(keyword in description for keyword in keywords):
#             category = cat
#             break
    
#     # Check for subcategories
#     subcategory = None
#     for subcat, keywords in subcategory_keywords.items():
#         if any(keyword in description for keyword in keywords):
#             subcategory = subcat
#             break
    
#     # If no match, assign 'Other' to category and subcategory
#     if category is None:
#         category = 'Other'
#     if subcategory is None:
#         subcategory = 'Other'
    
#     return category, subcategory

# category_keywords = {
#     'Electronics': r'(phone|laptop|headphones|tablet|camera|smartphone|digital)',
#     'Appliances': r'(blender|microwave|washing machine|toaster|vacuum|coffee maker)',
#     'Clothing': r'(t-shirt|jeans|jacket|dress|sweater|shirt)',
#     'Kitchen': r'(coffee maker|microwave|blender|toaster|grinder)',
#     'Furniture': r'(sofa|chair|table|bookshelf|bed|couch|armchair)'
# }

# subcategory_keywords = {
#     'Computers': r'(laptop|desktop|computer|macbook)',
#     'Phones': r'(smartphone|mobile|cell phone)',
#     'Wearable Tech': r'(headphones|fitness band|smartwatch|earphones)',
#     'Home Appliances': r'(blender|microwave|washing machine|vacuum)',
#     'Small Appliances': r'(toaster|coffee maker|grinder)',
#     'Furniture': r'(sofa|chair|table|bookshelf|armchair)',
#     'Apparel': r'(t-shirt|jeans|jacket|dress|sweater|shirt)'
# }

# # # Function to classify products using regular expressions
# def classify_product_with_regex(description):
#     # If the description is NaN or empty, assign a default value
#     if pd.isna(description) or description == '':
#         description = 'No Description'
    
#     # If the description contains numbers, we convert them to strings
#     description = str(description).lower()

#     # Check for categories
#     category = None
#     for cat, regex in category_keywords.items():
#         if re.search(regex, description):
#             category = cat
#             break
    
#     # Check for subcategories
#     subcategory = None
#     for subcat, regex in subcategory_keywords.items():
#         if re.search(regex, description):
#             subcategory = subcat
#             break
    
#     # If no match, assign 'Other' to category and subcategory
#     if category is None:
#         category = 'Other'
#     if subcategory is None:
#         subcategory = 'Other'
    
#     return category, subcategory

# # # Sample usage on your UCI data (assuming 'Description' is in your UCI dataset)
# # uci_data = pd.read_csv('path_to_your_uci_dataset.csv')  # Replace with your actual path
# df['Category'], df['Subcategory'] = zip(*df['Description'].apply(classify_product_with_regex))

# # Show the first few rows of the classified data
# df[['Description', 'Category', 'Subcategory']].head()


# def generate_product_dimension_from_uci(uci_data):
#     product_dim = []
    
#     for idx, row in uci_data.iterrows():
#         # Classify the product based on description
#         category, subcategory = classify_product_with_regex(row['Description'])
        
#         product = {
#             'ProductKey': idx + 1,  # Unique ProductKey
#             'StockCode': row['StockCode'],
#             'ProductName': row['Description'],
#             'ProductCategory': category,  # Assigned Category
#             'ProductSubcategory': subcategory,  # Assigned Subcategory
#             'Description': row['Description']  # Original description
#         }
#         product_dim.append(product)
    
#     return pd.DataFrame(product_dim)

# # Generate the Product Dimension Table based on UCI data
# product_dimension = generate_product_dimension_from_uci(df)
# product_dimension.head()

# # product_dimension.to_csv('data/product_dimension.csv',index=False)


# from sklearn.feature_extraction.text import TfidfVectorizer
# from sklearn.model_selection import train_test_split
# from sklearn.linear_model import LogisticRegression
# from sklearn.metrics import classification_report

# # Expanded keywords for categories and subcategories
# category_keywords = {
#     'Electronics': r'(phone|laptop|headphones|tablet|camera|smartphone|digital|charger|tv|monitor|speaker|earbuds)',
#     'Appliances': r'(blender|microwave|washing machine|toaster|vacuum|coffee maker|fridge|dishwasher|dryer|stove|air conditioner)',
#     'Clothing': r'(t-shirt|jeans|jacket|dress|sweater|shirt|pants|shorts|sweatshirt|suit|skirt)',
#     'Kitchen': r'(coffee maker|microwave|blender|toaster|grinder|oven|kettle|dishwasher|juicer|cooker)',
#     'Furniture': r'(sofa|chair|table|bookshelf|bed|couch|armchair|recliner|wardrobe|dresser|cabinet|desk|furniture)'
# }

# subcategory_keywords = {
#     'Computers': r'(laptop|desktop|computer|macbook|tablet|notebook)',
#     'Phones': r'(smartphone|mobile|cell phone|android|iphone)',
#     'Wearable Tech': r'(headphones|fitness band|smartwatch|earphones|wireless earbuds)',
#     'Home Appliances': r'(blender|microwave|washing machine|vacuum|coffee maker|fridge|dishwasher)',
#     'Small Appliances': r'(toaster|coffee maker|grinder|kettle|juicer)',
#     'Furniture': r'(sofa|chair|table|bookshelf|armchair|bed|couch)',
#     'Apparel': r'(t-shirt|jeans|jacket|dress|sweater|shirt|pants|shorts|suit)'
# }


# import re

# def preprocess_description(description):
#     # Remove non-alphabetic characters and extra spaces
#     description = re.sub(r'[^a-zA-Z\s]', '', description)
#     # Convert to lowercase
#     description = description.lower()
#     # Remove extra spaces
#     description = ' '.join(description.split())
#     return description

# # Apply the preprocessing function
# product_dimension['Cleaned_Description'] = product_dimension['Description'].apply(preprocess_description)

# # Apply the classification function to the cleaned descriptions
# df['Category'], df['Subcategory'] = zip(*df['Cleaned_Description'].apply(classify_product_with_regex))

# # Check the distribution of categories again
# category_counts = df['Category'].value_counts()
# subcategory_counts = df['Subcategory'].value_counts()

# print(category_counts)
# print(subcategory_counts)







# import pandas as pd
# import re

# # Expanded keywords for categories and subcategories
# category_keywords = {
#     'Electronics': r'(phone|laptop|headphones|tablet|camera|smartphone|digital|charger|tv|monitor|speaker|earbuds|gadget)',
#     'Appliances': r'(blender|microwave|washing machine|toaster|vacuum|coffee maker|fridge|dishwasher|dryer|stove|air conditioner|iron)',
#     'Clothing': r'(t-shirt|jeans|jacket|dress|sweater|shirt|pants|shorts|sweatshirt|suit|skirt|blouse|coat|scarf|hat)',
#     'Kitchen': r'(coffee maker|microwave|blender|toaster|grinder|oven|kettle|dishwasher|juicer|cooker|chopper|fryer)',
#     'Furniture': r'(sofa|chair|table|bookshelf|bed|couch|armchair|recliner|wardrobe|dresser|cabinet|desk|furniture|stool|bench|cabinet)',
#     'Other': r'(.*)'  # Match anything that does not belong to other categories
# }

# subcategory_keywords = {
#     'Computers': r'(laptop|desktop|computer|macbook|tablet|notebook|gaming)',
#     'Phones': r'(smartphone|mobile|cell phone|android|iphone|smartwatch)',
#     'Wearable Tech': r'(headphones|fitness band|smartwatch|earphones|wireless earbuds|fitbit)',
#     'Home Appliances': r'(blender|microwave|washing machine|vacuum|coffee maker|fridge|dishwasher|dryer|stove)',
#     'Small Appliances': r'(toaster|coffee maker|grinder|kettle|juicer|air fryer|mixer)',
#     'Furniture': r'(sofa|chair|table|bookshelf|armchair|bed|couch|recliner|wardrobe|dresser|cabinet)',
#     'Apparel': r'(t-shirt|jeans|jacket|dress|sweater|shirt|pants|shorts|skirt|blouse)'
# }

# # Function to preprocess the description (handle NaN, blank, and special characters)
# def preprocess_description(description):
#     # Ensure that the description is a string (convert float or NaN to a string)
#     description = str(description)  # Convert to string

#     # If the description is empty or just whitespace, assign a default value
#     if description.strip() == '' or description == 'nan':
#         return 'No Description'
    
#     # Remove non-alphabetic characters and extra spaces
#     description = re.sub(r'[^a-zA-Z\s]', '', description)
#     # Convert to lowercase
#     description = description.lower()
#     # Remove extra spaces
#     description = ' '.join(description.split())
#     return description

# # Function to classify products based on expanded regex patterns
# def classify_product(description):
#     description = preprocess_description(description)
    
#     # Check for categories
#     category = 'Other'
#     for cat, regex in category_keywords.items():
#         if re.search(regex, description):
#             category = cat
#             break
    
#     # Check for subcategories
#     subcategory = 'Other'
#     for subcat, regex in subcategory_keywords.items():
#         if re.search(regex, description):
#             subcategory = subcat
#             break
    
#     return category, subcategory

# # Sample usage on your UCI data (assuming 'Description' is in your UCI dataset)
# uci_data = df

# # Apply the classification function
# uci_data['Category'], uci_data['Subcategory'] = zip(*uci_data['Description'].apply(classify_product))

# # Check the distribution of categories again
# category_counts = uci_data['Category'].value_counts()
# subcategory_counts = uci_data['Subcategory'].value_counts()

# # Print the updated counts
# print("Category Counts:\n", category_counts)
# print("Subcategory Counts:\n", subcategory_counts)

# # Optionally, you can also show a few examples from the "Other" category
# other_samples = uci_data[uci_data['Category'] == 'Other'].head(10)
# print("\nSamples from 'Other' Category:\n", other_samples[['Description', 'Category', 'Subcategory']])


# import pandas as pd
# import re
# from sklearn.feature_extraction.text import TfidfVectorizer
# from sklearn.model_selection import train_test_split
# from sklearn.linear_model import LogisticRegression
# from sklearn.metrics import classification_report

# # Preprocess the descriptions to handle missing data and clean text
# def preprocess_description(description):
#     # Ensure that the description is a string (convert float or NaN to a string)
#     description = str(description)  # Convert to string

#     # If the description is empty or just whitespace, assign a default value
#     if description.strip() == '' or description == 'nan':
#         return 'Unknown'
    
#     # Remove non-alphabetic characters and extra spaces
#     description = re.sub(r'[^a-zA-Z\s]', '', description)
#     # Convert to lowercase
#     description = description.lower()
#     # Remove extra spaces
#     description = ' '.join(description.split())
#     return description

# # Clean the descriptions
# uci_data['Cleaned_Description'] = uci_data['Description'].apply(preprocess_description)

# # Check if there are any missing categories or descriptions
# print(uci_data['Cleaned_Description'].isnull().sum(), "missing descriptions")
# print(uci_data['Category'].isnull().sum(), "missing categories")

# # If there are any missing values in 'Category', remove those rows
# uci_data = uci_data.dropna(subset=['Category'])

# # Feature matrix (X) and target vector (y)
# X = uci_data['Cleaned_Description']
# y = uci_data['Category']

# # Vectorize the descriptions using TF-IDF
# vectorizer = TfidfVectorizer(max_features=5000)
# X_tfidf = vectorizer.fit_transform(X)

# # Split the data into train and test sets
# X_train, X_test, y_train, y_test = train_test_split(X_tfidf, y, test_size=0.3, random_state=42)

# # Train a Logistic Regression model
# # classifier = LogisticRegression(max_iter=1000)  # Increase max_iter if convergence warning
# # classifier.fit(X_train, y_train)

# classifier = LogisticRegression(max_iter=1000, class_weight='balanced')  # 'balanced' adjusts weights automatically
# classifier.fit(X_train, y_train)

# # Predict the categories on the test set
# y_pred = classifier.predict(X_test)

# # Evaluate the model
# print("Classification Report:\n", classification_report(y_test, y_pred))

# y_pred = classifier.predict(X_test)

# # Output the predicted categories for the test set
# print("Predicted Categories for the Test Set:", y_pred)

# # Combine the true values and predicted values for inspection
# predictions_df = pd.DataFrame({'True Category': y_test, 'Predicted Category': y_pred})
# print(predictions_df.head())


# from imblearn.over_sampling import SMOTE

# # Apply SMOTE to balance the dataset
# # smote = SMOTE(random_state=42)
# # X_train_smote, y_train_smote = smote.fit_resample(X_train, y_train)

# smote = SMOTE(sampling_strategy={'Other': 10000, 'Appliances': 5000, 'Clothing': 10000, 'Electronics': 5000, 'Furniture': 5000, 'Kitchen': 5000}, random_state=42)
# X_train_smote, y_train_smote = smote.fit_resample(X_train, y_train)

# # Train a Logistic Regression model on the balanced dataset
# classifier = LogisticRegression(max_iter=1000)
# classifier.fit(X_train_smote, y_train_smote)

# # Predict the categories on the test set
# y_pred = classifier.predict(X_test)

# # Evaluate the model
# print("Classification Report (with SMOTE):\n", classification_report(y_test, y_pred))

# from sklearn.model_selection import cross_val_score
# # Perform cross-validation
# cv_scores = cross_val_score(classifier, X_train_smote, y_train_smote, cv=5)  # 5-fold cross-validation
# print(f"Cross-Validation Scores: {cv_scores}")
# print(f"Average CV Score: {cv_scores.mean()}")


# predictions_df.to_csv('data/pre_product_dimension.csv',index=False)

import pandas as pd
import re

category_keywords = {
    'Electronics': r'(phone|laptop|headphones|tablet|camera|smartphone|digital|charger|tv|monitor|speaker|earbuds|gadget)',
    'Appliances': r'(blender|microwave|washing machine|toaster|vacuum|coffee maker|fridge|dishwasher|dryer|stove|air conditioner|iron)',
    'Clothing': r'(t-shirt|jeans|jacket|dress|sweater|shirt|pants|shorts|sweatshirt|suit|skirt|blouse|coat|scarf|hat)',
    'Kitchen': r'(coffee maker|microwave|blender|toaster|grinder|oven|kettle|dishwasher|juicer|cooker|chopper|fryer)',
    'Furniture': r'(sofa|chair|table|bookshelf|bed|couch|armchair|recliner|wardrobe|dresser|cabinet|desk|furniture|stool|bench|cabinet)',
    'Other': r'(.*)'  # Match anything that does not belong to other categories
}

subcategory_keywords = {
    'Computers': r'(laptop|desktop|computer|macbook|tablet|notebook|gaming)',
    'Phones': r'(smartphone|mobile|cell phone|android|iphone|smartwatch)',
    'Wearable Tech': r'(headphones|fitness band|smartwatch|earphones|wireless earbuds|fitbit)',
    'Home Appliances': r'(blender|microwave|washing machine|vacuum|coffee maker|fridge|dishwasher|dryer|stove)',
    'Small Appliances': r'(toaster|coffee maker|grinder|kettle|juicer|air fryer|mixer)',
    'Furniture': r'(sofa|chair|table|bookshelf|armchair|bed|couch|recliner|wardrobe|dresser|cabinet)',
    'Apparel': r'(t-shirt|jeans|jacket|dress|sweater|shirt|pants|shorts|skirt|blouse)'
}

def preprocess_description(description):
    # Ensure that the description is a string (convert float or NaN to a string)
    description = str(description)  # Convert to string
    
    # Handle specific invalid descriptions like '?', '??', '???', 'nan'
    if re.match(r'^[?]+$', description) or description.strip().lower() in ['nan', '', 'no description', 'unknown']:
        return 'Unknown'

    # Remove non-alphabetic characters and extra spaces, keeping only letters and spaces
    description = re.sub(r'[^a-zA-Z\s]', '', description)
    
    # Convert to lowercase and remove extra spaces
    description = description.lower()
    description = ' '.join(description.split())
    
    # If the description is still empty or only contains invalid chars, return 'Unknown'
    if not description.strip():
        return 'Unknown'
    
    return description

# Function to classify products based on expanded regex patterns
def classify_product(description):
    description = preprocess_description(description)
    
    # Check for categories
    category = 'Other'
    for cat, regex in category_keywords.items():
        if re.search(regex, description):
            category = cat
            break
    
    # Check for subcategories
    subcategory = 'Other'
    for subcat, regex in subcategory_keywords.items():
        if re.search(regex, description):
            subcategory = subcat
            break
    
    return category, subcategory

# Assuming `uci_data` is your dataframe containing the sales data
uci_data = unique_products  # Replace `df` with your actual dataframe

uci_data['Cleaned_Description'] = uci_data['Description'].apply(preprocess_description)

# Apply the classification function
uci_data['Category'], uci_data['Subcategory'] = zip(*uci_data['Cleaned_Description'].apply(classify_product))

# Generate Product Dimension Table
def generate_product_dimension_table(uci_data):
    product_dim = uci_data[['StockCode', 'Description', 'Category', 'Subcategory','Cleaned_Description']].drop_duplicates()
    product_dim['ProductKey'] = product_dim.index + 1  # Add a unique ProductKey for each product
    return product_dim[['ProductKey', 'StockCode', 'Description', 'Category', 'Subcategory','Cleaned_Description']]

# Generate Product Dimension Table
product_dimension = generate_product_dimension_table(uci_data)

# Print the first few rows of the Product Dimension Table
print(product_dimension.head())

valid_sku_pattern = r'^[A-Za-z0-9]{5,}$'  # Modify this pattern to fit your SKU format

# Step 1: Remove rows where StockCode is NaN
uci_data = product_dimension.dropna(subset=['StockCode'])

# Step 2: Filter out rows where StockCode is not valid (does not match the pattern)
uci_data_valid = uci_data[uci_data['StockCode'].str.match(valid_sku_pattern, na=False)]

# Output the cleaned dataset
print(uci_data_valid)

uci_data_valid.to_csv('data/product_dimension.csv',index=False)