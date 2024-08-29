import streamlit as st
import pandas as pd

# Load the Excel file with multiple sheets
data_file = 'data.xlsx'

# Load relevant sheets into DataFrames
products_df = pd.read_excel(data_file, sheet_name=0)
similar_products_df = pd.read_excel(data_file, sheet_name=1)
user_similarity_df = pd.read_excel(data_file, sheet_name=2)

# Page configuration
st.set_page_config(page_title="E-Commerce Demo", layout="wide")

# Title
st.title("E-Commerce Demo with Recommendations")

# Sidebar for browsing products
st.sidebar.header("Browse Products")
subcategories = products_df['category'].unique()
selected_subcategory = st.sidebar.selectbox("Select a Subcategory", subcategories)

# Filter products based on the selected subcategory
filtered_df = products_df[products_df['category'] == selected_subcategory]

# Display search box
search_query = st.sidebar.text_input("Or search for a product")

# Filter based on search query
if search_query:
    filtered_df = filtered_df[filtered_df['ProdName'].str.contains(search_query, case=False)]

# Display product list
if not filtered_df.empty:
    selected_product = st.selectbox("Select a Product", filtered_df['ProdName'].unique())
else:
    st.write("No products found.")
    selected_product = None

# Display selected product details and recommendations
if selected_product:
    product_details = filtered_df[filtered_df['ProdName'] == selected_product].iloc[0]
    
    st.header(f"Selected Product: {selected_product}")
    st.write(f"**Category:** {product_details['category']}")
    st.write(f"**Discounted Price:** ${product_details['DPrice']}")
    st.write(f"**Actual Price:** ${product_details['APrice']}")
    st.write(f"**Discount Percentage:** {product_details['DPerct']}%")
    st.write(f"**Rating:** {product_details['rating']}/5")
    st.write(f"**Description:** {product_details['ProdDescr']}")
    
    # Display product image if available
    if product_details['img_link']:
        st.image(product_details['img_link'], caption=selected_product)

    # Recommendations Section
    st.subheader("Recommended Products")

    # Similar products based on product features
    st.markdown("### Similar Products")
    similar_products = similar_products_df[similar_products_df['searchedProd'] == selected_product]
    if not similar_products.empty:
        for _, row in similar_products.iterrows():
            st.write(f"- {row['SuggProdNames']} (Similarity Score: {row['Similarity_Score']})")
    else:
        st.write("No similar products found.")
    
    # Products often bought by similar users
    st.markdown("### Products Bought by Similar Users")
    similar_user_products = user_similarity_df[user_similarity_df['ProdName'] == selected_product]
    if not similar_user_products.empty:
        for _, row in similar_user_products.iterrows():
            st.write(f"- {row['ProdName']} (Bought by similar users)")
    else:
        st.write("No products bought by similar users found.")
