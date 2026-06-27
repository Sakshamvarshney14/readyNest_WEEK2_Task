import streamlit as st
import pandas as pd
import plotly.express as px

# ==========================================
# PAGE CONFIG
# ==========================================

st.set_page_config(
    page_title="Customer Insights Dashboard",
    page_icon="📊",
    layout="wide"
)

# ==========================================
# CUSTOM CSS
# ==========================================

st.markdown("""
<style>

.main {
    background-color: #F5F7FA;
}

.block-container {
    padding-top: 1rem;
    padding-bottom: 2rem;
}

h1 {
    color: #1E3A8A;
    text-align: center;
}

[data-testid="metric-container"] {
    background-color: white;
    border: 2px solid #E5E7EB;
    padding: 15px;
    border-radius: 15px;
    box-shadow: 0px 4px 12px rgba(0,0,0,0.1);
}

[data-testid="metric-container"]:hover {
    transform: scale(1.03);
    transition: 0.3s;
}

.stTabs [data-baseweb="tab-list"] {
    gap: 20px;
}

.stTabs [data-baseweb="tab"] {
    background-color: #E5E7EB;
    border-radius: 10px;
    padding: 10px 20px;
    color: black !important;
    font-weight: bold;
}

.stTabs [data-baseweb="tab"]:hover {
    background-color: #D1D5DB;
    color: black !important;
}

.stTabs [aria-selected="true"] {
    background-color: #2563EB !important;
    color: white !important;
}

</style>
""", unsafe_allow_html=True)

# ==========================================
# LOAD DATA
# ==========================================

@st.cache_data
def load_data():
    df = pd.read_csv(
        "outputs/cleaned_dataset.csv"
    )

    segments = pd.read_csv(
        "outputs/customer_segments.csv"
    )

    recommendations = pd.read_csv(
        "outputs/product_recommendations.csv"
    )

    return df, segments, recommendations


df, segments, recommendations = load_data()

# ==========================================
# SIDEBAR
# ==========================================

st.sidebar.markdown(
    """
    # 📊 Customer Analytics

    ### Business Intelligence Platform

    Analyze customer behavior,
    sales trends and recommendations.
    """
)

state = st.sidebar.multiselect(
    "Select State",
    options=sorted(df["customer_state"].dropna().unique()),
    default=sorted(df["customer_state"].dropna().unique())
)

payment = st.sidebar.multiselect(
    "Payment Method",
    options=sorted(df["payment_type"].dropna().unique()),
    default=sorted(df["payment_type"].dropna().unique())
)

filtered_df = df[
    (df["customer_state"].isin(state)) &
    (df["payment_type"].isin(payment))
]

# ==========================================
# TITLE
# ==========================================

st.markdown("""
# 📊 Customer Insights & Recommendation System

### Transforming Raw Data into Business Intelligence

This platform analyzes customer behavior,
sales performance and recommendation patterns
using the Brazilian E-Commerce Dataset.
""")

# ==========================================
# KPI CARDS
# ==========================================

total_revenue = filtered_df["Order_Value"].sum()
total_orders = filtered_df["order_id"].nunique()
total_customers = filtered_df["customer_unique_id"].nunique()
avg_order = filtered_df["Order_Value"].mean()

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "💰 Total Revenue",
    f"${total_revenue:,.0f}"
)

col2.metric(
    "📦 Total Orders",
    total_orders
)

col3.metric(
    "👥 Customers",
    total_customers
)

col4.metric(
    "🛒 Avg Order Value",
    f"${avg_order:.2f}"
)

st.divider()

# ==========================================
# TABS
# ==========================================

tab1, tab2, tab3 = st.tabs([
    "📈 Overview",
    "👥 Customer Insights",
    "🤖 Recommendations"
])

# ==========================================
# TAB 1
# ==========================================

with tab1:

    col1, col2 = st.columns(2)

    with col1:

        top_products = (
            filtered_df.groupby(
                "product_category_name_english"
            )["Order_Value"]
            .sum()
            .sort_values(ascending=False)
            .head(10)
            .reset_index()
        )

        fig = px.bar(
            top_products,
            x="product_category_name_english",
            y="Order_Value",
            title="Top Product Categories"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    with col2:

        payment_chart = px.pie(
            filtered_df,
            names="payment_type",
            title="Payment Method Distribution"
        )

        st.plotly_chart(
            payment_chart,
            use_container_width=True
        )

    monthly_sales = (
        filtered_df.groupby(
            ["Year", "Month"]
        )["Order_Value"]
        .sum()
        .reset_index()
    )

    monthly_sales["Date"] = pd.to_datetime(
        monthly_sales[["Year", "Month"]]
        .assign(day=1)
    )

    fig2 = px.line(
        monthly_sales,
        x="Date",
        y="Order_Value",
        title="Monthly Sales Trend",
        markers=True
    )

    st.plotly_chart(
        fig2,
        use_container_width=True
    )

# ==========================================
# TAB 2
# ==========================================

with tab2:

    col1, col2 = st.columns(2)

    with col1:

        segment_counts = (
            segments["Segment"]
            .value_counts()
            .reset_index()
        )

        segment_counts.columns = [
            "Segment",
            "Count"
        ]

        fig3 = px.bar(
            segment_counts,
            x="Segment",
            y="Count",
            color="Segment",
            title="Customer Segmentation"
        )

        st.plotly_chart(
            fig3,
            use_container_width=True
        )

    with col2:

        top_customers = (
            filtered_df.groupby(
                "customer_unique_id"
            )["Order_Value"]
            .sum()
            .sort_values(ascending=False)
            .head(10)
            .reset_index()
        )

        fig4 = px.bar(
            top_customers,
            x="customer_unique_id",
            y="Order_Value",
            title="Top Customers"
        )

        st.plotly_chart(
            fig4,
            use_container_width=True
        )

    st.subheader("Customer Segment Dataset")

    st.dataframe(
        segments.head(20),
        use_container_width=True
    )

# ==========================================
# TAB 3
# ==========================================

with tab3:

    st.subheader(
        "Product Recommendations"
    )

    st.dataframe(
        recommendations,
        use_container_width=True
    )

    st.subheader(
        "Business Recommendations"
    )

    st.success(
        """
        • Focus on High Value Customers

        • Improve Customer Retention

        • Promote Top Selling Categories

        • Optimize Delivery Performance

        • Increase Marketing in Top States
        """
    )
    st.metric(
    "Recommendation Rules Generated",
    len(recommendations)
    )

# ==========================================
# DATASET PREVIEW
# ==========================================

st.divider()

with st.expander("🔍 View Dataset Preview"):

    st.dataframe(
        filtered_df.head(20),
        use_container_width=True
    )

# ==========================================
# DOWNLOAD BUTTON
# ==========================================

csv = filtered_df.to_csv(index=False)

st.download_button(
    label="⬇ Download Filtered Dataset",
    data=csv,
    file_name="filtered_dataset.csv",
    mime="text/csv"
)
