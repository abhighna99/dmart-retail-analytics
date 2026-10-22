# DMart Retail Analytics — Performance Analysis & Strategic Roadmap

**Author:** Abhighna Mopidevi  
**Role:** Data Analyst Case Study & Technical Assessment  
**Evaluation Scope:** 15,000 Retail Transactions | 3,200 Customers | 20 Products Across 10 Categories (Jan 2025 – Oct 2026)  

---

## 📌 Project Overview & Executive Summary

This project presents an end-to-end retail business intelligence and performance analysis conducted on operational datasets from **DMart**. The objective of the analysis is to evaluate sales performance, customer cohort economics, and omnichannel fulfillment friction, derive actionable Key Performance Indicators (KPIs), and present a strategic merchandising and retention roadmap.

The project encompasses:
1. **Data Auditing & ETL:** Identification and remediation of deliberately injected data quality anomalies (duplicates, negative prices, decimal errors, impossible dates).
2. **Financial & Operational Analytics:** Derivation of core retail KPIs (Net Sales, COGS, Gross Margin %, ABV, ASP, UPT, ARPU, Cancellation & Return rates).
3. **Omnichannel & Category Deep-Dives:** Granular analysis across 10 product categories, 3 sales channels (In-store, App, Online), 5 payment methods, and 30 retail store locations.
4. **Interactive Executive Dashboard:** A standalone, responsive web dashboard built with Tailwind CSS and Chart.js for executive exploration.

---

## 🎯 Executive KPI Summary

| Metric | Calculated Value | Formula & Business Rationale |
| :--- | :---: | :--- |
| **Gross Sales** | **₹25,88,674.00** | $\sum (\text{Quantity} \times \text{List Price})$ across completed orders |
| **Total Discounts** | **₹1,38,047.08** | $\sum (\text{Gross Sales} \times \text{Discount Rate})$ (5.33% effective discount rate) |
| **Realized Net Sales** | **₹24,50,626.92** | $\text{Gross Sales} - \text{Total Discounts}$ |
| **Cost of Goods Sold (COGS)** | **₹18,34,429.00** | $\sum (\text{Quantity} \times \text{Unit Cost})$ across 20 SKUs |
| **Gross Profit** | **₹6,16,197.92** | $\text{Net Sales} - \text{COGS}$ |
| **Gross Margin (%)** | **25.14%** | $(\text{Gross Profit} / \text{Net Sales}) \times 100$ |
| **Completed Orders** | **13,602** | Orders with verified canonical status `'Completed'` |
| **Total Units Sold** | **20,513** | Units fulfilled |
| **Average Basket Value (ABV)** | **₹180.17** | $\text{Net Sales} / \text{Completed Orders}$ |
| **Average Selling Price (ASP)** | **₹119.47** | $\text{Net Sales} / \text{Units Sold}$ |
| **Units Per Transaction (UPT)** | **1.51** | $\text{Units Sold} / \text{Completed Orders}$ |
| **Active Customers** | **3,150** | Distinct transacting customers (98.4% activity rate) |
| **ARPU** | **₹777.98** | $\text{Net Sales} / \text{Active Customers}$ |
| **Fulfillment Funnel** | **90.68% Completed** | 4.02% Cancelled (₹1.14L lost) \| 3.29% Returned (₹82.3k reversed) |

---

## 🔍 Data Quality Audit & Integrity Remediation

Raw input datasets were subjected to rigorous audit before calculating business metrics:

- **Transaction Duplicates:** Removed **35 duplicate records** (10 exact row duplicates + 25 synthetic `TXDUP` clones) to establish a true baseline of **15,000 unique records**.
- **Negative Catalog Prices:** Identified 12 rows with negative unit prices (e.g., `-210`, `-180`). Realigned each to `List_Price_INR` from `Dmart_Product_Lookup.csv`.
- **Decimal Discount Errors:** Detected 10 rows with `Discount_Rate = 1.2` (120% discount). Corrected the data entry typo from 1.2 to 0.12 (12%).
- **Negative Quantities:** Rectified 13 negative quantity rows on completed receipts as POS scan sign glitches.
- **Categorical Standardization:** Normalized case and whitespace variants across status (`Completed`, `Cancelled`, `Returned`, `Pending`), channels (`App`, `Online`, `In-store`), and categories.
- **Customer Master Deduplication:** Deduplicated 26 redundant customer rows to confirm **3,200 unique customer accounts**. Filtered out biologically impossible ages (`-3`, `5`, `121`, `250`).

---

## 💡 Key Business Insights

1. **Staples Volume vs. Margin Divergence:**  
   Staples represent **30.9% of Net Sales** (₹7.57 Lakhs) but operate at the lowest gross margin (**19.23%**). Conversely, high-margin categories like Stationery (40.3%), Packaged Food (38.0%), and Bakery (36.9%) contribute under 3.5% of sales each.
2. **Mobile App Operational Efficiency:**  
   Sales are evenly split across App (34.2%), Online (33.0%), and In-store (32.8%). The **Mobile App delivers the highest ABV (₹183.33) and lowest return rate (2.97%)**, whereas Online web orders suffer from higher returns (3.51%) and cancellations (4.10%).
3. **Loyalty Program Inefficacy:**  
   Platinum members generate **₹773.51 in ARPU**, which is slightly below Non-Members (₹779.06) and virtually identical to Silver members (₹771.17). Current loyalty tiers do not offer spend-gated incentives, pointing to an urgent need for restructuring.

---

## 🚀 Strategic Recommendations

1. **Cross-Category Bundle Merchandising:** Pair low-margin staples with high-margin impulse items (e.g., *"Buy 5kg Rice, get 20% off Biscuits/Chocolates"*). Expected impact: **+12% to +15% expansion in ABV** and +180 bps in gross margin.
2. **Tier-Gated Loyalty Restructuring:** Establish explicit annual spending thresholds (e.g., ₹5,000 for Gold, ₹12,000 for Platinum) with high-value perks (free app delivery, weekend grocery discounts). Target: **+25% increase in Platinum spend**.
3. **App-First Digital Shift:** Migrate web traffic to the Mobile App via first-order app discounts, lowering return rates and saving over ₹40,000 in annual operational waste.
4. **Automated POS Constraints:** Implement database validations at POS checkout to block manual price overrides and discount inputs >20%.

---

## 📂 Repository Structure

```text
dmart-retail-analytics/
├── data/
│   ├── raw/                  # Original raw input datasets
│   └── processed/            # Cleaned, audited, and enriched datasets
├── src/
│   ├── etl_clean.py          # Data ingestion, audit, and cleaning script
│   └── analytics.py          # KPI calculation and chart generation engine
├── reports/
│   ├── DMart_Data_Analyst_Report.md   # Executive assessment report
│   ├── charts/               # High-resolution publication-grade visual charts
│   └── *.csv                 # Category, channel, store, and monthly summaries
├── dashboard/
│   └── index.html            # Interactive Tailwind + Chart.js visual dashboard
├── requirements.txt          # Python dependencies
└── README.md                 # Project documentation and summary
```

---

## 💻 Setup & Execution

### 1. Clone the Repository
```bash
git clone https://github.com/abhighna99/dmart-retail-analytics.git
cd dmart-retail-analytics
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Run Data Cleaning & Analytics Pipeline
```bash
python src/etl_clean.py
python src/analytics.py
```

### 4. View Interactive Dashboard
Open `dashboard/index.html` in any web browser:
```bash
start dashboard/index.html    # Windows
open dashboard/index.html     # macOS
```
