import pandas as pd
import altair as alt
import numpy as np


alt.data_transformers.disable_max_rows()

url="https://raw.githubusercontent.com/byuidatascience/data4dwellings/master/data-raw/dwellings_ml/dwellings_ml.csv"
data = pd.read_csv(url)

print(data.head(5))

from sklearn.naive_bayes import GaussianNB
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split 
from sklearn import metrics
from sklearn import tree


"""
I want to be able to get the categories it learns from
to be sprice (Selling Price), condition_AVG, condition_Fair,
 and livearea (Square Footage of Liveable area)
"""
title = "Does Square Footage Impact A House's Condition"
chart1 = alt.Chart(data, title=title).transform_density(
    "livearea",
    as_=["livearea", "sprice"],
    groupby=["condition_AVG","condition_Fair"]
).mark_area(opacity=.5).encode(
    alt.X("livearea:Q"),
    alt.Y("sprice:Q"),
    alt.Color("condition_Fair:N","condition_AVG:N")
).configure_title(anchor="start")

chart1