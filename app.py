import streamlit as st
import pandas as pd
import json

# Load JSON data
with open("artsy_net_sample.json", "r") as file:
    data = json.load(file)

# Extract auction data and artist details
all_auctions = []
for artist in data:
    for auction in artist["auctions"]:
        auction["artist_name"] = artist["name"]
        auction["bio"] = artist["bio"]
        auction["cv_url"] = artist["cv"]["url"] if "cv" in artist and "url" in artist["cv"] else None
        auction["artist_url"] = artist["url"]
        all_auctions.append(auction)
df = pd.DataFrame(all_auctions)

# Title
st.title("Art Auction Data Viewer")

# Sidebar filters
st.sidebar.header("Filters")
selected_artist = st.sidebar.multiselect("Select Artist(s)", df["artist_name"].unique())
selected_organization = st.sidebar.multiselect("Select Organization(s)", df["organization"].unique())
selected_category = st.sidebar.multiselect("Select Category(s)", df["category_text"].dropna().unique())

# Filter the data
if selected_artist:
    df = df[df["artist_name"].isin(selected_artist)]
if selected_organization:
    df = df[df["organization"].isin(selected_organization)]
if selected_category:
    df = df[df["category_text"].isin(selected_category)]

# Display data in a table
st.dataframe(df[["artist_name", "title", "organization", "medium_text", "category_text", "date_text", "sale_date", "estimate", "price_realized_display"]])

# Click to view full details
st.subheader("Artwork Details")
artwork_index = st.selectbox("Select an artwork to view full details:", df.index)
selected_data = df.loc[artwork_index]
st.write(selected_data[["artist_name", "title", "organization", "medium_text", "category_text", "date_text", "sale_date", "estimate", "price_realized_display"]])
st.subheader("Artist Details")
st.write("Name:", selected_data["artist_name"])
st.write("Bio:", selected_data["bio"])
st.write("Artist URL:", selected_data["artist_url"])
st.write("CV:", selected_data["cv_url"])
