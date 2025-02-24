This Streamlit-based Python script fetches restaurant data from OpenStreetMap (OSM) and displays it on a web app with an enhanced UI. Users can view restaurant details, including randomly generated phone numbers and ratings, and download the data as a CSV file.

# 1️⃣ Prerequisites: Installing Required Libraries
Before running this script, you need to install the necessary Python libraries. Run the following command in the terminal or command prompt:
pip install streamlit pandas requests

## These libraries serve the following purposes:

Streamlit → Used for creating the interactive web application.
Pandas → Helps process and display data in tabular form.
Requests → Makes API calls to fetch data from OpenStreetMap.

# 2️⃣ How to Run the Script
Follow these steps to run the Streamlit web app:

Save the script as script.py in your desired project directory.

Navigate to the directory in your terminal or command prompt:

cd path/to/your/project
Run the Streamlit application using:

streamlit run script.py
Your browser will open automatically, and you will see the interactive web page.

# 3️⃣ Breakdown of the Code
🔹 Importing Required Modules

import requests
import pandas as pd
import streamlit as st
import random  

requests: Used to send HTTP requests to the Overpass API.
pandas: Helps in structuring and handling data in tabular form.
streamlit: Used to build the web interface.
random: Generates random ratings and phone numbers.

# 🔹 Overpass API Query for Fetching Restaurant Data
OVERPASS_URL = "http://overpass-api.de/api/interpreter"

QUERY = """
[out:json];
area[name="Toronto"]->.searchArea;
(
  node["amenity"="restaurant"](area.searchArea);
  way["amenity"="restaurant"](area.searchArea);
  relation["amenity"="restaurant"](area.searchArea);
);
out center;
"""
Overpass API is a tool that extracts specific data from OpenStreetMap.
The query requests all restaurants in Toronto using amenity="restaurant".
The out center; statement fetches geographical data (longitude/latitude).

# 🔹 Function to Generate Random Phone Numbers

def generate_random_phone_number(country="CA"):
    """Generate a random phone number based on country code."""
    country_codes = {
        "CA": "+1",
        "US": "+1",
        "IN": "+91",
        "UK": "+44",
        "AU": "+61"
    }
    
    code = country_codes.get(country, "+1")
    number = f"{code} {random.randint(600, 999)}-{random.randint(100, 999)}-{random.randint(1000, 9999)}"
    return number
    
A dictionary stores country dialing codes.
The function generates a random 10-digit phone number.
The format follows +CountryCode XXX-XXX-XXXX.

# 🔹 Function to Fetch Restaurant Data

def fetch_restaurant_data():
    """Fetch restaurant data from OpenStreetMap using Overpass API."""
    response = requests.get(OVERPASS_URL, params={"data": QUERY})
    
    if response.status_code == 200:
        return response.json()
    else:
        st.error(f"Error {response.status_code}: Unable to fetch data")
        return None
Sends a GET request to the Overpass API.
Returns JSON data containing restaurant details.
Displays an error message if the request fails.

# 🔹 Function to Process Restaurant Data

def process_data(osm_data):
    """Extract relevant details from OSM response and add random ratings and phone numbers."""
    restaurants = []

    for element in osm_data.get("elements", []):
        tags = element.get("tags", {})
        restaurants.append({
            "Name": tags.get("name", "Unknown"),
            "Cuisine": tags.get("cuisine", "Not specified"),
            "Address": tags.get("addr:street", "Unknown") + ", " + tags.get("addr:city", "Unknown"),
            "Phone": generate_random_phone_number("CA"),  
            "Rating": f"{round(random.uniform(1.0, 5.0), 1):.1f}"  # ✅ Ensures one decimal
        })
    
    return restaurants
Extracts restaurant name, cuisine, address.
Generates random phone numbers.
Assigns random restaurant ratings (between 1.0 - 5.0) with one decimal place.

# 4️⃣ The Streamlit Web App
🔹 Adding Custom CSS for Styling

st.markdown("""
    <style>
        body {
            background-color: #f5f5f5;
            font-family: 'Arial', sans-serif;
        }
        .main-title {
            font-size: 36px;
            font-weight: bold;
            text-align: center;
            color: white;
            padding: 20px;
            background: linear-gradient(90deg, #ff758c, #ff7eb3);
            border-radius: 10px;
            margin-bottom: 20px;
        }
        .custom-button {
            background-color: #ff4b5c;
            color: white;
            padding: 10px 20px;
            font-size: 18px;
            border-radius: 8px;
            border: none;
            cursor: pointer;
            transition: background 0.3s ease-in-out;
        }
        .custom-button:hover {
            background-color: #e84352;
        }
        .dataframe {
            background-color: white;
            padding: 15px;
            border-radius: 10px;
            box-shadow: 0px 0px 10px rgba(0,0,0,0.1);
        }
    </style>
""", unsafe_allow_html=True)
Uses CSS to enhance UI design.
Adds a gradient background to the title.
Styles buttons and data tables.

# 🔹 Creating the Streamlit Page

st.markdown("<div class='main-title'>🍽️ Restaurant Finder in Toronto</div>", unsafe_allow_html=True)
Displays a title with enhanced styling.

# 🔹 Fetching and Displaying Data

if st.button('Fetch Restaurant Data', help="Click to fetch the latest restaurant data"):
    osm_data = fetch_restaurant_data()
    
    if osm_data:
        restaurant_list = process_data(osm_data)
        if restaurant_list:
            df = pd.DataFrame(restaurant_list)

            # Display Table with Styling
            st.markdown("<h3 style='text-align: center;'>📋 Restaurant List</h3>", unsafe_allow_html=True)
            st.markdown("<div class='dataframe'>", unsafe_allow_html=True)
            st.dataframe(df.style.set_properties(**{'background-color': 'white', 'color': 'black'}))
            st.markdown("</div>", unsafe_allow_html=True)

            st.success("✅ Data fetched successfully!")

            # Download Button
            st.download_button(
                label="📥 Download CSV",
                data=df.to_csv(index=False),
                file_name="restaurants.csv",
                mime="text/csv"
            )
        else:
            st.warning("No restaurant data found.")
    else:
        st.error("❌ Failed to retrieve data.")
        
Fetches data when the button is clicked.
Displays the restaurant list in a styled table.
Adds a download button for CSV export.


# 5️⃣ Running the Application

streamlit run script.py
This will open your web browser with the Restaurant Finder app.

# 6️⃣ Summary
Fetches restaurant data from OpenStreetMap.
Displays name, cuisine, address, random rating, and phone number.
Provides a CSV download button.
Uses custom CSS to make the UI more attractive.
🚀 Now you have a fully functional restaurant finder app with an enhanced UI! 🎉
