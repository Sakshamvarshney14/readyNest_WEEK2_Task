import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os

# =====================================
# CREATE OUTPUT FOLDERS
# =====================================

os.makedirs("outputs/charts", exist_ok=True)

print("=" * 60)
print("CUSTOMER INSIGHTS PROJECT STARTED")
print("=" * 60)

# =====================================
# LOAD DATASETS
# =====================================

customers = pd.read_csv(
    "dataset/olist_customers_dataset.csv"
)

orders = pd.read_csv(
    "dataset/olist_orders_dataset.csv"
)

order_items = pd.read_csv(
    "dataset/olist_order_items_dataset.csv"
)

products = pd.read_csv(
    "dataset/olist_products_dataset.csv"
)

payments = pd.read_csv(
    "dataset/olist_order_payments_dataset.csv"
)

reviews = pd.read_csv(
    "dataset/olist_order_reviews_dataset.csv"
)

translation = pd.read_csv(
    "dataset/product_category_name_translation.csv"
)

print("Datasets Loaded Successfully")

# =====================================
# MERGE DATASETS
# =====================================

print("Merging datasets...")

df = orders.merge(
    customers,
    on="customer_id",
    how="left"
)

df = df.merge(
    order_items,
    on="order_id",
    how="left"
)

df = df.merge(
    products,
    on="product_id",
    how="left"
)

df = df.merge(
    payments,
    on="order_id",
    how="left"
)

df = df.merge(
    reviews,
    on="order_id",
    how="left"
)

df = df.merge(
    translation,
    on="product_category_name",
    how="left"
)

print("Merged Shape:", df.shape)

# Save merged dataset

df.to_csv(
    "outputs/final_merged_dataset.csv",
    index=False
)

# =====================================
# DATA CLEANING
# =====================================

before = len(df)

df.drop_duplicates(inplace=True)

duplicates_removed = before - len(df)

# Keep only completed orders

df = df[
    df["order_status"] == "delivered"
]

# Convert date columns

date_columns = [
    "order_purchase_timestamp",
    "order_approved_at",
    "order_delivered_carrier_date",
    "order_delivered_customer_date",
    "order_estimated_delivery_date"
]

for col in date_columns:

    if col in df.columns:

        df[col] = pd.to_datetime(
            df[col],
            errors="coerce"
        )

# Handle Missing Values

numeric_cols = df.select_dtypes(
    include=np.number
).columns

categorical_cols = df.select_dtypes(
    include="object"
).columns

for col in numeric_cols:

    df[col] = df[col].fillna(
        df[col].median()
    )

for col in categorical_cols:

    if not df[col].mode().empty:

        df[col] = df[col].fillna(
            df[col].mode()[0]
        )

# =====================================
# FEATURE ENGINEERING
# =====================================

df["Year"] = (
    df["order_purchase_timestamp"]
    .dt.year
)

df["Month"] = (
    df["order_purchase_timestamp"]
    .dt.month
)

df["Day"] = (
    df["order_purchase_timestamp"]
    .dt.day
)

df["Order_Value"] = (
    df["price"] +
    df["freight_value"]
)

df["Delivery_Days"] = (
    df["order_delivered_customer_date"]
    -
    df["order_purchase_timestamp"]
).dt.days

# New vs Returning Customers

customer_orders = (
    df.groupby(
        "customer_unique_id"
    )["order_id"]
    .nunique()
)

returning_customers = (
    customer_orders > 1
).sum()

new_customers = (
    customer_orders == 1
).sum()

# =====================================
# SORT DATASET
# =====================================

df = df.sort_values(
    by=[
        "order_purchase_timestamp",
        "customer_unique_id"
    ]
).reset_index(drop=True)

# =====================================
# REARRANGE IMPORTANT COLUMNS
# =====================================

important_cols = [
    "order_id",
    "customer_unique_id",
    "customer_city",
    "customer_state",
    "order_purchase_timestamp",
    "product_category_name_english",
    "price",
    "freight_value",
    "Order_Value",
    "payment_type",
    "review_score",
    "Delivery_Days"
]


important_cols = [
    col for col in important_cols
    if col in df.columns
]

