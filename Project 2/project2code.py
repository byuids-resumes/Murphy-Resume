import pandas as pd
import numpy as np

# Load the JSON file
data = pd.read_json("https://raw.githubusercontent.com/byuidatascience/data4missing/master/data-raw/flights_missing/flights_missing.json")

# Replace empty strings with NaN
data = data.replace('', np.nan)

# Display one record example
example_record = data.iloc[0].to_json()
print(example_record)
data.head(5)
data.info

# Calculate total flights per airport_code
total_flights = data.groupby('airport_code')['num_of_flights_total'].sum()
total_flights

# Calculate total delayed flights per airport_code
total_delayed_flights = data.groupby('airport_code')['num_of_delays_total'].sum()
total_delayed_flights
# Calculate proportion of delayed flights per airport_code
proportion_delayed = total_delayed_flights / total_flights
proportion_delayed
# Calculate average delay time per airport_code
average_delay_time = data.groupby('airport_code')['num_of_delays_total'].mean()

# Create summary table
summary_table = pd.DataFrame({
    'Total Flights': total_flights,
    'Total Delayed Flights': total_delayed_flights,
    'Proportion of Delayed Flights': proportion_delayed,
    'Average Delay Time (hours)': average_delay_time
})
summary_table
# Sort the table by the proportion of delayed flights in descending order
summary_table = summary_table.sort_values('Proportion of Delayed Flights', ascending=False)

# Display the summary table
summary_table

# Remove rows with missing month values
data = data.dropna(subset='month')

# Calculate the proportion of delayed flights for each month
proportion_delayed_month = data.groupby('month')['num_of_delays_total'].mean()

# Create a bar chart
import altair as alt

chart = alt.Chart(proportion_delayed_month.reset_index()).mark_bar().encode(
    x=alt.X('month:N', sort=alt.EncodingSortField(field='month', order='ascending')),
    y='num_of_delays_total:Q'
)

chart

# Replace missing values in Late Aircraft with the mean
data['num_of_delays_total'] = data['num_of_delays_total'].fillna(data['num_of_delays_total'].mean())

# Calculate total flights delayed by weather
data['num_of_delays_weather'] >= 1
data.loc[data['num_of_delays_total'] == 'num_of_delays_weather', 'num_of_delays_weather'] = data.loc[data['num_of_delays_total'] == 'num_of_delays_weather', 'num_of_delays_total']
data.loc[data['num_of_delays_total'] == 'num_of_delays_total', 'num_of_delays_weather'] = data.loc[data['num_of_delays_total'] == 'num_of_delays_total', 'num_of_delays_total'] * 0.3
data.loc[(data['num_of_delays_total'] == 'NAS') & (data['month'].isin(['April', 'May', 'June', 'July', 'August'])), 'num_of_delays_weather'] = data.loc[(data['num_of_delays_total'] == 'NAS') & (data['month'].isin(['April', 'May', 'June', 'July', 'August'])), 'num_of_delays_total'] * 0.4
data.loc[(data['num_of_delays_total'] == 'NAS') & (~data['month'].isin(['April', 'May', 'June', 'July', 'August'])), 'num_of_delays_weather'] = data.loc[(data['num_of_delays_total'] == 'NAS') & (~data['month'].isin(['April', 'May', 'June', 'July', 'August'])), 'num_of_delays_total'] * 0.65

# Print the first 5 rows of the updated data
print(data)

# Calculate the proportion of all flights delayed by weather at each airport_code
proportion_weather_delay = data.groupby('airport_code')['num_of_delays_weather'].sum() / data.groupby('airport_code')['num_of_flights_total'].sum()

# Create a barplot
chart2 = alt.Chart(proportion_weather_delay.reset_index()).mark_bar().encode(
    x='airport_code:N',
    y='num_of_delays_weather:Q'
)

chart2
