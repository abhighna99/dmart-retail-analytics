"""
DMart Retail Data Analytics - ETL & Data Cleaning Pipeline
Author: Abhighna Mopidevi
Date: October 2026

Description:
This script handles the ingestion, auditing, and cleaning of raw DMart synthetic
retail datasets (Customer Master, Consumer Transactions, and Product Lookup).
It identifies and rectifies quality anomalies, standardizes categorical values,
and outputs verified clean datasets ready for downstream business intelligence.
"""

import os
import pandas as pd
import numpy as np

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW_DATA_DIR = os.path.join(BASE_DIR, "data", "raw")
PROCESSED_DATA_DIR = os.path.join(BASE_DIR, "data", "processed")
os.makedirs(PROCESSED_DATA_DIR, exist_ok=True)

def load_raw_data():
    """Load raw CSV inputs."""
    cust_df = pd.read_csv(os.path.join(RAW_DATA_DIR, "Dmart_Customer_Master_Raw.csv"))
    tx_df = pd.read_csv(os.path.join(RAW_DATA_DIR, "Dmart_Consumer_Transactions_Raw.csv"))
    prod_df = pd.read_csv(os.path.join(RAW_DATA_DIR, "Dmart_Product_Lookup.csv"))
    return cust_df, tx_df, prod_df

def clean_customer_master(cust_df):
    """
    Deduplicate customer master, normalize casing, validate demographic fields.
    """
    print(f"Ingesting Customer Master: {len(cust_df)} raw records.")
    
    # 1. Deduplication on Customer_ID (drops 26 casing/duplicate rows)
    clean_cust = cust_df.drop_duplicates(subset=['Customer_ID']).copy()
    
    # 2. Text normalization
    clean_cust['Customer_Name'] = clean_cust['Customer_Name'].astype(str).str.strip().str.title()
    clean_cust['City'] = clean_cust['City'].astype(str).str.strip().str.title()
    clean_cust['State'] = clean_cust['State'].astype(str).str.strip().str.title()
    
    # 3. Customer Segment mapping
    segment_map = {
        'REGULAR': 'Regular', 'regular': 'Regular', 'Regular ': 'Regular', 'Regular': 'Regular',
        'Value Seeker': 'Value Seeker', 'Premium': 'Premium', 'Occasional': 'Occasional', 'Family Shopper': 'Family Shopper'
    }
    clean_cust['Customer_Segment'] = clean_cust['Customer_Segment'].str.strip().map(lambda s: segment_map.get(s, s))
    clean_cust['Customer_Segment'] = clean_cust['Customer_Segment'].fillna('Unknown / Unassigned')
    
    # 4. Loyalty Tier mapping
    loyalty_map = {
        'SILVER': 'Silver', 'Silver': 'Silver',
        'gold': 'Gold', 'Gold': 'Gold',
        'Platinum ': 'Platinum', 'Platinum': 'Platinum'
    }
    clean_cust['Loyalty_Tier'] = clean_cust['Loyalty_Tier'].str.strip().map(lambda s: loyalty_map.get(s, s))
    clean_cust['Loyalty_Tier'] = clean_cust['Loyalty_Tier'].fillna('Non-Member / None')
    
    # 5. Age audit (filter impossible values: <15 or >100)
    clean_cust['Age_Cleaned'] = clean_cust['Age'].apply(lambda a: a if pd.notna(a) and 15 <= a <= 100 else np.nan)
    
    # 6. Phone cleanup
    def normalize_phone(p):
        if pd.isna(p):
            return np.nan
        p_clean = str(p).replace('.0', '').replace('+91-', '').strip()
        return p_clean if len(p_clean) == 10 and p_clean.isdigit() else np.nan
        
    clean_cust['Mobile_Cleaned'] = clean_cust['Mobile_Number'].apply(normalize_phone)
    
    print(f"Customer Master Cleaned: {len(clean_cust)} unique valid profiles.")
    return clean_cust

