import pandas as pd
import altair as alt
import numpy as np
import sqlite3

sqlite_file='lahmansbaseballdb.sqlite'
con=sqlite3.connect(sqlite_file)


byui=pd.read_sql_query(
    'SELECT DISTINCT(c.playerid), c.schoolid, s.salary, s.yearid, s.teamid FROM collegeplaying c JOIN salaries s ON c.playerid = s.playerid WHERE schoolid = "idbyuid" ORDER BY salary DESC;',
    con
)
byui




query1 = """
SELECT playerid, yearid, (batting.h/batting.ab) AS Batting_Average
FROM batting
WHERE ab >= 1
ORDER BY Batting_Average DESC , playerid ASC
LIMIT 5;
"""


top_BA_any = pd.read_sql_query(query1, con)

top_BA_any



query2 = """
SELECT playerid, yearid, (CAST(batting.h AS REAL)/batting.ab) AS Batting_Average
FROM batting
WHERE ab >= 10
ORDER BY Batting_Average DESC , playerid ASC
LIMIT 5;
"""


top_BA_10=pd.read_sql_query(query2, con)

top_BA_10

query3 = """
SELECT DISTINCT(batting.playerid), COUNT(playerid) AS Career_Length, (CAST(batting.h AS REAL)/batting.ab) AS Batting_Average
FROM batting
WHERE batting.ab >= 100
GROUP BY playerid
ORDER BY Batting_Average DESC, batting.playerid ASC
LIMIT 5;
"""

top_BA_Career = pd.read_sql_query(query3, con)

top_BA_Career



query4 = """
SELECT teams.teamid, yearid, name , w ,l, attendance
FROM teams
WHERE teamid = 'LAN' OR teamid = 'BAL'
ORDER BY yearid DESC, teamid ASC
LIMIT 20;
"""

fans_help = pd.read_sql_query(query4, con)

fans_help


chart_name = "Does Fan Attendance Help Impact the Team's Record"
fans_chart = alt.Chart(fans_help, title=chart_name).mark_circle(size=60).encode(
    x=alt.X('attendance:Q', title='Attendance at Home Games all Year',axis=alt.Axis(format="d")),
    y=alt.Y('w:Q' , title='Wins in the Season'),
    color='teamID:N'
)

fans_chart

fans_chart_edited=(alt.Chart(fans_help).encode(x='W',y='attendance',color='teamID', tooltip=['teamID','W','attendance']).mark_circle()).interactive()
fans_chart_edited


quiz_query1="""
SELECT playerid, (CAST(batting.h AS REAL)/batting.ab) AS Batting_Average
FROM batting
LIMIT 2
"""

quiz_1=pd.read_sql_query(quiz_query1, con)
quiz_1

