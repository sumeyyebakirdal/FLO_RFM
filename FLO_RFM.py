###############################################################
# Customer Segmentation with RFM
###############################################################

###############################################################
# Business Problem
###############################################################
# FLO wants to segment its customers and determine marketing strategies according to these segments.
# To this end, customer behaviors will be defined and groups will be formed based on these behavior clusters.

###############################################################
# Dataset Story
###############################################################

# The dataset consists of information obtained from the past shopping behaviors of customers 
# who made their last purchases as OmniChannel (both online and offline) in 2020 - 2021.

# master_id: Unique customer identifier
# order_channel: Which channel was used for the shopping platform (Android, iOS, Desktop, Mobile, Offline)
# last_order_channel: The channel where the last purchase was made
# first_order_date: Date of the customer's first purchase
# last_order_date: Date of the customer's last purchase
# last_order_date_online: Date of the customer's last purchase on the online platform
# last_order_date_offline: Date of the customer's last purchase on the offline platform
# order_num_total_ever_online: Total number of purchases made by the customer on the online platform
# order_num_total_ever_offline: Total number of purchases made by the customer offline
# customer_value_total_ever_offline: Total fees paid by the customer for offline purchases
# customer_value_total_ever_online: Total fees paid by the customer for online purchases
# interested_in_categories_12: List of categories the customer has shopped in the last 12 months

###############################################################
# TASKS
###############################################################

# TASK 1: Data Understanding and Preparation
           # 1. Read the flo_data_20K.csv data.
           # 2. In the dataset, examine:
                     # a. First 10 observations,
                     # b. Variable names,
                     # c. Descriptive statistics,
                     # d. Null values,
                     # e. Variable types.
           # 3. Omnichannel implies customers shop from both online and offline platforms. Create new variables 
           # for each customer's total number of purchases and total spending.
           # 4. Examine variable types. Convert date-related variables to date type.
           # 5. Look at the distribution of the number of customers in shopping channels, average number of products purchased, and average spending.
           # 6. Rank the top 10 customers bringing in the most revenue.
           # 7. Rank the top 10 customers with the most orders.
           # 8. Functionalize the data preparation process.

# TASK 2: Calculating RFM Metrics

# TASK 3: Calculating RF and RFM Scores

# TASK 4: Defining RF Scores as Segments

# TASK 5: Time for Action!
           # 1. Examine the recency, frequency, and monetary averages of the segments.
           # 2. Using RFM analysis, find customers for 2 specific cases and save their IDs to CSV files.
                   # a. FLO is adding a new women's shoe brand. The products are above general price preferences. 
                   # Therefore, they want to contact customers who would be interested. Target: Loyal customers (champions, loyal_customers) 
                   # who spent over 250 TL on average and shopped in the "WOMEN" category. Save to 'yeni_marka_hedef_müşteri_id.csv'.
                   # b. A 40% discount is planned for Men's and Children's products. Target: Past good customers who haven't shopped 
                   # in a long time (cant_loose, hibernating) and new customers. Save to 'indirim_hedef_müşteri_ids.csv'.

# TASK 6: Functionalize the entire process.

###############################################################
# TASK 1: Data Understanding and Preparation
###############################################################

import pandas as pd
import datetime as dt
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
pd.set_option('display.float_format', lambda x: '%.2f' % x)
pd.set_option('display.width',1000)

# 1. Read the data and create a copy.
df_ = pd.read_csv("Modül_2_CRM_Analitigi/Dataset/flo_data_20K.csv")
df = df_.copy()
df.head()

# 2. Data Exploration
        # a. First 10 observations
        # b. Variable names
        # c. Shape
        # d. Descriptive stats
        # e. Null values
        # f. Variable types

df.head(10)
df.columns
df.shape
df.describe().T
df.isnull().sum()
df.info()

# 3. Create total order and total value variables for Omnichannel customers.
df["order_num_total"] = df["order_num_total_ever_online"] + df["order_num_total_ever_offline"]
df["customer_value_total"] = df["customer_value_total_ever_offline"] + df["customer_value_total_ever_online"]

# 4. Convert date variables to datetime type.
date_columns = df.columns[df.columns.str.contains("date")]
df[date_columns] = df[date_columns].apply(pd.to_datetime)
df.info()

# 5. Distribution of customer count, total products, and total spending across channels.
df.groupby("order_channel").agg({"master_id":"count",
                                 "order_num_total":"sum",
                                 "customer_value_total":"sum"})

# 6. Top 10 revenue-generating customers.
df.sort_values("customer_value_total", ascending=False)[:10]

# 7. Top 10 customers by order count.
df.sort_values("order_num_total", ascending=False)[:10]

# 8. Functionalizing data prep.
def data_prep(dataframe):
    dataframe["order_num_total"] = dataframe["order_num_total_ever_online"] + dataframe["order_num_total_ever_offline"]
    dataframe["customer_value_total"] = dataframe["customer_value_total_ever_offline"] + dataframe["customer_value_total_ever_online"]
    date_columns = dataframe.columns[dataframe.columns.str.contains("date")]
    dataframe[date_columns] = dataframe[date_columns].apply(pd.to_datetime)
    return df

###############################################################
# TASK 2: Calculating RFM Metrics
###############################################################

# Set analysis date to 2 days after the last purchase date in the set.
df["last_order_date"].max() # 2021-05-30
analysis_date = dt.datetime(2021,6,1)

