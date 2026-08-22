import matplotlib.pyplot as plt
import pandas as pd

# 1. LOAD DATA

df = pd.read_csv(
    "online_retail.csv",
    encoding_errors="ignore",
)

print("Original shape:", df.shape)

# 2. CHECK RAW DATA
print("\nFirst 5 rows:")
print(df.head())

print("\nMissing values:")
print(df.isnull().sum())

# 3. CONVERT DATE COLUMN

df["InvoiceDate"] = pd.to_datetime(
    df["InvoiceDate"],
    errors="coerce",
)

# 4. REMOVE DUPLICATES

df = df.drop_duplicates()

# 5. REMOVE INVALID SALES

df = df[
    (df["Quantity"] > 0)
    & (df["UnitPrice"] > 0)
]

# 6. REMOVE MISSING PRODUCT DESCRIPTIONS

df = df[df["Description"].notna()]


# 7. REMOVE INVALID DATES

df = df[df["InvoiceDate"].notna()]


# 8. CREATE REVENUE

df["Revenue"] = (
    df["Quantity"] * df["UnitPrice"]
)

# 9. CREATE DATE FEATURES

df["Year"] = df["InvoiceDate"].dt.year
df["Month"] = df["InvoiceDate"].dt.month
df["MonthName"] = df["InvoiceDate"].dt.strftime("%b")
df["YearMonth"] = (
    df["InvoiceDate"]
    .dt.to_period("M")
    .astype(str)
)
print("\nCleaned shape:", df.shape)

# 10. BUSINESS KPIs

total_revenue = df["Revenue"].sum()

total_orders = df["InvoiceNo"].nunique()

total_units = df["Quantity"].sum()

total_customers = df["CustomerID"].nunique()

total_products = df["StockCode"].nunique()

average_order_value = (
    total_revenue / total_orders
)


print("\n========== BUSINESS KPIs ==========")

print(
    "Total Revenue:",
    round(total_revenue, 2),
)

print(
    "Total Orders:",
    total_orders,
)

print(
    "Total Units Sold:",
    total_units,
)

print(
    "Unique Customers:",
    total_customers,
)

print(
    "Unique Products:",
    total_products,
)

print(
    "Average Order Value:",
    round(average_order_value, 2),
)

# 11. MONTHLY REVENUE

monthly_sales = (
    df.groupby("YearMonth")["Revenue"]
    .sum()
    .sort_index()
)

print("\n========== MONTHLY REVENUE ==========")
print(monthly_sales)

# 12. TOP 10 PRODUCTS

top_products = (
    df.groupby("Description")["Revenue"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

print("\n========== TOP 10 PRODUCTS ==========")
print(top_products)

# 13. TOP 10 COUNTRIES

country_sales = (
    df.groupby("Country")["Revenue"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

print("\n========== TOP 10 COUNTRIES ==========")
print(country_sales)

# 14. MONTHLY REVENUE CHART

plt.figure(figsize=(12, 6))

monthly_sales.plot(
    kind="line",
    marker="o",
)

plt.title("Monthly Revenue Trend")
plt.xlabel("Month")
plt.ylabel("Revenue")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# 15. TOP PRODUCTS CHART

plt.figure(figsize=(10, 6))

top_products.sort_values().plot(
    kind="barh",
)

plt.title("Top 10 Products by Revenue")
plt.xlabel("Revenue")
plt.ylabel("Product")
plt.tight_layout()
plt.show()

# 16. TOP COUNTRIES CHART

plt.figure(figsize=(10, 6))

country_sales.sort_values().plot(
    kind="barh",
)

plt.title("Top 10 Countries by Revenue")
plt.xlabel("Revenue")
plt.ylabel("Country")
plt.tight_layout()
plt.show()

# 17. EXPORT CLEANED DATA

df.to_csv(
    "online_retail_cleaned.csv",
    index=False,
)

print(
    "\nCleaned dataset saved as "
    "'online_retail_cleaned.csv'."
)

print("\nAnalysis completed successfully!")
