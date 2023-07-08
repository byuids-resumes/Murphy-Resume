import pandas as pd
import altair as alt
import numpy as np
import string as str

from IPython.display import Markdown
from IPython.display import display
from tabulate import tabulate
from sklearn.naive_bayes import GaussianNB
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split 
from sklearn import metrics
from sklearn import tree


from sklearn.metrics import classification_report
from IPython.display import Markdown
from IPython.display import display
from tabulate import tabulate


swResponse = pd.read_csv('https://raw.githubusercontent.com/fivethirtyeight/data/master/star-wars-survey/StarWars.csv',encoding_errors='ignore',header=None,skiprows=2)
swQuestion = pd.read_csv('https://raw.githubusercontent.com/fivethirtyeight/data/master/star-wars-survey/StarWars.csv',encoding_errors='ignore',header=None,nrows=2)

print(swResponse.head(10))
print(swQuestion.head(5))


swQuestion[9]=swQuestion[9].str.strip('?').str.replace('Please rank the Star Wars films in order of preference with 1 being your favorite film in the franchise and 6 being your least favorite film.','FilmPreference')
swQuestion[1]=swQuestion[1].str.strip('?').str.replace('Have you seen any of the 6 films in the Star Wars franchise','SeenAny')
swQuestion[2]=swQuestion[2].str.strip('?').str.replace('Do you consider yourself to be a fan of the Star Wars film franchise','IsFan')
swQuestion[3]=swQuestion[3].str.replace('^.*$','Seen',regex=True) ##Fix
swQuestion[15]=swQuestion[15].str.replace('Please state whether you view the following characters favorably, unfavorably, or are unfamiliar with him/her.','Favorable_')
swQuestion[29]=swQuestion[29].str.strip('?').str.replace('Which character shot first?','HanShot')
swQuestion[30]=swQuestion[30].str.strip('?').str.replace('Are you familiar with the Expanded Universe?','EUFamiliar')
swQuestion[31]=swQuestion[31].str.strip('?').str.replace('Do you consider yourself to be a fan of the Expanded Universe?','EUFan')
swQuestion[32]=swQuestion[32].str.strip('?').str.replace('Do you consider yourself to be a fan of the Star Trek franchise?','Startrek')

swQuestion.ffill()
swQuestion[0].na_rep = "NA"
for x in range(3,15):
    swQuestion[x] = (swQuestion[x].str.strip().str.replace('Star Wars: Episode I  The Phantom Menace','Ep1')
    .str.replace('Star Wars: Episode II  Attack of the Clones','Ep2')
    .str.replace('Star Wars: Episode III  Revenge of the Sith','Ep3')
    .str.replace('Star Wars: Episode IV  A New Hope','Ep4')
    .str.replace('Star Wars: Episode V The Empire Strikes Back','Ep5')
    .str.replace('Star Wars: Episode VI Return of the Jedi','Ep6')
    )    

for x in range(15,29):
    swQuestion[x]=swQuestion[x].str.strip().str.replace(' ','')
    
swQuestion[35]=swQuestion[35].str.replace('HouseholdIncome','')
swQuestion[37]=swQuestion[37].str.replace('\(.*$','').str.strip()
swQuestion.iloc[1]=swQuestion.iloc[1].ffill().str.replace('Response','')
swQuestion.iloc[0]=swQuestion.iloc[0].ffill()
Markdown(swQuestion.to_markdown(index=False))



for x in range(15,29):
    swResponse[x] = (swResponse[x].str.replace('Very favorably','5')
    .str.replace('Somewhat favorably','4')
    .str.replace('^N.*$','3',regex=True)
    .str.replace('Somewhat unfavorably','2')
    .str.replace('Very unfavorably','1')
    .str.replace('^U.*$','0',regex=True)
    )


for x in range(3,9):
    swResponse[x] = (swResponse[x].str.replace('Star Wars: Episode I  The Phantom Menace','ep1')
    .str.replace('Star Wars: Episode II  Attack of the Clones','ep2')
    .str.replace('Star Wars: Episode III  Revenge of the Sith','ep3')
    .str.replace('Star Wars: Episode IV  A New Hope','ep4')
    .str.replace('Star Wars: Episode V The Empire Strikes Back','ep5')
    .str.replace('Star Wars: Episode VI Return of the Jedi','ep6')
)

swResponse[35]=(swResponse[35].dropna()
    .str.replace(',','')
    .str.replace('+','')
    .str.replace('$','')
    .str.replace('\s\-\s\d*$','',regex=True)
        #everything after the first number
    .astype('int')
) 

swResponse[34]=swResponse[34].str.replace('\d*[->]','',regex=True)

swResponse[36]=(swResponse[36]
    .str.replace('^.*A','A',regex=True)
    .str.replace('degree','')
    .str.upper()
    .str.replace(' ','')
)
Markdown(swResponse.sample(n=10).to_markdown(index=False)
)


newHeader = []
for x in range(38):
    #newHeader.append(
    newpiece = pd.Series([swQuestion.iat[0,x],swQuestion.iat[1,x]])
    newHeader.append(newpiece.str.cat(na_rep = "NA"))

swResponse.columns=newHeader
swResponse
#swResponse['Over50K']=np.where(swResponse['HouseholdIncome']>=50000,1,0)
#double check, should be moved

