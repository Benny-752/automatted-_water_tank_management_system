import streamlit as st
import pandas as pd
import requests
import plotly.express as px

# Fetch live sensor data from the server
@st.cache_data
def fetch_sensor_data():
    # The URL of the server
    url = "https://iot1.innotrat.in/api/product/get-data"  # Replace with the actual URL

    # The JSON payload
    payload = {
        "productID": "3c5add95-a638-4481-803d-027791a6fd59"
    }

    # Headers (if required by the server)
    headers = {
    "Content-Type": "application/json",
    "Authorization": "Bearer your_token_here",
    "User-Agent": "YourAppName/1.0",
    "Accept": "application/json"
    }


    try:
        # Making the POST request
        response = requests.post(url, json=payload)

        # Checking for successful response
        if response.status_code == 200:
            # Parsing the response JSON
            data = response.json()
            return data["data"]["data"]  # Adjust key structure if different
        else:
            st.error(f"Failed to fetch data: {response.status_code} - {response.text}")
            return []
    except Exception as e:
        st.error(f"An error occurred while fetching data: {str(e)}")
        return []

# Prepare the DataFrame
@st.cache_data
def prepare_dataframe(sensor_data):
    df = pd.DataFrame(sensor_data)
    df["floatSensor"] = df["floatSensor"].astype(float)
    df["gaseSensor"] = df["gaseSensor"].astype(float)
    df["solar-sensor"] = df["solar-sensor"].astype(float)
    df["Timestamp"] = pd.to_datetime(df["Timestamp"])
    return df

# Fetch and prepare data
sensor_data = fetch_sensor_data()
if sensor_data:
    df = prepare_dataframe(sensor_data)

    # Define custom colors for sensors
    sensor_colors = {
        "floatSensor": "blue",
        "gaseSensor": "grey",
        "solar-sensor": "orange",
    }
    # Streamlit app layout
    st.markdown(
        """
        <style>
        .title {
            text-align: center; /* Center-align the text */
            width: 100%; /* Make it span full width */
            font-size: 3em; /* Adjust size as needed */
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    # Render the title
    st.markdown('<div class="title">Automated Water Tank Management System</div>', unsafe_allow_html=True)
        
    # Separate Line Charts for Each Sensor using Plotly
    st.markdown(
        """
        <h2 style='text-align: center;'>💧📊Sensor Data Visualization📉☀️</h2>
        """, unsafe_allow_html=True
    )
    for sensor in ["floatSensor", "gaseSensor", "solar-sensor"]:
        st.subheader(f"{sensor} Over Time")
        fig = px.line(
            df,
            x="Timestamp",
            y=sensor,
            #title=f"{sensor} Over Time",
            labels={"Timestamp": "Time", sensor: "Sensor Value"},
            line_shape="linear",
            markers=True,
        )
        # Set the custom color for the sensor
        fig.update_traces(line=dict(color=sensor_colors[sensor], width=2), marker=dict(size=8))
        st.plotly_chart(fig)
    # Dropdown to filter data by date and time
    
    # Dropdown to filter data by date and 
    st.subheader("🔍Searching of Sensor Data by 📅Date and ⌚Time🔎")

    # Extract unique dates and times
    df["Date"] = df["Timestamp"].dt.date
    df["Time"] = df["Timestamp"].dt.time
    unique_dates = df["Date"].unique()
    unique_times = df["Time"].unique()

    # Create dropdowns
    selected_date = st.selectbox("Select a Date", unique_dates, index=0)
    selected_time = st.selectbox("Select a Time", unique_times, index=0)

    # Filter the data based on selected date and time
    filtered_df = df[(df["Date"] == selected_date) & (df["Time"] == selected_time)]

    st.subheader(f"Filtered Data for {selected_date} at {selected_time}")
    if filtered_df.empty:
        st.write("No data available for the selected date and time.")
    else:
        st.dataframe(filtered_df)

    # Separate Line Charts for Each Sensor using Plotly
    st.subheader("Line Charts: 🔍Sensor Data at given Time⌚")
    for sensor in ["floatSensor", "gaseSensor", "solar-sensor"]:
        st.subheader(f"{sensor} at given Time")
        fig = px.line(
            filtered_df,
            x="Timestamp",
            y=sensor,
            #title=f"{sensor} Over Time",
            labels={"Timestamp": "Time", sensor: "Sensor Value"},
            line_shape="linear",
            markers=True,
        )
        # Set the custom color for the sensor
        fig.update_traces(line=dict(color=sensor_colors[sensor], width=2), marker=dict(size=8))
        st.plotly_chart(fig)

        

    # Display raw data
    st.subheader("Raw Data")
    st.dataframe(df)
else:
    st.error("No data to display. Please check the server or your configuration.")