remaining_cols = [
    col for col in df.columns
    if col not in important_cols
]

df = df[
    important_cols + remaining_cols
]

# =====================================
# SAVE CLEANED DATASET
# =====================================

df.to_csv(
    "outputs/cleaned_dataset.csv",
    index=False
)

print("Cleaning Completed")

# =====================================
# DESCRIPTIVE STATISTICS
# =====================================

stats = df.describe(include="all")

stats.to_csv(
    "outputs/descriptive_statistics.csv"
)

# =====================================
# MONTHLY SALES TREND
# =====================================

monthly_sales = (
    df.groupby(
        ["Year", "Month"]
    )["Order_Value"]
    .sum()
    .reset_index()
)

monthly_sales["Date"] = pd.to_datetime(
    monthly_sales[
        ["Year", "Month"]
    ].assign(day=1)
)

plt.figure(figsize=(12, 5))

plt.plot(
    monthly_sales["Date"],
    monthly_sales["Order_Value"]
)

plt.title("Monthly Sales Trend")

plt.xticks(rotation=45)

plt.tight_layout()

plt.savefig(
    "outputs/charts/monthly_sales.png"
)

plt.close()

# =====================================
# TOP PRODUCT CATEGORIES
# =====================================

top_products = (
    df.groupby(
        "product_category_name_english"
    )["Order_Value"]
    .sum()
    .sort_values(
        ascending=False
    )
    .head(10)
)

plt.figure(figsize=(12, 6))

top_products.plot(
    kind="bar"
)

plt.title(
    "Top Product Categories"
)

plt.xticks(rotation=45)

plt.tight_layout()

plt.savefig(
    "outputs/charts/top_products.png"
)

plt.close()

# =====================================
# SALES BY STATE
# =====================================

state_sales = (
    df.groupby(
        "customer_state"
    )["Order_Value"]
    .sum()
    .sort_values(
        ascending=False
    )
    .head(10)
)

plt.figure(figsize=(10, 5))

state_sales.plot(
    kind="bar"
)

plt.title(
    "Top States by Sales"
)

plt.tight_layout()

plt.savefig(
    "outputs/charts/sales_by_state.png"
)

plt.close()

# =====================================
# PAYMENT METHODS
# =====================================

plt.figure(figsize=(7, 7))

df["payment_type"]\
    .value_counts()\
    .plot(
        kind="pie",
        autopct="%1.1f%%"
    )

plt.ylabel("")

plt.title(
    "Payment Methods"
)

plt.tight_layout()

plt.savefig(
    "outputs/charts/payment_methods.png"
)

plt.close()

# =====================================
# REVIEW DISTRIBUTION
# =====================================

plt.figure(figsize=(8, 5))

sns.countplot(
    x="review_score",
    data=df
)

plt.title(
    "Review Score Distribution"
)

plt.tight_layout()

plt.savefig(
    "outputs/charts/review_distribution.png"
)

plt.close()

# =====================================
# TOP CUSTOMERS
# =====================================

top_customers = (
    df.groupby(
        "customer_unique_id"
    )["Order_Value"]
    .sum()
    .sort_values(
        ascending=False
    )
    .head(10)
)

plt.figure(figsize=(10, 5))

top_customers.plot(
    kind="bar"
)

plt.title(
    "Top Customers"
)

plt.tight_layout()

plt.savefig(
    "outputs/charts/top_customers.png"
)

plt.close()

# =====================================
# CORRELATION HEATMAP
# =====================================

plt.figure(figsize=(12, 8))

sns.heatmap(
    df[numeric_cols].corr(),
    cmap="coolwarm",
    annot=False
)

plt.title(
    "Correlation Heatmap"
)

plt.tight_layout()

plt.savefig(
    "outputs/charts/heatmap.png"
)

plt.close()

# =====================================
# CUSTOMER SEGMENTATION
# =====================================

customer_value = (
    df.groupby(
        "customer_unique_id"
    )["Order_Value"]
    .sum()
)

high = customer_value.quantile(0.75)
low = customer_value.quantile(0.25)

segments = []

