import requests
import pandas as pd
import streamlit as st
import random  

# Define Overpass API endpoint
OVERPASS_URL = "http://overpass-api.de/api/interpreter"

# Define the area (Example: Downtown Toronto)
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

# List of random dishes
random_dishes = ["Pizza", "Sushi", "Burger", "Pasta", "Tacos", "Ramen", "BBQ", "Steak", "Salad", "Falafel"]

# List of random street names in Toronto
random_streets = ["King St", "Queen St", "Dundas St", "Yonge St", "Spadina Ave", "Bloor St", "Bay St", "College St"]

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

def fetch_restaurant_data():
    """Fetch restaurant data from OpenStreetMap using Overpass API."""
    response = requests.get(OVERPASS_URL, params={"data": QUERY})
    
    if response.status_code == 200:
        return response.json()
    else:
        st.error(f"Error {response.status_code}: Unable to fetch data")
        return None

def process_data(osm_data):
    """Extract relevant details from OSM response and add random ratings, dishes, and phone numbers."""
    restaurants = []

    for element in osm_data.get("elements", []):
        tags = element.get("tags", {})

        # Assign a random dish if cuisine is not specified
        cuisine = tags.get("cuisine")
        if not cuisine:
            cuisine = random.choice(random_dishes)

        # Assign a random address if it's not provided
        street = tags.get("addr:street")
        city = tags.get("addr:city")
        
        if not street:
            street = random.choice(random_streets)
        
        if not city:
            city = "Toronto"  # Default city

        address = f"{street}, {city}"

        restaurants.append({
            "Name": tags.get("name", "Unknown"),
            "Cuisine": cuisine,
            "Address": address,
            "Phone": generate_random_phone_number("CA"),  
            "Rating": f"{round(random.uniform(1.0, 5.0), 1):.1f}"  # ✅ Ensures one decimal
        })
    
    return restaurants

def app():
    """Streamlit app with enhanced UI."""
    
    # Custom CSS for Styling
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

    # Custom Title
    st.markdown("<div class='main-title'>🍽️ Restaurant Finder in Toronto</div>", unsafe_allow_html=True)

    # Fetch data when the user presses the button
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

if __name__ == '__main__':
    app()