# Create new rfm dataframe with recency, frequency and monetary.
rfm = pd.DataFrame()
rfm["customer_id"] = df["master_id"]
rfm["recency"] = (analysis_date - df["last_order_date"]).astype('timedelta64[D]')
rfm["frequency"] = df["order_num_total"]
rfm["monetary"] = df["customer_value_total"]

rfm.head()

###############################################################
# TASK 3: Calculating RF and RFM Scores
###############################################################

# Convert metrics to 1-5 scores using qcut.
rfm["recency_score"] = pd.qcut(rfm['recency'], 5, labels=[5, 4, 3, 2, 1])
rfm["frequency_score"] = pd.qcut(rfm['frequency'].rank(method="first"), 5, labels=[1, 2, 3, 4, 5])
rfm["monetary_score"] = pd.qcut(rfm['monetary'], 5, labels=[1, 2, 3, 4, 5])

rfm.head()

# Create RF_SCORE.
rfm["RF_SCORE"] = (rfm['recency_score'].astype(str) + rfm['frequency_score'].astype(str))

# Create RFM_SCORE.
rfm["RFM_SCORE"] = (rfm['recency_score'].astype(str) + rfm['frequency_score'].astype(str) + rfm['monetary_score'].astype(str))

rfm.head()

###############################################################
# TASK 4: Defining RF Scores as Segments
###############################################################

# Segment mapping for interpretability.
seg_map = {
    r'[1-2][1-2]': 'hibernating',
    r'[1-2][3-4]': 'at_Risk',
    r'[1-2]5': 'cant_loose',
    r'3[1-2]': 'about_to_sleep',
    r'33': 'need_attention',
    r'[3-4][4-5]': 'loyal_customers',
    r'41': 'promising',
    r'51': 'new_customers',
    r'[4-5][2-3]': 'potential_loyalists',
    r'5[4-5]': 'champions'
}

rfm['segment'] = rfm['RF_SCORE'].replace(seg_map, regex=True)

rfm.head()

###############################################################
# TASK 5: Time for Action!
###############################################################

# 1. Examine segment averages.
rfm[["segment", "recency", "frequency", "monetary"]].groupby("segment").agg(["mean", "count"])

# 2. Case studies for business actions.

# Case A: Target customers for the new premium women's brand.
target_segments_customer_ids = rfm[rfm["segment"].isin(["champions","loyal_customers"])]["customer_id"]
cust_ids = df[(df["master_id"].isin(target_segments_customer_ids)) &(df["interested_in_categories_12"].str.contains("KADIN"))]["master_id"]
cust_ids.to_csv("yeni_marka_hedef_müşteri_id.csv", index=False)
cust_ids.shape

# Case B: Target customers for the 40% discount on Men's and Children's categories.
target_segments_customer_ids = rfm[rfm["segment"].isin(["cant_loose","hibernating","new_customers"])]["customer_id"]
cust_ids = df[(df["master_id"].isin(target_segments_customer_ids)) & ((df["interested_in_categories_12"].str.contains("ERKEK"))|(df["interested_in_categories_12"].str.contains("COCUK")))]["master_id"]
cust_ids.to_csv("indirim_hedef_müşteri_ids.csv", index=False)

###############################################################
# BONUS: Functionalize the Whole Process
###############################################################

def create_rfm(dataframe):
    # Data Prep
    dataframe["order_num_total"] = dataframe["order_num_total_ever_online"] + dataframe["order_num_total_ever_offline"]
    dataframe["customer_value_total"] = dataframe["customer_value_total_ever_offline"] + dataframe["customer_value_total_ever_online"]
    date_columns = dataframe.columns[dataframe.columns.str.contains("date")]
    dataframe[date_columns] = dataframe[date_columns].apply(pd.to_datetime)

    # Calculating RFM Metrics
    analysis_date = dt.datetime(2021, 6, 1)
    rfm = pd.DataFrame()
    rfm["customer_id"] = dataframe["master_id"]
    rfm["recency"] = (analysis_date - dataframe["last_order_date"]).astype('timedelta64[D]')
    rfm["frequency"] = dataframe["order_num_total"]
    rfm["monetary"] = dataframe["customer_value_total"]

    # Calculating Scores
    rfm["recency_score"] = pd.qcut(rfm['recency'], 5, labels=[5, 4, 3, 2, 1])
    rfm["frequency_score"] = pd.qcut(rfm['frequency'].rank(method="first"), 5, labels=[1, 2, 3, 4, 5])
    rfm["monetary_score"] = pd.qcut(rfm['monetary'], 5, labels=[1, 2, 3, 4, 5])
    rfm["RF_SCORE"] = (rfm['recency_score'].astype(str) + rfm['frequency_score'].astype(str))
    rfm["RFM_SCORE"] = (rfm['recency_score'].astype(str) + rfm['frequency_score'].astype(str) + rfm['monetary_score'].astype(str))

    # Segment Mapping
    seg_map = {
        r'[1-2][1-2]': 'hibernating',
        r'[1-2][3-4]': 'at_Risk',
        r'[1-2]5': 'cant_loose',
        r'3[1-2]': 'about_to_sleep',
        r'33': 'need_attention',
        r'[3-4][4-5]': 'loyal_customers',
        r'41': 'promising',
        r'51': 'new_customers',
        r'[4-5][2-3]': 'potential_loyalists',
        r'5[4-5]': 'champions'
    }
    rfm['segment'] = rfm['RF_SCORE'].replace(seg_map, regex=True)

    return rfm[["customer_id", "recency","frequency","monetary","RF_SCORE","RFM_SCORE","segment"]]

rfm_df = create_rfm(df)