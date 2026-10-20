import csv
import random
import os

# Target file size: 1.5 GB in bytes
TARGET_SIZE_BYTES = int(1.5 * 1024 * 1024 * 1024)
FILENAME = "people.csv"

# Pre-defined pools for fast generation
FIRST_NAMES = [
    "James", "Mary", "John", "Patricia", "Robert", "Jennifer", "Michael", "Linda",
    "William", "Elizabeth", "David", "Barbara", "Richard", "Susan", "Joseph", "Jessica",
    "Thomas", "Sarah", "Charles", "Karen", "Christopher", "Nancy", "Daniel", "Lisa",
    "Matthew", "Margaret", "Anthony", "Sandra", "Donald", "Ashley", "Mark", "Kimberly"
]
LAST_NAMES = [
    "Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis",
    "Rodriguez", "Martinez", "Hernandez", "Lopez", "Gonzalez", "Wilson", "Anderson",
    "Thomas", "Taylor", "Moore", "Jackson", "Martin", "Lee", "Perez", "Thompson", "White"
]


def generate_row():
    name = f"{random.choice(FIRST_NAMES)} {random.choice(LAST_NAMES)}"
    age = random.randint(18, 80)
    # Weight in kg (correlated roughly with realistic human weight)
    weight = round(random.uniform(50.0, 110.0), 1)
    # Height in cm
    height = round(random.uniform(150.0, 195.0), 1)
    employed = random.choices([True, False], weights=[0.65, 0.35])[0]
    return [name, age, weight, height, employed]


def create_dataset():
    print(f"Generating '{FILENAME}' (~1.5 GB)...")

    with open(FILENAME, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        # Header
        writer.writerow(["name", "age", "weight", "height", "employed"])

        bytes_written = file.tell()
        rows = 0

        while bytes_written < TARGET_SIZE_BYTES:
            # Write in batches of 10,000 for maximum I/O performance
            batch = [generate_row() for _ in range(10000)]
            writer.writerows(batch)
            rows += 10000
            bytes_written = file.tell()

            # Print progress every 100MB
            mb_written = bytes_written / (1024 * 1024)
            print(f"Written: {mb_written:.2f} MB / 1536 MB", end="\r")

    final_size_gb = os.path.getsize(FILENAME) / (1024 * 1024 * 1024)
    print(f"\nDone! Generated {rows:,} rows. Final file size: {final_size_gb:.2f} GB.")


if __name__ == "__main__":
    create_dataset()