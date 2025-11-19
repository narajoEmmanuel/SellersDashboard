# Web Development for Analytics Apps
# Testing Streamlit

# Student: Emmanuel Naranjo
# ID: A00835704
# Date: November 14, 2025

# ============================================================
# Description:
# This Streamlit app loads the sellers.xlsx dataset and allows
# users to explore sales data interactively. It includes:
#   - Table display with region filter
#   - Graphs of Units Sold, Total Sales, and Average Sales
#   - Vendor-specific data view
#   - Containers and interactive widgets for usability
# ============================================================

import altair as alt
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


# ---------- Page config and simple CSS for minimal look and centered title ----------
st.set_page_config(page_title="Sellers Dashboard", layout="wide")

# Minimal, system UI font stack and centered title
st.markdown("""
<style>
/* Global font */
html, body, [class*="css"]  {
  font-family: Inter, -apple-system, system-ui, Segoe UI, Roboto, Helvetica, Arial, sans-serif;
  font-size: 15px;
}
/* Center title, tighten spacing */
.centered-title h1 {
  text-align: center;
  margin-top: 0.2rem;
  margin-bottom: 0.6rem;
}
/* Subheaders a bit tighter */
.block-container h2, .block-container h3 {
  margin-top: 0.8rem;
}
/* Soft cards feel */
.stMetric, .stDataFrame, .stPlotlyChart, .stAltairChart, .stMarkdown {
  border-radius: 12px;
}
/* Make metric title bigger */
div[data-testid="stMetricLabel"] > p {
    font-size: 1.1rem;
    font-weight: 600;
}

/* Make metric value bigger */
div[data-testid="stMetricValue"] > div {
    font-size: 2.4rem !important;
    font-weight: 700 !important;
}

/* Increase vertical spacing */
div[data-testid="stMetric"] {
    padding-top: 10px;
    padding-bottom: 10px;
}
</style>
""", unsafe_allow_html=True)

# ---------- Header and student info ----------
with st.container():
    st.markdown('<div class="centered-title"><h1>Sellers Dashboard</h1></div>',
                unsafe_allow_html=True)
    st.markdown("Comprehensive view of seller performance across regions, including income, units sold, total sales, and sales averages. All charts and tables update automatically based on selected regions.")


