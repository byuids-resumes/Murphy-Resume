#%%
import pandas as pd
import altair as alt

url="https://raw.githubusercontent.com/byuidatascience/data4names/master/data-raw/names_year/names_year.csv"
NameData= pd.read_csv(url)

NameData.head()
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

Brittany = NameData.query("name == 'Brittany'")

titleBrit = "Years of Babies Named Brittany"

BritGraph= alt.Chart(Brittany, title=titleBrit).mark_line().encode(
    x=alt.X("year", title="Year", axis=alt.Axis(format="d")),
    y=alt.Y("Total", title="Babies Named Brittany")
)

BritGraph


# %%

titleBib= "4 Famous Biblical Names in Recent Years"

BibName = NameData.query("name == 'Mary' | name == 'Peter' | name == 'Paul' | name == 'Martha'")
BibName

BibGraph = alt.Chart(BibName , title=titleBib).mark_line().encode(
    x=alt.X("year", title="Year", axis=alt.Axis(format="d")),
    y=alt.Y("Total", title="Babies Named "),
    color="name"
)

BibGraph

# %%
BatName = NameData.query("name == 'Christian'")

Battitle = "Christian and Batman Movies"
BatNameGraph = alt.Chart(BatName, title=Battitle).mark_line().encode(
    x=alt.X("year", title="Year", axis=alt.Axis(format="d")),
    y=alt.Y("Total", title="Babies Named Christian")
)

YearData = pd.DataFrame({"year": [2005]})

YearChart = alt.Chart(YearData).mark_rule(color="red").encode(
    x="year"
)

BatNameGraph+YearChart
# %%
