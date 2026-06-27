# 📊 Customer Insights & Recommendation System

## Overview

The **Customer Insights & Recommendation System** is an end-to-end Data Analytics and Business Intelligence project developed using the **Brazilian E-Commerce Public Dataset by Olist**.

The project transforms raw e-commerce data into actionable business insights by integrating data processing, exploratory analysis, customer segmentation, recommendation systems, interactive dashboards, and web-based analytics.

The solution helps businesses:

* Analyze customer purchasing behavior
* Monitor sales performance
* Identify top-performing products and regions
* Segment customers based on spending patterns
* Generate personalized product recommendations
* Support data-driven business decisions

---

# 🏗 Project Architecture

```text
Data Sources
     │
     ▼
Data Integration Layer
     │
     ▼
Data Cleaning Layer
     │
     ▼
Feature Engineering Layer
     │
     ▼
Exploratory Data Analysis
     │
     ▼
Customer Segmentation
     │
     ▼
Recommendation Engine
     │
     ▼
Business Insights Generation
     │
     ▼
Power BI Dashboard
     │
     ▼
Streamlit Web Application
```

---

# 🎯 Project Objectives

* Analyze customer purchasing behavior.
* Discover sales trends and regional performance.
* Identify high-value customers.
* Compare new and returning customers.
* Generate product recommendations.
* Develop interactive business dashboards.
* Provide strategic business recommendations.

---

# 📂 Dataset

**Dataset Used:** Brazilian E-Commerce Public Dataset by Olist

### Files Used

* `olist_customers_dataset.csv`
* `olist_orders_dataset.csv`
* `olist_order_items_dataset.csv`
* `olist_products_dataset.csv`
* `olist_order_payments_dataset.csv`
* `olist_order_reviews_dataset.csv`
* `product_category_name_translation.csv`

---

# 📁 Repository Structure

```text
Customer_Insights_Recommendation_Project/

├── app/
│   └── app.py
│
├── dataset/
│   ├── olist_customers_dataset.csv
│   ├── olist_orders_dataset.csv
│   ├── olist_order_items_dataset.csv
│   ├── olist_products_dataset.csv
│   ├── olist_order_payments_dataset.csv
│   ├── olist_order_reviews_dataset.csv
│   └── product_category_name_translation.csv
│
├── outputs/
│   ├── final_merged_dataset.csv
│   ├── cleaned_dataset.csv
│   ├── customer_segments.csv
│   ├── product_recommendations.csv
│   ├── business_insights.txt
│   └── charts/
│
├── dashboard/
│   ├── Customer_Insights_Dashboard.pbix
│   ├── page1.png
│   ├── page2.png
│   └── page3.png
│
├── reports/
│   └── project_report.pdf
│
├── main.py
├── requirements.txt
└── README.md
```

---

# ⚙ Technologies Used

## Programming & Analytics

* Python
* Pandas
* NumPy

## Visualization

* Matplotlib
* Seaborn
* Plotly
* Power BI
* Streamlit

## Machine Learning & Analytics

* Scikit-Learn
* Mlxtend

---

# 🔄 Data Processing Pipeline

The project performs the following data engineering tasks:

* Multi-file dataset merging
* Missing value treatment
* Duplicate removal
* Datetime conversion
* Data standardization
* Feature engineering

Generated Features:

* Order Value
* Delivery Days
* Purchase Year
* Purchase Month
* Purchase Day

---

# 📈 Exploratory Data Analysis

The project analyzes:

* Monthly Sales Trends
* Product Category Performance
* Customer Spending Patterns
* State-wise Revenue Analysis
* Payment Method Distribution
* Customer Review Distribution
* Delivery Performance Analysis

---

# 👥 Customer Analytics

## Customer Segmentation

Customers are segmented into:

* High Value Customers
* Medium Value Customers
* Low Value Customers

Segmentation is performed based on total customer spending.

---

# 🤖 Recommendation System

The recommendation engine uses:

## Technique

* Apriori Algorithm
* Association Rule Mining

## Metrics

* Support
* Confidence
* Lift

The system identifies products frequently purchased together and generates product recommendations.

---

# 📊 Interactive Dashboards

## Power BI Dashboard

### Page 1: Executive Overview

* Revenue KPIs
* Total Orders
* Total Customers
* Monthly Sales Trend
* Top Product Categories
* State-wise Sales Map

### Page 2: Customer Insights

* Customer Segmentation
* Top Customers
* New vs Returning Customers
* Product Recommendations
* Business Recommendations

### Page 3: Advanced Analytics

* Review Score Analysis
* Delivery Performance
* State-wise Analysis
* Interactive Filters

---

# 🌐 Streamlit Web Application

The project also includes an interactive Streamlit dashboard featuring:

* KPI Cards
* Sidebar Filters
* Interactive Charts
* Customer Analytics
* Product Recommendations
* Dataset Preview

---

# 📊 Key Visualizations

* KPI Cards
* Line Charts
* Bar Charts
* Pie Charts
* Correlation Heatmap
* Geographic Analysis
* Customer Segment Charts

---

# 💡 Business Insights

* Credit Card is the most preferred payment method.
* Bed Bath Table is among the highest-performing categories.
* High-value customers contribute significantly to total revenue.
* Certain states generate substantially higher sales.
* Customer satisfaction remains relatively high with average review scores around 4/5.

---

# 🚀 Business Recommendations

1. Focus marketing efforts on high-value customers.
2. Improve customer retention strategies.
3. Promote best-selling product categories.
4. Optimize delivery performance.
5. Expand campaigns in high-performing regions.

---

# 🔮 Future Enhancements

* RFM-based customer segmentation
* Advanced recommendation algorithms
* Customer Lifetime Value Prediction
* Real-time analytics dashboard
* Cloud deployment integration
* Streamlit cloud deployment

---

# 📌 Business Value

This project enables organizations to:

* Improve customer understanding
* Monitor business performance
* Increase revenue visibility
* Enhance customer retention
* Support strategic decision-making
* Discover hidden business opportunities

---

# 👨‍💻 Author

**Saksham Varshney**

Data Analytics
