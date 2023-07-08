import pandas as pd
import altair as alt
import numpy as np
import string as str
from IPython.display import Markdown


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
    
swQuestion[35]=swQuestion[35].str.replace('Household','')
swQuestion[37]=swQuestion[37].str.replace('\(.*$','').str.strip()
swQuestion.iloc[1]=swQuestion.iloc[1].ffill().str.replace('Response','')
swQuestion.iloc[0]=swQuestion.iloc[0].ffill()
Markdown(swQuestion.to_markdown(index=False))