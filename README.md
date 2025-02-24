# 🍽️ Restaurant Finder

## 📌 Project Overview
The **Restaurant Finder** is a web application built using **Streamlit**, **OpenStreetMap (Overpass API)**, and **Python**. It fetches restaurant data for a given city (default: Toronto) and displays essential details such as name, cuisine, address, phone number, and a random rating.

## 🚀 Features
- Fetches restaurant data from OpenStreetMap.
- Displays restaurant details in a structured table.
- Handles missing data by assigning random values.
- Provides an option to download the data as a CSV file.
- Enhanced UI with a modern look using Streamlit's markdown and custom CSS.

---

## 🎯 Why Use Random Data?

### 📞 1. **Random Phone Numbers**
**Reason:**
- OpenStreetMap does not always provide restaurant contact numbers.
- To maintain data privacy and avoid exposing real phone numbers, we generate **random phone numbers**.
- The numbers follow country-specific formats, ensuring they look realistic without violating any privacy rules.

### ⭐ 2. **Random Ratings**
**Reason:**
- OpenStreetMap does not store user ratings for restaurants.
- To simulate a real-world experience, we generate a **random rating between 1.0 and 5.0**, ensuring only **one decimal place**.
- This provides a user-friendly view while avoiding misinformation about actual restaurant quality.

### 🍽️ 3. **Assigning Cuisine When Missing**
**Reason:**
- Some restaurants may not have their cuisine type listed in OpenStreetMap.
- To improve data completeness, we randomly assign a **popular dish** (e.g., Pizza, Sushi, Burger, etc.).
- This enhances the user experience by providing useful information even if the actual data is missing.

### 📍 4. **Assigning Addresses When Missing**
**Reason:**
- Many restaurants in OpenStreetMap do not provide a full address.
- To make the data usable, we randomly assign **a street name from the selected city**.
- This ensures that every restaurant in the dataset has a location reference.

---

## 🛠️ Tech Stack
- **Python**: Core language used.
- **Streamlit**: Interactive UI framework.
- **Pandas**: Data handling and table display.
- **Requests**: API calls to fetch restaurant data.
- **OpenStreetMap (Overpass API)**: Source of restaurant data.
- **Random**: Used for generating missing data (ratings, phone numbers, cuisine, addresses).

---

## 📜 How to Run the Project
### 🔹 Prerequisites
Make sure you have Python installed and install the required dependencies:
```sh
pip install streamlit pandas requests
```

### 🔹 Run the Application
```sh
streamlit run script.py
```

### 🔹 Fetch Restaurant Data
1. Click on the **"Fetch Restaurant Data"** button to retrieve data from OpenStreetMap.
2. View restaurant details in a table format.
3. Download the data as a CSV file if needed.

---

## 🏗️ Future Improvements
- Add more cities dynamically.
- Implement real user reviews and ratings.
- Integrate Google Maps for better location representation.

📌 **This project ensures privacy while making restaurant data more accessible and user-friendly!** 🎉

