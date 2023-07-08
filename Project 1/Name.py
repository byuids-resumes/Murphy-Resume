#%%
import pandas as pd
import altair as alt

url="https://raw.githubusercontent.com/byuidatascience/data4names/master/data-raw/names_year/names_year.csv"
NameData= pd.read_csv(url)

#NameData.head()
#%%
# How does your name at your birth year compare to its use historically?
MyName = NameData.query("name == 'Joshua'")


title = "My Name Was Popular When I Was Born"
MyNameGraph = alt.Chart(MyName, title=title).mark_line().encode(
    x=alt.X("year", title="Year", axis=alt.Axis(format="d")),
    y=alt.Y("Total", title="Babies Named Joshua")
)

YearData = pd.DataFrame({"year": [1997]})

YearChart = alt.Chart(YearData).mark_rule(color="red").encode(
    x="year"
)

MyNameGraph+YearChart

# %%

# If you talked to someone named Brittany on the phone, 
# what is your guess of his or her age? What ages would you not guess?

Felisha = NameData.query("name == 'Felisha'")

titleBrit = "Years Babies were Named Brittany"

BritGraph= alt.Chart(Felisha, title=titleBrit).mark_line().encode(
    x=alt.X("year", title="Year", axis=alt.Axis(format="d")),
    y=alt.Y("Total", title="Babies Named Brittany")
)

BritGraph
# %%

Oliver = NameData.query("name == 'Oliver'")['UT'].sum()

Oliver
# %%
Felisha

# %%
