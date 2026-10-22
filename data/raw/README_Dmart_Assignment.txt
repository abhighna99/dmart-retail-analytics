DMART DATA ANALYST ASSIGNMENT — RAW DATA PACK

Purpose
This dataset is designed to assess a candidate with 1–2 years of Data Analyst experience. It is synthetic retail data and is not sourced from DMart or real consumers.

Main master workbook
Dmart_Raw_Master_Datasheets.xlsx
- Customer_Master_Raw: customer profile fields with deliberately introduced quality issues.
- Consumer_Transactions_Raw: retail transaction/product-line records with deliberately introduced quality issues.
- Product_Lookup: reference list of products, categories, list prices, and unit costs.

CSV files
- Dmart_Customer_Master_Raw.csv
- Dmart_Consumer_Transactions_Raw.csv
- Dmart_Product_Lookup.csv

Candidate instructions
Treat the files as raw input. Do not assume every row is valid. Identify, quantify, and document data-quality issues; standardise formats; assess duplicates; validate relationships between customers and transactions; derive suitable KPIs; and explain all assumptions. Keep raw data unchanged and create cleaned outputs separately.

Suggested analytical questions
- How many unique customers and transactions are represented after cleaning?
- What are sales, discounts, estimated gross profit, and average basket value?
- How do sales vary by month, store, category, channel, and payment method?
- Which customer segments and products contribute most to sales and profit?
- What patterns appear in cancellations and returns?
- Which KPIs would management monitor weekly and monthly?
- What limitations prevent reliable conclusions?

Important
- Customer names, emails, and phone numbers are randomly generated synthetic data.
- Transaction records represent product-line purchases, not necessarily unique bills. Candidates should establish the correct grain before calculating order-level KPIs.
- Discount_Rate is intended as a proportion (0.10 = 10%), but invalid values may be present.
- Validate whether a transaction status should be included in each KPI.
- Do not assume that marketing, customer and transaction records can be joined without validation.
