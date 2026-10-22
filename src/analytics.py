"""
DMart Retail Data Analytics - KPI Computation & Visual Reporting
Author: Abhighna Mopidevi
Date: October 2026

Description:
Computes executive retail KPIs (Net Sales, Gross Profit, ABV, ASP, UPT, ARPU,
Cancellation & Return rates) across categories, channels, customer cohorts,
and store networks. Exports summary tables and generates publication-grade charts.
"""

import os
import json
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROCESSED_DATA_DIR = os.path.join(BASE_DIR, "data", "processed")
REPORTS_DIR = os.path.join(BASE_DIR, "reports")
CHARTS_DIR = os.path.join(REPORTS_DIR, "charts")
os.makedirs(CHARTS_DIR, exist_ok=True)

# Plot settings
plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
plt.rcParams['font.sans-serif'] = 'Arial'
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['figure.dpi'] = 300

NAVY = '#1A365D'
BLUE = '#2B6CB0'
TEAL = '#319795'
CORAL = '#DD6B20'
RED = '#E53E3E'
GREEN = '#38A169'

def compute_kpis():
    cust_clean = pd.read_csv(os.path.join(PROCESSED_DATA_DIR, "Dmart_Customer_Master_Cleaned.csv"))
    tx_clean = pd.read_csv(os.path.join(PROCESSED_DATA_DIR, "Dmart_Consumer_Transactions_Cleaned.csv"))
    
    # Merge customer info
    tx_full = tx_clean.merge(
        cust_clean[['Customer_ID', 'Customer_Segment', 'Loyalty_Tier', 'City', 'State']],
        on='Customer_ID',
        how='left'
    )
    tx_full['Customer_Segment'] = tx_full['Customer_Segment'].fillna('Unregistered / Guest')
    tx_full['Loyalty_Tier'] = tx_full['Loyalty_Tier'].fillna('Unregistered / Guest')
    
    completed_tx = tx_full[tx_full['Transaction_Status'] == 'Completed'].copy()
    cancelled_tx = tx_full[tx_full['Transaction_Status'] == 'Cancelled'].copy()
    returned_tx = tx_full[tx_full['Transaction_Status'] == 'Returned'].copy()
    pending_tx = tx_full[tx_full['Transaction_Status'] == 'Pending'].copy()
    
    # Financial metrics
    gross_sales = completed_tx['Gross_Sales_INR'].sum()
    discounts = completed_tx['Discount_Amount_INR'].sum()
    net_sales = completed_tx['Net_Sales_INR'].sum()
    cogs = completed_tx['COGS_INR'].sum()
    gross_profit = completed_tx['Gross_Profit_INR'].sum()
    gross_margin_pct = (gross_profit / net_sales) * 100
    
    orders = len(completed_tx)
    units = completed_tx['Quantity_Cleaned'].sum()
    abv = net_sales / orders
    asp = net_sales / units
    upt = units / orders
    
    active_cust = completed_tx['Customer_ID'].dropna().nunique()
    arpu = net_sales / active_cust
    
    kpis = {
        "Gross_Sales_INR": round(float(gross_sales), 2),
        "Total_Discounts_INR": round(float(discounts), 2),
        "Realized_Net_Sales_INR": round(float(net_sales), 2),
        "COGS_INR": round(float(cogs), 2),
        "Gross_Profit_INR": round(float(gross_profit), 2),
        "Gross_Margin_%": round(float(gross_margin_pct), 2),
        "Completed_Orders": int(orders),
        "Total_Units_Sold": int(units),
        "Average_Basket_Value_INR": round(float(abv), 2),
        "Average_Selling_Price_INR": round(float(asp), 2),
        "Units_Per_Transaction": round(float(upt), 2),
        "Active_Customers": int(active_cust),
        "ARPU_INR": round(float(arpu), 2),
        "Cancellation_Rate_%": round(float((len(cancelled_tx)/len(tx_full))*100), 2),
        "Return_Rate_%": round(float((len(returned_tx)/(orders + len(returned_tx)))*100), 2)
    }
    
    with open(os.path.join(REPORTS_DIR, "kpi_summary.json"), "w") as f:
        json.dump(kpis, f, indent=4)
        
    print("=== COMPUTED KPIS ===")
    for k, v in kpis.items():
        print(f"{k}: {v}")
        
    # Generate charts
    # 1. Category Margin & Net Sales
    cat_summary = completed_tx.groupby('Category').agg(
        Net_Sales=('Net_Sales_INR', 'sum'),
        Gross_Profit=('Gross_Profit_INR', 'sum')
    ).reset_index()
    cat_summary['Margin_%'] = (cat_summary['Gross_Profit'] / cat_summary['Net_Sales']) * 100
    cat_summary = cat_summary.sort_values('Net_Sales', ascending=False)
    
    fig, ax1 = plt.subplots(figsize=(10, 5))
    ax2 = ax1.twinx()
    bars = ax1.bar(cat_summary['Category'], cat_summary['Net_Sales']/1e5, color=BLUE, alpha=0.85)
    line = ax2.plot(cat_summary['Category'], cat_summary['Margin_%'], color=CORAL, marker='o', linewidth=2.5)
    ax1.set_ylabel('Net Sales (₹ Lakhs)', fontsize=10)
    ax2.set_ylabel('Gross Margin (%)', fontsize=10, color=CORAL)
    ax1.set_xticklabels(cat_summary['Category'], rotation=45, ha='right', fontsize=9)
    plt.title('Category Performance: Net Sales vs. Gross Margin %', fontsize=12, fontweight='bold', pad=15)
    plt.tight_layout()
    plt.savefig(os.path.join(CHARTS_DIR, "category_sales_margin.png"), dpi=300)
    plt.close()
    
    print("KPIs and charts exported successfully to reports/")

if __name__ == "__main__":
    compute_kpis()
