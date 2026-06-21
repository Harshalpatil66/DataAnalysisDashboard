import pandas as pd
import numpy as np

# Read CSV file
df = pd.read_csv("data/sales.csv")

# Create Total column
df["Total"] = df["Price"] * df["Quantity"]

# Display data
print(df)

# Total Revenue
print("\nTotal Revenue =", df["Total"].sum())

# NumPy Operations
prices = np.array(df["Price"])

print("\nAverage Price =", np.mean(prices))
print("Maximum Price =", np.max(prices))
print("Minimum Price =", np.min(prices))