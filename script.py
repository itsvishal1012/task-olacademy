import requests
import pandas as pd
import streamlit as st

# Define the Overpass API endpoint
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

def fetch_restaurant_data():
    """Fetch restaurant data from OpenStreetMap using Overpass API."""
    response = requests.get(OVERPASS_URL, params={"data": QUERY})
    
    if response.status_code == 200:
        return response.json()
    else:
        st.error(f"Error {response.status_code}: Unable to fetch data")
        return None

def process_data(osm_data):
    """Extract relevant details from OSM response."""
    restaurants = []

    for element in osm_data.get("elements", []):
        tags = element.get("tags", {})
        restaurants.append({
            "Name": tags.get("name", "Unknown"),
            "Cuisine": tags.get("cuisine", "Not specified"),
            "Address": tags.get("addr:street", "Unknown") + ", " + tags.get("addr:city", "Unknown"),
            "Phone": tags.get("contact:phone", "N/A"),
            "Rating": tags.get("rating", "N/A")
        })
    
    return restaurants

def app():
    """Streamlit app to display restaurant data."""
    st.title("Restaurant Finder in Toronto")

    # Fetch data when the user presses the button
    if st.button('Fetch Restaurant Data'):
        osm_data = fetch_restaurant_data()
        
        if osm_data:
            restaurant_list = process_data(osm_data)
            if restaurant_list:
                df = pd.DataFrame(restaurant_list)
                st.write(df)  # Display the table
                st.success("✅ Data fetched successfully!")
                
                # Allow users to download the data as CSV
                st.download_button(
                    label="Download CSV",
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