for value in customer_value:

    if value >= high:
        segments.append(
            "High Value"
        )

    elif value <= low:
        segments.append(
            "Low Value"
        )

    else:
        segments.append(
            "Medium Value"
        )

segment_df = pd.DataFrame({
    "Customer_ID":
    customer_value.index,

    "Total_Spending":
    customer_value.values,

    "Segment":
    segments
})

segment_df.to_csv(
    "outputs/customer_segments.csv",
    index=False
)

plt.figure(figsize=(7, 5))

segment_df["Segment"]\
    .value_counts()\
    .plot(kind="bar")

plt.title(
    "Customer Segments"
)

plt.tight_layout()

plt.savefig(
    "outputs/charts/customer_segments.png"
)

plt.close()

# =====================================
# NEW VS RETURNING CUSTOMERS
# =====================================

customer_type = pd.DataFrame({
    "Customer_Type": [
        "New Customers",
        "Returning Customers"
    ],
    "Count": [
        new_customers,
        returning_customers
    ]
})

plt.figure(figsize=(7,5))

plt.bar(
    customer_type["Customer_Type"],
    customer_type["Count"]
)

plt.title(
    "New vs Returning Customers"
)

plt.tight_layout()

plt.savefig(
    "outputs/charts/new_vs_returning_customers.png"
)

plt.close()

# =====================================
# BUSINESS INSIGHTS
# =====================================

insights = f"""
CUSTOMER INSIGHT REPORT

Total Orders:
{df['order_id'].nunique()}

Total Customers:
{df['customer_unique_id'].nunique()}

New Customers:
{new_customers}

Returning Customers:
{returning_customers}

Total Revenue:
${df['Order_Value'].sum():,.2f}

Average Order Value:
${df['Order_Value'].mean():.2f}

Duplicates Removed:
{duplicates_removed}

Average Delivery Time:
{df['Delivery_Days'].mean():.2f} Days

Top Product Category:
{top_products.index[0]}

Top State:
{state_sales.index[0]}

Most Used Payment Method:
{df['payment_type'].mode()[0]}

Average Review Score:
{df['review_score'].mean():.2f}

BUSINESS RECOMMENDATIONS

1. Focus on high-value customers.

2. Improve customer retention.

3. Increase promotions in top-performing states.

4. Optimize delivery performance.

5. Promote best-selling categories.
"""

with open(
    "outputs/business_insights.txt",
    "w",
    encoding="utf-8"
) as f:

    f.write(insights)

print("=" * 60)
print("PROJECT COMPLETED SUCCESSFULLY")
print("=" * 60)

print("All outputs saved successfully.")

# =====================================
# RECOMMENDATION SYSTEM
# =====================================

from mlxtend.frequent_patterns import apriori, association_rules

print("Generating Recommendations...")
# Remove rows where product category is missing
df_recommend = df.dropna(
    subset=["product_category_name_english"]
)
basket = (
    df.groupby(
        ["customer_unique_id",
         "product_category_name_english"]
    )["order_id"]
    .count()
    .unstack()
    .fillna(0)
)

# 0/1 matrix mein convert

basket = (basket > 0).astype(int)

# Frequent Itemsets

frequent_items = apriori(
    basket.astype(bool),
    min_support=0.001,
    use_colnames=True
)
print("Frequent Itemsets:", len(frequent_items))

# Association Rules

rules = association_rules(
    frequent_items,
    metric="support",
    min_threshold=0.001
)
print("Rules Generated:", len(rules))

# Important columns select karo

if not rules.empty:

    recommendations = rules[
        [
            "antecedents",
            "consequents",
            "support",
            "confidence",
            "lift"
        ]
    ]

    recommendations["antecedents"] = (
        recommendations["antecedents"]
        .apply(lambda x: ', '.join(list(x)))
    )

    recommendations["consequents"] = (
        recommendations["consequents"]
        .apply(lambda x: ', '.join(list(x)))
    )

    recommendations = recommendations.sort_values(
        by="lift",
        ascending=False
    )

    recommendations.to_csv(
        "outputs/product_recommendations.csv",
        index=False
    )

    print(
        "Recommendations generated successfully."
    )

else:
    print(
        "No recommendation rules found."
    )
    