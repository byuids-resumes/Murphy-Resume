
import pandas as pd
import altair as alt
import numpy as np

url="https://raw.githubusercontent.com/byuidatascience/data4missing/master/data-raw/flights_missing/flights_missing.json"
flight_data=pd.read_json(url)

flight_data.head(5)

flight_data.info()

flight_data.month.value_counts()

flight_data.describe()

flight_data.year.fillna

flight_data.dropna(inplace=True)

flight_data.year=flight_data.year.astype(int)


# missing values in the airport_name, minutes_delayed_carrier
# num_of_delays_carrier, num_of_delays_late_aircraft, minutes_delayed_nas
# year, month

flight_data = flight_data.assign(average_delay_time = flight_data.minutes_delayed_total/flight_data.num_of_delays_total)
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

flight_data.minutes_delayed_nas.value_counts()

flight_data.dropna(subset='month')


flight_data_total_delays = flight_data.dropna(subset='month').groupby(['airport_code','num_of_delays_total'])
flight_data_total_delays.agg('Delays', np.count_nonzero(flight_data_total_delays >0)).reset_index()

title_q2 = "The Overall Worst Month to Fly is"

flight_chart_month_delays = alt.Chart(flight_data.dropna(subset= 'month'), title=title_q2, width=500).mark_bar().encode(x=alt.X("month", title = "Months"),y=alt.Y("num_of_delays_total", title= "Total Delays"))

flight_chart_month_delays