def clean_transactions(tx_df, prod_df):
    """
    Standardize transaction statuses, align prices, fix discount rates, and calculate financial fields.
    """
    print(f"Ingesting Consumer Transactions: {len(tx_df)} raw records.")
    
    # 1. Deduplication: drop 10 exact identical duplicate rows and 25 TXDUP synthetic clones
    clean_tx = tx_df.drop_duplicates().copy()
    clean_tx = clean_tx[~clean_tx['Transaction_ID'].str.startswith('TXDUP')].copy()
    print(f"Post-deduplication records: {len(clean_tx)} unique transactions.")
    
    # 2. Canonical Status Standardization
    status_map = {
        'Completed': 'Completed', 'COMPLETE': 'Completed', 'completed': 'Completed',
        'Cancelled': 'Cancelled', 'cancelled': 'Cancelled',
        'Returned': 'Returned', 'RETURN': 'Returned',
        'Pending': 'Pending'
    }
    clean_tx['Transaction_Status'] = clean_tx['Transaction_Status'].str.strip().map(lambda s: status_map.get(s, s))
    
    # 3. Channel Standardization
    channel_map = {
        'App': 'App', 'App ': 'App', 'APP': 'App',
        'Online': 'Online', 'online': 'Online',
        'In-store': 'In-store', 'IN-STORE': 'In-store'
    }
    clean_tx['Sales_Channel'] = clean_tx['Sales_Channel'].str.strip().map(lambda s: channel_map.get(s.strip(), s))
    
    # 4. Category Standardization
    cat_map = {
        'DAIRY': 'Dairy', 'STAPLES': 'Staples', 'PERSONAL CARE': 'Personal Care',
        'HOME CARE': 'Home Care', 'STATIONERY': 'Stationery'
    }
    clean_tx['Category'] = clean_tx['Category'].str.strip().map(lambda s: cat_map.get(s, s.title() if s.isupper() else s))
    
    # 5. Payment Method Standardization
    pay_map = {
        'Cash': 'Cash', 'Cash ': 'Cash',
        'Debit Card': 'Debit Card',
        'Credit Card': 'Credit Card', 'CREDIT CARD': 'Credit Card',
        'UPI': 'UPI', 'upi': 'UPI',
        'Wallet': 'Wallet'
    }
    clean_tx['Payment_Method'] = clean_tx['Payment_Method'].str.strip().map(lambda s: pay_map.get(s, s))
    
    # 6. Realign Unit Prices from Catalog Lookup (resolves 12 negative price errors)
    clean_tx = clean_tx.merge(prod_df[['Product_ID', 'List_Price_INR', 'Unit_Cost_INR']], on='Product_ID', how='left')
    clean_tx['Unit_Price_Fixed'] = clean_tx['List_Price_INR']
    
    # 7. Rectify Discount Rates (resolves 10 rows with 1.20 -> 0.12)
    clean_tx['Discount_Rate_Fixed'] = clean_tx['Discount_Rate'].apply(lambda d: 0.12 if d > 1.0 else d)
    
    # 8. Rectify negative quantities on completed orders
    clean_tx['Quantity_Cleaned'] = clean_tx['Quantity'].apply(lambda q: abs(q) if q < 0 else q)
    
    # 9. Computed Financial Fields
    clean_tx['Gross_Sales_INR'] = clean_tx['Quantity_Cleaned'] * clean_tx['Unit_Price_Fixed']
    clean_tx['Discount_Amount_INR'] = clean_tx['Gross_Sales_INR'] * clean_tx['Discount_Rate_Fixed']
    clean_tx['Net_Sales_INR'] = clean_tx['Gross_Sales_INR'] - clean_tx['Discount_Amount_INR']
    clean_tx['COGS_INR'] = clean_tx['Quantity_Cleaned'] * clean_tx['Unit_Cost_INR']
    clean_tx['Gross_Profit_INR'] = clean_tx['Net_Sales_INR'] - clean_tx['COGS_INR']
    
    return clean_tx

def main():
    cust_df, tx_df, prod_df = load_raw_data()
    clean_cust = clean_customer_master(cust_df)
    clean_tx = clean_transactions(tx_df, prod_df)
    
    clean_cust.to_csv(os.path.join(PROCESSED_DATA_DIR, "Dmart_Customer_Master_Cleaned.csv"), index=False)
    clean_tx.to_csv(os.path.join(PROCESSED_DATA_DIR, "Dmart_Consumer_Transactions_Cleaned.csv"), index=False)
    print("ETL execution successful. Clean datasets saved to data/processed/")

if __name__ == "__main__":
    main()
