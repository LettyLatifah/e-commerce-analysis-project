import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency
sns.set(style='dark')

# helper function untuk menyiapkan dataframe
def create_product_sum_order_df(df):
  product_sum_order_df = df.groupby("product_category_name_english").order_id.nunique().sort_values(ascending=False).reset_index()
  product_sum_order_df.columns = ["product_category", "sum_order"]

  return product_sum_order_df

def create_product_review_df(df):
  product_review_df = df.groupby("product_category_name_english").agg({
    "review_id": "nunique",
    "review_score": "mean"
  }).reset_index()
  product_review_df.rename(columns={
    "product_category_name_english": "product_category",
    "review_id": "sum_review",
    "review_score": "review_score_avg"
  }, inplace=True)

  product_review_df.sort_values(by="review_score_avg", ascending=False)

  return product_review_df

# memproses data yang telah dibersihkan
all_df = pd.read_csv("all_data.csv")

datetime_columns = [
  "review_creation_date",
  "review_answer_timestamp",
  "shipping_limit_date"
]

all_df.sort_values(by="review_creation_date", inplace=True)
all_df.reset_index(inplace=True)

for column in datetime_columns:
  all_df[column] = pd.to_datetime(all_df[column])

# filter data
min_date = all_df["review_creation_date"].min()
max_date = all_df["review_creation_date"].max()

# menyiapkan sidebar
with st.sidebar:
  # menambahkan logo olist
  st.image("olist.png")

  # mengambil start_date dan end_date dari input
  start_date, end_date = st.date_input(
    label="Rentang Waktu",
    min_value=min_date,
    max_value=max_date,
    value=[min_date, max_date],
  )

main_df = all_df[(all_df["review_creation_date"] >= str(start_date)) & 
                (all_df["review_creation_date"] <= str(end_date))]

# # menyiapkan dataframe
product_sum_order_df = create_product_sum_order_df(main_df)
product_review_df = create_product_review_df(main_df)

# membuat header pada dashboard
st.header("Olist E-Commerce Product Review Dashboard")

# membuat visualisasi data jumlah produk terjual
st.subheader("Best and Worst Performing Product Categorized by Number of Order")

fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(24, 6))

colors = ["#0C28CE", "#B6BBC4", "#B6BBC4", "#B6BBC4", "#B6BBC4"]

sns.barplot(x="sum_order", y="product_category", data=product_sum_order_df.head(5), palette=colors, ax=ax[0])
ax[0].set_ylabel(None)
ax[0].set_xlabel(None)
ax[0].set_title("Best Performing Product", loc="center", fontsize=18)
ax[0].tick_params(axis ='y', labelsize=15)

sns.barplot(x="sum_order", y="product_category", data=product_sum_order_df.sort_values(by="sum_order", ascending=True).head(5), palette=colors, ax=ax[1])
ax[1].set_ylabel(None)
ax[1].set_xlabel(None)
ax[1].invert_xaxis()
ax[1].yaxis.set_label_position("right")
ax[1].yaxis.tick_right()
ax[1].set_title("Worst Performing Product", loc="center", fontsize=18)
ax[1].tick_params(axis='y', labelsize=15)

st.pyplot(fig)

# membuat visualisasi data peringkat review score produk
st.subheader("Highest and Lowest Review Score Product")

col1, col2 = st.columns(2)

with col1:
    st.metric("Highest Review", "cds_dvds_musicals" )
 
with col2:
    st.metric("Lowest Review", "security_and_services" )
 

fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(24, 6))

colors = ["#0C28CE", "#B6BBC4", "#B6BBC4", "#B6BBC4", "#B6BBC4"]

sns.barplot(x="review_score_avg", y="product_category", data=product_review_df.sort_values(by="review_score_avg", ascending=False).head(5), palette=colors, ax=ax[0])
ax[0].set_ylabel(None)
ax[0].set_xlabel(None)
ax[0].set_title("Best Performing Product", loc="center", fontsize=18)
ax[0].tick_params(axis ='y', labelsize=15)

sns.barplot(x="review_score_avg", y="product_category", data=product_review_df.sort_values(by="review_score_avg", ascending=True).head(5), palette=colors, ax=ax[1])
ax[1].set_ylabel(None)
ax[1].set_xlabel(None)
ax[1].invert_xaxis()
ax[1].yaxis.set_label_position("right")
ax[1].yaxis.tick_right()
ax[1].set_title("Worst Performing Product", loc="center", fontsize=18)
ax[1].tick_params(axis='y', labelsize=15)

st.pyplot(fig)
