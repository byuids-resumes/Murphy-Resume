# %%
print("Hello World!")
# %%

import pandas as pd
import altair as alt

# %%
url = "https://github.com/byuidatascience/data4python4ds/raw/master/data-raw/mpg/mpg.csv"
mpg = pd.read_csv(url)
# %%