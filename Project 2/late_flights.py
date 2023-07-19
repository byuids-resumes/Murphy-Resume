import pandas as pd
import numpy as np
import altair as alt
from tabulate import tabulate
#1
# Load the JSON file
data = pd.read_json("https://raw.githubusercontent.com/byuidatascience/data4missing/master/data-raw/flights_missing/flights_missing.json")

flight_data = data.assign(average_delay_time = data.minutes_delayed_total/data.num_of_delays_total)
title="Among Other Airlines, ORD Has The Highest Overall Delay Times"
flight_chart = alt.Chart(flight_data, title=title, width=500).mark_boxplot().encode(
    x=alt.X("average_delay_time", title = "Minutes"),
    y=alt.Y("airport_code", title= "Airport Code")
    )


flight_data=flight_data.assign(hours_delayed_total=flight_data.minutes_delayed_total / 60)

flight_data.groupby("airport_code").agg(
    total_num_flights=('num_of_flights_total','sum'),
    total_delayed_flights=('num_of_delays_total', 'sum'),
    hours_delay_average=('hours_delayed_total', 'mean')
).assign(prop_delayed_flights = lambda x: x.total_delayed_flights / x.total_num_flights )

flight_chart.encoding.x.scale = alt.Scale(domain=[30, 100])

flight_chart



#2
# Remove rows with missing month values
data_cleaned = data.dropna(subset=["month"])

# Group data by month
month_summary = data_cleaned.groupby("month").agg({
    "num_of_flights_total": "sum",
    "num_of_delays_total": "sum",
})

# Calculate proportion of num_of_delays_total
month_summary["Proportion of Delays"] = month_summary["num_of_delays_total"] / month_summary["num_of_flights_total"]

# Reset the index to use the month as a column
month_summary.reset_index(inplace=True)

# Sort months in chronological order
month_order = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
month_summary["month"] = pd.Categorical(month_summary["month"], categories=month_order, ordered=True)
month_summary = month_summary.sort_values("month")

# Create the bar plot using Altair
bar_plot_month = alt.Chart(month_summary).mark_bar().encode(
    x=alt.X("month:N", title="month", sort=month_order),
    y=alt.Y("Proportion of Delays:Q", title="Proportion of num_of_delays_total"),
    tooltip=["month", "Proportion of Delays"]
).properties(
    width=600,
    height=400,
    title="Proportion of Delays by month"
)

# Display the bar plot
bar_plot_month


#3
# Create a new column for mild weather delayed flights
data["Mild Weather"] = 0


# Rule 1: 100% of delayed flights in the Weather category are due to severe weather
data["Severe Weather"] = data["num_of_delays_weather"]

# Rule 2: 30% of all delayed flights in the Late-Arriving category are due to weather (mild weather)
data["Mild Weather"] = 0.3 * data["num_of_delays_late_aircraft"]

# Rule 3: From April to August, 40% of delayed flights are due to weather. The rest of the months, the proportion rises to 65%.
is_april_to_august = (data["month"].isin(["April", "May", "June", "July", "August"]))
data.loc[is_april_to_august & (data["Mild Weather"] == 0), "Mild Weather"] = 0.4 * data.loc[is_april_to_august & (data["Mild Weather"] == 0), "num_of_delays_nas"]
data.loc[~is_april_to_august & (data["Mild Weather"] == 0), "Mild Weather"] = 0.65 * data.loc[~is_april_to_august & (data["Mild Weather"] == 0), "num_of_delays_nas"]

data["Mild Weather"] = data["Mild Weather"].astype(int)

# Calculate the percentage of flights delayed by weather for each airport
airport_weather_summary = data.groupby("airport_code").agg({
    "num_of_flights_total": "sum",
    "Mild Weather": "sum",
    "Severe Weather": "sum"
})

# Calculate the proportion of flights delayed by mild and severe weather for each airport
airport_weather_summary["Mild Weather Delayed Flights"] = airport_weather_summary["Mild Weather"] / airport_weather_summary["num_of_flights_total"]
airport_weather_summary["Severe Weather Delayed Flights"] = airport_weather_summary["Severe Weather"] / airport_weather_summary["num_of_flights_total"]

# Display the first 5 rows of data with the new columns
data.head(5)

#4

# Reset the index and use .items() instead of iteritems()
airport_weather_summary.reset_index(inplace=True)
airport_weather_summary = pd.melt(airport_weather_summary, id_vars=["airport_code"], value_vars=["Mild Weather Delayed Flights", "Severe Weather Delayed Flights"], var_name="Weather Category", value_name="Proportion of Delayed Flights")

# Create the bar plot 
bar_plot_weather = alt.Chart(airport_weather_summary).mark_bar().encode(
    x=alt.X("airport_code:N", title="Airport"),
    y=alt.Y("Proportion of Delayed Flights:Q", title="Proportion of Delayed Flights"),
    color=alt.Color("Weather Category:N", scale=alt.Scale(domain=["Mild Weather Delayed Flights", "Severe Weather Delayed Flights"], range=["#1f77b4", "#ff7f0e"])),
    tooltip=["airport_code", "Proportion of Delayed Flights"]
).properties(
    width=700,
    height=500,
    title="Proportion of Flights Delayed by Mild and Severe Weather at Each Airport"
)

# Display the bar plot
bar_plot_weather

#5
# Fix missing data types (convert empty strings to NaN)
data.replace("", np.nan, inplace=True)

data.iloc[2]