import pandas as pd
import altair as alt
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score


# Load the data
data = pd.read_csv('https://raw.githubusercontent.com/fivethirtyeight/data/master/star-wars-survey/StarWars.csv',encoding_errors='ignore',header=None,skiprows=2)
# Shorten and clean up column names
data.columns=[
    'respondent_id',
    'seen_any',
    'fan',
    'seen_1',
    'seen_2',
    'seen_3',
    'seen_4',
    'seen_5',
    'seen_6',
    'ranking_1',
    'ranking_2',
    'ranking_3',
    'ranking_4',
    'ranking_5',
    'ranking_6',
    'han_solo',
    'luke_skywalker',
    'princess_leia',
    'anakin_skywalker',
    'obi_wan',
    'emperor_palpatine',
    'darth_vader',
    'lando_calrissian',
    'boba_fett',
    'c3po',
    'r2d2',
    'jar_jar_binks',
    'padme_amidala',
    'yoda',
    'shot_first',
    'expanded_universe',
    'fan_expanded_universe',
    'fan_star_trek',
    'gender',
    'age',
    'income',
    'education',
    'location'
    ]
data = data.rename(columns={
    1:'respondent_id',
    2:'seen_any',
    3:'fan',
    4:'seen_1',
    5:'seen_2',
    6:'seen_3',
    7:'seen_4',
    8:'seen_5',
    9:'seen_6',
    10:'ranking_1',
    11:'ranking_2',
    12:'ranking_3',
    13:'ranking_4',
    14:'ranking_5',
    15:'ranking_6',
    16:'favorite_character',
    17:'han_solo',
    18:'luke_skywalker',
    19:'princess_leia',
    20:'anakin_skywalker',
    21:'obi_wan',
    22:'emperor_palpatine',
    23:'darth_vader',
    24:'lando_calrissian',
    25:'boba_fett',
    26:'c3po',
    27:'r2d2',
    28:'jar_jar_binks',
    29:'padme_amidala',
    30:'yoda',
    31:'shot_first',
    32:'expanded_universe',
    33:'fan_expanded_universe',
    34:'fan_star_trek',
    35:'gender',
    36:'age',
    37:'income',
    38:'education',
    39:'location'
})
data
# Create a separate dataframe for visualization recreation
data_copy = data.copy()

# Clean and format the data
# Filter respondents that have seen at least one film
data = data[data['seen_any'] == 'Yes']
data
# Create a new column for age ranges as a single number
age_mapping = {
    '18-29': 1,
    '30-44': 2,
    '45-60': 3,
    '> 60': 4
}
data['age'] = data['age'].map(age_mapping)

# Drop the age range categorical column
#data['age'] = data['age'].str.replace('\d*[->]','',regex=True)

# Create a new column for education groupings as a single number
education_mapping = {
    'Less than high school degree': 1,
    'High school degree': 2,
    'Some college or Associate degree': 3,
    'Bachelor degree': 4,
    'Graduate degree': 5
}
data['education'] = data['education'].map(education_mapping)


# Create a new column for income ranges as a single number
income_mapping = {
    '$0 - $24,999': 1,
    '$25,000 - $49,999': 2,
    '$50,000 - $99,999': 3,
    '$100,000 - $149,999': 4,
    '$150,000+': 5
}
data['income'] = data['income'].map(income_mapping)


# Create the target column based on the new income range column
data['target'] = (data['income'] > 3).astype(int)

# One-hot encode all remaining categorical columns
categorical_columns = ['seen_1', 'seen_2', 'seen_3', 'seen_4', 'seen_5', 'seen_6',
                       'han_solo', 'luke_skywalker', 'princess_leia', 'anakin_skywalker', 'obi_wan',
                       'emperor_palpatine', 'darth_vader', 'lando_calrissian', 'boba_fett', 'c3po',
                       'r2d2', 'jar_jar_binks', 'padme_amidala', 'yoda', 'shot_first', 'expanded_universe',
                       'fan_expanded_universe', 'fan_star_trek', 'gender', 'location']
data = pd.get_dummies(data, columns=categorical_columns)



seen_all = data[
    (data['seen_1'] == 'Star Wars: Episode I  The Phantom Menace') &
    (data['seen_2'] == 'Star Wars: Episode II  Attack of the Clones') &
    (data['seen_3'] == 'Star Wars: Episode III  Revenge of the Sith') &
    (data['seen_4'] == 'Star Wars: Episode IV  A New Hope') &
    (data['seen_5'] == 'Star Wars: Episode V The Empire Strikes Back') &
    (data['seen_6'] == 'Star Wars: Episode VI Return of the Jedi')
]

# Calculate the percentage of respondents who ranked each movie as their best
ranking_columns = ['ranking_1', 'ranking_2', 'ranking_3', 'ranking_4', 'ranking_5', 'ranking_6']
percentage_best = seen_all[ranking_columns].apply(lambda x: (x == 1).mean() * 100)

# Reset the index and rename columns
percentage_best = percentage_best.reset_index().rename(columns={'index': 'Movie', 0: 'Percentage'})

# Create a bar chart
chart = alt.Chart(percentage_best).mark_bar().encode(
    y='Movie:N',
    x='Percentage:Q', 
    tooltip=['Movie', 'Percentage']
).properties(
    title="Which Star Wars Movie is the Best"
)

text = chart.mark_text(
    align='left',
    baseline='middle',
    dx=3,  # Adjust the horizontal offset of the labels
    fontSize=10
).encode(
    text=alt.Text('Percentage:Q', format='.1f')  # Format the labels to one decimal place
)

# Combine the chart and text layers
chart_with_labels = (chart + text)

chart_with_labels


# Filter the data for respondents who answered about who shot first
shoot_first_data = data[data['shot_first'].isin(['Han', 'Greedo', "I don't understand this question"])]

# Calculate the counts for each option
percentage_data2 = shoot_first_data['shot_first'].value_counts(normalize=True) * 100
percentage_data2 = percentage_data2.reset_index().rename(columns={'index': 'Option', 'shot_first': 'Percentage'})


# Create a bar chart
chart2 = alt.Chart(percentage_data2).mark_bar().encode(
    y=alt.Y('Option:N', title='Option'),
    x=alt.X('Percentage:Q', title='Percentage'),
    color=alt.Color('Option:N', scale=alt.Scale(scheme='category10')),
    tooltip=['Option', 'Percentage']
).properties(
    title="Han vs Greedo: Who Shot First? (Percentage)"
)

text2 = chart2.mark_text(
    align='center',
    baseline='bottom',
    dx=15,  # Adjust the vertical offset of the labels
    color='black',  # Set the color of the labels to black
    fontSize=10  # Set the font size of the labels
).encode(
    text=alt.Text('Percentage:Q', format='.1f')  # Format the labels to one decimal place
)

chart2_labels = (chart2 + text2)

chart2_labels

# Build a machine learning model to predict income > $50k
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score

# Prepare the data
X = data.drop(['respondent_id', 'income', 'target'], axis=1)
y = data['target']

# Split the data into training and test sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train the logistic regression model
model = LogisticRegression()
model.fit(X_train, y_train)

# Predict on the test set
y_pred = model.predict(X_test)

# Calculate accuracy
accuracy = accuracy_score(y_test, y_pred)

# Report the accuracy
print("Accuracy:", accuracy)