shot_first_onehot = pd.get_dummies(swResponse['HanShot'])
#swResponse['Han'],swResponse['eithershot'] = pd.get_dummies(swResponse['HanShot'], drop_first=True)
swResponse['Hanfirst'] = shot_first_onehot['Han']
swResponse['Greedofirst'] = shot_first_onehot['Greedo']

swResponse['Location']=swResponse['Location'].str.replace(' ','')
location_onehot= pd.get_dummies(swResponse['Location'],drop_first=True)
for x in location_onehot.columns:
    swResponse[x]=location_onehot[x]

ed_oh=pd.get_dummies(swResponse['Education'],drop_first=True)
for x in ed_oh.columns:
    swResponse[x]=ed_oh[x] 

for x in ['SeenAny','IsFan','EUFamiliar', 'EUFan', 'Startrek', 'Gender']:
    swResponse[x]=pd.get_dummies(swResponse[x],drop_first=True)
swResponse['IsMale']=pd.get_dummies(swResponse['Gender'],drop_first=True)
#Need the same thing for the seen categories
#prob too many columns
Markdown(swResponse[swResponse.SeenAny==1].sample(n=10).to_markdown(index=False))




likeLuke = swResponse['Favorable_LukeSkywalker'].value_counts().rename_axis('unique_values').reset_index(name='Count')
likeLuke

likeLuke['Percent']=likeLuke['Count']/sum(likeLuke['Count'])
luke2 = pd.DataFrame({
        'Favoring':['Favorable','Neutral','Unfavorable','Unfamiliar'],
        'Percent':[likeLuke['Percent'].iloc[0]+likeLuke['Percent'].iloc[1],likeLuke['Percent'].iloc[2],likeLuke['Percent'].iloc[3]+likeLuke['Percent'].iloc[5],likeLuke['Percent'].iloc[4]]
})
lukeChart = (alt.Chart(luke2)
    .encode(x=alt.X('Favoring'),
            y=alt.Y('Percent',axis=alt.Axis(format='%',title='Percentage'))
    )
    .properties(title="People Like Luke")
    .mark_bar(color='blue')
)
lukeChart






shots = swResponse['HanShot'].value_counts().rename_axis('unique_values').reset_index(name='Count')
shotssum = len(swResponse['HanShot'].dropna())
shots['Percent']=shots['Count']/shotssum

shotChart = (alt.Chart(shots)
    .encode(y=alt.Y('unique_values'),
    x=alt.X('Percent',axis=alt.Axis(format='%'))
    )
    .mark_bar(color='blue')
    .properties(title='Who Shot First?')
)
shotChart










swML=swResponse.dropna()
swML['Over50K']=np.where(swML['HouseholdIncome']>=50000,1,0)
features = swML[['IsFan','Hanfirst',
       'Greedofirst', 'EastSouthCentral', 'MiddleAtlantic', 'Mountain',
       'NewEngland', 'Pacific', 'SouthAtlantic', 'WestNorthCentral',
       'WestSouthCentral', 'IsMale', 'BACHELOR', 'GRADUATE',
       'HIGHSCHOOL', 'LESSTHANHIGHSCHOOL','EUFamiliar', 'EUFan', 'Startrek','Age']]
targets = swML['Over50K']
x_train, x_test, y_train, y_test = train_test_split(features, targets, test_size = .33, random_state = 14)

DT_model = DecisionTreeClassifier(max_depth = 5)
DT_model.fit(x_train,y_train)
DT_predict = DT_model.predict(x_test)
print('Accuracy: ', metrics.accuracy_score(y_test, DT_predict))


DT_model.feature_importances_
features_df = pd.DataFrame({'features':x_test.columns,'importance':DT_model.feature_importances_})
ImportantChart = alt.Chart(features_df).encode(
    x=alt.X('features',sort='-y',axis=alt.Axis(title='What Features?')),
    y=alt.Y('importance',axis=alt.Axis(title='How Impactful Were they?',format='%')),
).mark_bar().properties(title='The Resistance')
ImportantChart


alt.Chart(swResponse).mark_bar().encode(
    y='Cylinders:O',
    x='mean_acc:Q'
).transform_aggregate(
    mean_acc='mean(Acceleration)',
    groupby=["Cylinders"]
)







AnyWatch = swResponse[swResponse['IsMale']==1]['SeenAny'].value_counts().rename_axis('uniqueValues').reset_index(name='Count')
AnyWatch['Percent']=AnyWatch['Count']/sum(AnyWatch['Count'])
AnyWatch

maleWatch = swResponse[swResponse['IsMale']==1]

percent_males_seen = (len(maleWatch) / len(swResponse))
percent_males_seen = round(percent_males_seen, 4)
percent_males_seen

for x in ['SeenAny','Gender']:
    swResponse[x]=pd.get_dummies(swResponse[x],drop_first=True)
swResponse['IsMale']=pd.get_dummies(swResponse['Gender'],drop_first=True)
swResponse['SeenAny'].value_counts()
#Need the same thing for the seen categories
#prob too many columns
Markdown(swResponse[swResponse.IsMale==1].sample(n=497).to_markdown(index=False))

