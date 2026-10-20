import pandas as pd

# Load the CSV file into a DataFrame
df = pd.read_csv("people.csv")

# Display the first 5 rows (default)
print(df.head())