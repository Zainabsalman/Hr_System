from pymongo import MongoClient

# Connect to the MongoDB server
client = MongoClient('mongodb://localhost:27017')

# Access the database
db = client['HrSystem']

# Access the collection
collection = db['Hr_App_applicants']

applicants_to_insert = [
    {
        'name': 'Zainab',
        'mobile_number': '34188951',
        'dob': '1990-01-01',
        'email': 'zainab@example.com'
    },
    # Add more documents as needed
]

# Insert the list of documents into the collection
result = collection.insert_many(applicants_to_insert)

# Print the IDs of the inserted documents
print(result)

