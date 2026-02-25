# FLO Customer Segmentation with RFM Analysis

![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![Pandas](https://img.shields.io/badge/pandas-v1.3+-green)
![CRM](https://img.shields.io/badge/Focus-CRM_Analytics-orange)

## 📌 Business Problem
FLO, a leading retail company, aims to segment its customers to develop targeted marketing strategies. By analyzing customer behavior patterns, the company intends to create groups based on these clusters and engage with customers through personalized campaigns.

---

## 📂 Dataset Story
The dataset is based on the past shopping behaviors of customers who made their last purchases in 2020-2021 as **OmniChannel** (both online and offline) shoppers.

* **Dataset Source:** [Kaggle - FLO Data 20K](https://www.kaggle.com/datasets/emrebilir/flo-data-20k-csv)
* **Total Observations:** 19,945
* **Total Variables:** 12

### Key Features:
| Feature | Description |
| :--- | :--- |
| **master_id** | Unique customer identifier |
| **order_channel** | Platform used for shopping (Android, iOS, Desktop, Mobile, Offline) |
| **last_order_date** | Date of the customer's most recent purchase |
| **order_num_total** | Total number of orders (Online + Offline) |
| **customer_value_total** | Total revenue generated (Online + Offline) |
| **interested_in_categories_12** | Categories the customer shopped in the last 12 months |

---

## 🛠️ Project Roadmap

### 1. Data Understanding & Preparation
* Explored descriptive statistics and variable types.
* Created new variables for **Omnichannel** shopping (Total Order & Total Value).
* Converted date-related columns to `datetime` objects.
* Analyzed distribution of spending across different channels.

### 2. Calculating RFM Metrics
Standardized the metrics for analysis:
* **Recency:** Days since the customer's last purchase (Analysis Date: 2021-06-01).
* **Frequency:** Total number of repeat purchases.
* **Monetary:** Total spending (Customer Value).

### 3. RFM Scoring & Segmentation
* Generated **RFM Scores** by dividing metrics into quintiles (1-5).
* Created an **RF_SCORE** to define segments.
* Mapped scores to 10 distinct segments (e.g., Champions, Hibernating, At Risk, Loyal Customers).



### 4. Actionable Business Cases
Two specific marketing scenarios were addressed:
* **Premium Women's Brand Launch:** Identified "Champions" and "Loyal Customers" who shop in the "WOMEN" category for exclusive outreach.
* **Category Specific Discounts:** Targeted "At Risk," "Hibernating," and "New Customers" interested in Men's and Children's categories for a 40% discount campaign.

---
