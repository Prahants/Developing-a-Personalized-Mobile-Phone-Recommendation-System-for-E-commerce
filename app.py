import streamlit as st
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder

# Load and prepare the data
data = pd.read_csv("flipkart Mobiles.csv")

# Combine relevant columns to form descriptions
data["Description"] = data[
    ["Storage", "Cameras", "screen_size", "Battery", "processor"]
].apply(lambda x: " ".join(x.dropna().astype(str)), axis=1)

# Convert price to numeric by removing any non-numeric characters
data["price"] = data["price"].replace("[\₹,]", "", regex=True).astype(float)

# Handle missing values
data = data.dropna(subset=["Title", "price", "Description"])

# Ensure all text data is in string format
data["Description"] = data["Description"].astype(str)

# Filter out rows with empty strings in 'Description'
data = data[data["Description"].str.strip() != ""]


# Define a function to clean text
def clean_text(text):
    text = text.lower()  # Convert to lowercase
    text = "".join(
        [char for char in text if char.isalnum() or char.isspace()]
    )  # Remove non-alphanumeric characters
    return text


# Apply the cleaning function
data["Description"] = data["Description"].apply(clean_text)


# Ensure there are no rows with just stop words
def is_meaningful(text):
    # Simple check: text length greater than a threshold (e.g., 3 words)
    return len(text.split()) > 3


data = data[data["Description"].apply(is_meaningful)]

# Encoding categorical features
label_encoder = LabelEncoder()
data["Title"] = label_encoder.fit_transform(data["Title"])

# Vectorizing text data
tfidf_vectorizer = TfidfVectorizer(max_features=500, stop_words="english")
description_tfidf = tfidf_vectorizer.fit_transform(data["Description"])

# Combine all features into a single DataFrame
description_df = pd.DataFrame(
    description_tfidf.toarray(),
    columns=[f"desc_{i}" for i in range(description_tfidf.shape[1])],
)
features = pd.concat([data[["Title", "price"]], description_df], axis=1)

# Define target variable (for demonstration, we'll assume a dummy target variable)
data["Target"] = (data["price"] > data["price"].mean()).astype(
    int
)  # Example target variable
target = data["Target"]

# Train the Random Forest model
rf_model = RandomForestClassifier(n_estimators=100, random_state=42)
rf_model.fit(features, target)

# Streamlit app
st.title("Mobile Phone Recommendation System")

st.write(
    """
## Enter your budget to get recommendations:
"""
)

min_price = st.number_input("Enter minimum price:", min_value=0.0, step=0.01)
max_price = st.number_input("Enter maximum price:", min_value=0.0, step=0.01)

if st.button("Get Recommendations"):
    if min_price < max_price:
        # Filter products based on the price range
        recommended_products = data[
            (data["price"] >= min_price) & (data["price"] <= max_price)
        ]

        if not recommended_products.empty:
            st.success("We recommend the following phones within your budget:")
            for index, row in recommended_products.iterrows():
                st.write(
                    f"**Product Name:** {label_encoder.inverse_transform([row['Title']])[0]}"
                )
                st.write(f"Price: ₹{row['price']}")
                st.write(f"Description: {row['Description']}")
                st.write("---")
        else:
            st.error("No products found within your budget.")
    else:
        st.error("Please ensure the minimum price is less than the maximum price.")
