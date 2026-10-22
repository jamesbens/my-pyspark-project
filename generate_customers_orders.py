import csv
import random

# Configuration
NUM_ORDERS = 1000
NUM_CUSTOMERS = 150  # 150 unique customers distributed across 1000 orders

# Sample pool for generating realistic customer names and countries
FIRST_NAMES = ["James", "Sophia", "Liam", "Emma", "Noah", "Ava", "Ethan", "Isabella", "Lucas", "Mia"]
LAST_NAMES = ["Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis", "Rodriguez", "Martinez"]
COUNTRIES = ["United States", "Israel", "United Kingdom", "Canada", "Germany", "France", "Australia", "Japan"]


def generate_ecommerce_data():
    # 1. Create a set of unique customer IDs
    customer_ids = [f"CUST-{1000 + i}" for i in range(NUM_CUSTOMERS)]

    # 2. Build orders.csv and track which customer IDs were actually used
    used_customer_ids = set()

    with open("orders.csv", mode="w", newline="", encoding="utf-8") as f_orders:
        writer = csv.writer(f_orders)
        writer.writerow(["order_id", "customer_id", "amount"])  # Header

        for order_id in range(1, NUM_ORDERS + 1):
            cust_id = random.choice(customer_ids)
            amount = round(random.uniform(10.0, 500.0), 2)

            writer.writerow([order_id, cust_id, amount])
            used_customer_ids.add(cust_id)

    print(f"Successfully generated orders.csv with {NUM_ORDERS} rows.")

    # 3. Build customers.csv containing distinct customers present in orders.csv
    with open("customers.csv", mode="w", newline="", encoding="utf-8") as f_customers:
        writer = csv.writer(f_customers)
        writer.writerow(["customer_id", "name", "country"])  # Header

        for cust_id in sorted(used_customer_ids):
            full_name = f"{random.choice(FIRST_NAMES)} {random.choice(LAST_NAMES)}"
            country = random.choice(COUNTRIES)

            writer.writerow([cust_id, full_name, country])

    print(f"Successfully generated customers.csv with {len(used_customer_ids)} distinct customers.")


if __name__ == "__main__":
    generate_ecommerce_data()