with st.sidebar:
    st.markdown("## About")

    # User card
    st.markdown("""
    <div style='padding:15px; border-radius:10px; background-color:#f7f9fc;'>
        <h3 style='margin-bottom:5px;'>👤 Emmanuel Naranjo</h3>
        <p style='margin:0; font-size:14px;'>
            <strong>ID:</strong> A00835704<br>
            <strong>Module:</strong> Web Development for Analytics Apps<br>
            <strong>Assignment:</strong> Testing Streamlit
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.write("")  # spacing

    st.write("")  # spacing

    # Navigation menu (symbolic)
    st.markdown("### Navigation")
    st.markdown("""
    - 📊 Overview Metrics  
    - 📄 Data Table  
    - 🛍️ Sales by Vendor  
    - 🔎 Vendor Detail  
    """)

    st.info("Place sellers.xlsx in the same folder as this .py file.")

    st.write("")
    st.markdown("<hr>", unsafe_allow_html=True)

    # Footer
    st.markdown(
        "<p style='text-align:center; font-size:12px; color:#666;'>© 2025 ITESM | Streamlit Dashboard</p>",
        unsafe_allow_html=True
    )


# ---------- Load data with caching ----------


@st.cache_data
def load_data(path: str = "sellers.xlsx") -> pd.DataFrame:
    df = pd.read_excel(path)
    # Create helper columns
    df["FULL NAME"] = df["NAME"].astype(str).str.strip(
    ) + " " + df["LASTNAME"].astype(str).str.strip()
    # Ensure numeric types in case Excel exported strings
    for col in ["SOLD UNITS", "TOTAL SALES", "SALES AVERAGE", "INCOME"]:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")
    return df


df = load_data()

# Safety check for required columns
required_cols = ["REGION", "FULL NAME", "SOLD UNITS", "TOTAL SALES",
                 "SALES AVERAGE", "INCOME", "ID", "NAME", "LASTNAME"]
missing = [c for c in ["REGION", "SOLD UNITS",
                       "TOTAL SALES", "SALES AVERAGE"] if c not in df.columns]
if missing:
    st.error(f"Required columns not found: {missing}")
    st.stop()

# ---------- Top metrics, filtered by region selection ----------
with st.container():
    st.subheader("Filters")
    # Region filter with multiselect for flexibility
    regions = sorted(df["REGION"].dropna().unique().tolist())
    default_regions = regions  # show all by default
    sel_regions = st.multiselect(
        "Select Regions", regions, default_regions, help="Use this to filter everything on the page")
    mask_region = df["REGION"].isin(
        sel_regions) if sel_regions else pd.Series([True] * len(df))
    df_region = df[mask_region].copy()

# KPI row
with st.container():
    st.subheader("Overview Metrics")
    c1, c2, c3, c4 = st.columns(4)
    total_vendors = df_region["FULL NAME"].nunique()
    total_units = int(df_region["SOLD UNITS"].sum())
    total_sales = float(df_region["TOTAL SALES"].sum())
    mean_ticket = float(
        np.where(total_units > 0, total_sales / total_units, np.nan))

    c1.metric("Vendors", f"{total_vendors}")
    c2.metric("Units Sold", f"{total_units:,}")
    c3.metric("Total Sales", f"{total_sales:,.0f}")
    c4.metric("Avg Ticket", f"{mean_ticket:,.2f}" if not np.isnan(
        mean_ticket) else "N A")

# ---------- Data table with region filter and download ----------
with st.container():
    st.subheader("Dataset Filtered by Region")
    st.dataframe(df_region, use_container_width=True)
    csv = df_region.to_csv(index=False).encode("utf-8")
    st.download_button("Download filtered CSV", data=csv,
                       file_name="sellers_filtered.csv", mime="text/csv")

# ---------- Charts, improved version using Altair with horizontal bars ----------

with st.container():
    st.subheader("Sales by Vendor")

    # Aggregate by vendor for charts
    g = (
        df_region.groupby("FULL NAME", as_index=False)
                 .agg({
                     "SOLD UNITS": "sum",
                     "TOTAL SALES": "sum",
                     "SALES AVERAGE": "mean"
                 })
        .sort_values("TOTAL SALES", ascending=False)
    )

    colA, colB = st.columns(2)

    # --- Total Sales Chart (horizontal) ---
    sales_chart = (
        alt.Chart(g)
        .mark_bar(color="#4C72B0")
        .encode(
            y=alt.Y("FULL NAME:N", sort="-x", title="Vendor"),
            x=alt.X("TOTAL SALES:Q", title="Total Sales"),
            tooltip=["FULL NAME", "TOTAL SALES"]
        )
        .properties(width="container", height=350,
                    title="Total Sales by Vendor")
    )

    # --- Units Sold Chart (horizontal) ---
    units_chart = (
        alt.Chart(g)
        .mark_bar(color="#55A868")
        .encode(
            y=alt.Y("FULL NAME:N", sort="-x", title="Vendor"),
            x=alt.X("SOLD UNITS:Q", title="Units Sold"),
            tooltip=["FULL NAME", "SOLD UNITS"]
        )
        .properties(width="container", height=350,
                    title="Units Sold by Vendor")
    )

    colA.altair_chart(sales_chart, use_container_width=True)
    colB.altair_chart(units_chart, use_container_width=True)

    # --- Average Sales Chart (horizontal, full width) ---
    avg_chart = (
        alt.Chart(g)
        .mark_bar(color="#C44E52")
        .encode(
            y=alt.Y("FULL NAME:N", sort="-x", title="Vendor"),
            x=alt.X("SALES AVERAGE:Q", title="Average Sales"),
            tooltip=["FULL NAME", "SALES AVERAGE"]
        )
        .properties(width="container", height=350,
                    title="Average Sales by Vendor")
    )

    st.altair_chart(avg_chart, use_container_width=True)


# ---------- Vendor drilldown ----------
with st.container():
    st.subheader("Vendor Detail")
    vendors = sorted(df_region["FULL NAME"].unique().tolist())
    sel_vendor = st.selectbox("Select a Vendor", vendors)
    vendor_df = df_region[df_region["FULL NAME"] == sel_vendor].copy()

    # Show vendor level metrics
    v1, v2, v3, v4 = st.columns(4)
    v1.metric("Total Units", f"{int(vendor_df['SOLD UNITS'].sum()):,}")
    v2.metric("Total Sales", f"{float(vendor_df['TOTAL SALES'].sum()):,.0f}")
    # Mean of SALES AVERAGE across rows
    avg_sales = float(vendor_df["SALES AVERAGE"].mean())
    v3.metric("Sales Average", f"{avg_sales*100:.1f}%")

    v4.metric("Income", f"{float(vendor_df['INCOME'].mean()):,.0f}")

    # Show raw rows for the selected vendor
    st.markdown("**Records for selected vendor**")
    st.dataframe(vendor_df, use_container_width=True)

    # Optional action
    if st.button("Download vendor records"):
        st.download_button(
            "Save CSV",
            data=vendor_df.to_csv(index=False).encode("utf-8"),
            file_name=f"vendor_{sel_vendor.replace(' ', '_')}.csv",
            mime="text/csv",
            key="vendor_dl"
        )
