import streamlit as st
import pandas as pd
import json
import plotly.express as px

# Load JSON data
@st.cache_data
def load_data(file_path):
    with open(file_path, "r") as file:
        json_data = json.load(file)
    return json_data["data"]["data"]

# Prepare the DataFrame
@st.cache_data
def prepare_dataframe(sensor_data):
    df = pd.DataFrame(sensor_data)
    df["floatSensor"] = df["floatSensor"].astype(float)
    df["gaseSensor"] = df["gaseSensor"].astype(float)
    df["solar-sensor"] = df["solar-sensor"].astype(float)
    df["Timestamp"] = pd.to_datetime(df["Timestamp"])
    return df

# Load and prepare data
sensor_data = load_data("hack11.json")
df = prepare_dataframe(sensor_data)

# Streamlit app layout

# Add custom CSS to style the title
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

# Define custom colors for sensors
sensor_colors = {
    "floatSensor": "blue",
    "gaseSensor": "grey",
    "solar-sensor": "orange",
}

# Separate Line Charts for Each Sensor using Plotly
st.markdown(
    """
    <h2 style='text-align: center;'>💧📊Sensor Data Visualization📉☀️</h2>
    """, unsafe_allow_html=True
)


# Loop over each sensor to plot the bar chart
for sensor in ["floatSensor"]:
    st.subheader("Water level Vs Time")
    
    # Create the bar chart using Plotly Express
    fig = px.bar(
        df,
        x="Time",
        y="Water level",
        #labels={"Timestamp": "Time", sensor: "Water level"},
        #title=f"{sensor} Water Level Over Time",
    )
    
    # Set the custom color for the sensor's bars
    fig.update_traces(marker=dict(color=sensor_colors[sensor], line=dict(width=7)))
    
    # Display the chart in Streamlit
    st.plotly_chart(fig)
for sensor in ["gaseSensor"]:
    st.subheader("Gas level Vs time")
    fig = px.line(
        df,
        x="Timestamp",
        y=sensor,
        #title=f"{sensor} Over Time",
        labels={"Timestamp": "Time", sensor: "Gas level"},
        line_shape="linear",
        markers=True,
    )
    # Set the custom color for the sensor
    fig.update_traces(line=dict(color=sensor_colors[sensor], width=2), marker=dict(size=8))
    st.plotly_chart(fig)
for sensor in ["solar-sensor"]:
    st.subheader("Solar energy consumed Vs Time")
    fig = px.line(
        df,
        x="Timestamp",
        y=sensor,
        #title=f"{sensor} Over Time",
        labels={"Timestamp": "Time", sensor: "Solar energy consumption"},
        line_shape="linear",
        markers=True,
    )
    # Set the custom color for the sensor
    fig.update_traces(line=dict(color=sensor_colors[sensor], width=2), marker=dict(size=8))
    st.plotly_chart(fig)
# Dropdown to filter data by date and 
st.subheader("🔍Searching of Sensor data by 📅Date and ⌚Time🔎")

# Extract unique dates and times
df['Date'] = df['Timestamp'].dt.date
df['Time'] = df['Timestamp'].dt.time
unique_dates = df['Date'].unique()
unique_times = df['Time'].unique()

# Create dropdowns
selected_date = st.selectbox("Select a Date", unique_dates, index=0)
selected_time = st.selectbox("Select a Time", unique_times, index=0)

# Filter the data based on selected date and time
filtered_df = df[(df['Date'] == selected_date) & (df['Time'] == selected_time)]

st.subheader(f"Filtered Data for {selected_date} at {selected_time}")
if filtered_df.empty:
    st.write("No data available for the selected date and time.")
else:
    st.dataframe(filtered_df)

# Define custom colors for sensors
sensor_colors = {
    "floatSensor": "blue",
    "gaseSensor": "grey",
    "solar-sensor": "orange",
}

# Separate Line Charts for Each Sensor using Plotly
st.subheader("Line Charts: 🔍Sensor Data at given Time⌚")

for sensor in ["floatSensor", "gaseSensor", "solar-sensor"]:
    st.subheader(f"{sensor} at given Time")
    fig = px.line(
        filtered_df,
        x="Timestamp",
        y=sensor,
        #title=f"{sensor} at given Time",
        labels={"Timestamp": "Time", sensor: "Sensor Value"},
        line_shape="linear",
        markers=True,
    )
    # Set the custom color for the sensor
    fig.update_traces(line=dict(color=sensor_colors[sensor], width=2), marker=dict(size=8))
    st.plotly_chart(fig)

# Display raw data
st.subheader("Raw json Data")
st.dataframe(df)
