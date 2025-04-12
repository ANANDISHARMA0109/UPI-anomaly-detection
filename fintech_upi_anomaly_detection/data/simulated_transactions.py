import random
import csv
from faker import Faker
from datetime import datetime, timedelta
import uuid

# Initialize Faker and random seeds
fake = Faker()
Faker.seed(42)
random.seed(42)

users = [f"user_{i}" for i in range(1, 21)]
devices = [f"device_{i}" for i in range(1, 11)]
locations = ['Delhi', 'Mumbai', 'Bangalore', 'Kolkata', 'Chennai', 'Hyderabad', 'Pune']

# Merchant category to name mapping
merchant_categories = {
    "Food": ["Zomato", "Swiggy", "Dominos"],
    "E-Commerce": ["Amazon", "Flipkart", "Myntra"],
    "Grocery": ["BigBasket", "JioMart", "Nature's Basket"],
    "Travel": ["Uber", "Ola", "IRCTC"],
    "Bills": ["Airtel", "BESCOM", "Mahanagar Gas"],
    "Healthcare": ["1mg", "Apollo", "PharmEasy"],
    "Entertainment": ["Netflix", "Hotstar", "BookMyShow"]
}

# Simulated UPI handles (recipients)
recipients = ["@paytm", "@upi", "@ybl", "@oksbi", "@okhdfcbank"]

# Assign a consistent device per user
user_device_map = {user: random.choice(devices) for user in users}

# Generate one transaction
def generate_transaction():
    is_anomalous = random.choices([0, 1], weights=[0.95, 0.05])[0]

    user_id = random.choice(users)
    device_id = user_device_map[user_id]
    category = random.choice(list(merchant_categories.keys()))
    merchant = random.choice(merchant_categories[category])
    location = random.choice(locations[:3])
    recipient_id = random.choice(recipients)
    transaction_id = str(uuid.uuid4())
    amount = round(random.uniform(100, 3000), 2)

    # Generate a random datetime in the past 30 days
    transaction_datetime = datetime.now() - timedelta(
        days=random.randint(0, 30),
        hours=random.randint(0, 23),
        minutes=random.randint(0, 59)
    )

    if is_anomalous:
        amount = round(random.uniform(5000, 20000), 2)
        location = random.choice(locations)
        device_id = str(uuid.uuid4())  # unknown device
        transaction_datetime = datetime.now() + timedelta(
            hours=random.randint(0, 24)
        )

    timestamp = transaction_datetime.strftime("%Y-%m-%d %H:%M:%S")
    day_of_week = transaction_datetime.strftime("%A")

    return {
        "transaction_id": transaction_id,
        "user_id": user_id,
        "device_id": device_id,
        "amount": amount,
        "timestamp": timestamp,
        "day_of_week": day_of_week,
        "location": location,
        "recipient_id": recipient_id,
        "merchant_category": category,
        "merchant_name": merchant
    }

# Generate and save 1000 transactions
with open("simulated_upi_transactions.csv", "w", newline="") as file:
    fieldnames = [
        "transaction_id", "user_id", "device_id", "amount", "timestamp",
        "day_of_week", "location", "recipient_id", "merchant_category", "merchant_name"
    ]
    writer = csv.DictWriter(file, fieldnames=fieldnames)
    writer.writeheader()

    for _ in range(5000):
        writer.writerow(generate_transaction())
