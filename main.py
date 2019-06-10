import requests
import pprint
import csv
import pandas as pd
import re
# response = requests.get("http://www.omdbapi.com/?apikey=2dd71c99&i=tt3896198")
# data = response.json()
# pprint.pprint(data['Title'])
#
# v=open('movies.csv')
# r=csv.reader(v)
# row0=next(r)
# print(row0)
#
# for item in r[:5]:
#     item.append('added')
#     print(item)
csv_input = pd.read_csv('movies.csv')
csv_input.drop(['domgross','intgross',
       'code', 'budget_2013$', 'domgross_2013$', 'intgross_2013$',
       'period code', 'decade code'], axis=1, inplace=True)
# csv_input = csv_input.drop(columns="budget")
# csv_input = csv_input.drop(columns="domgross")
csv_input['Country']='null'
csv_input['Genre']='null'
csv_input['isUSFilm']=False
csv_input['Production']=''
csv_input['RT_Score']=-1


# print(csv_input[:5])
# print(csv_input.iloc[0].year)
# print(csv_input.shape[0])

row_n=csv_input.shape[0]


def getFromJson(jsondata,jsoncol,default):
    if jsoncol in jsondata:
        return jsondata[jsoncol]
    return default


for i in range(1000,1050):
    imdb=csv_input.iloc[i].imdb
    response=requests.get("http://www.omdbapi.com/?apikey=2dd71c99&i="+ imdb)
    data=response.json()
    # pprint.pprint(data)
    # if 'Country' in data:
    #     country=data['Country']
    # else:
    #     country='null'
    country=getFromJson(data,'Country','null')
    genre=getFromJson(data,'Genre','null')
    production=getFromJson(data,'Production','null')
    isUSA=True
    tomatoes=-1
    if 'Ratings' in data:
        for d in data['Ratings']:
            if d['Source']=='Rotten Tomatoes':
                tomatoes=int(d['Value'].replace('%',''))
                csv_input.at[i,"RT_Score"]=tomatoes
                break

    if 'USA' not in country:
        isUSA=False

    csv_input.at[i,"Country"]=country
    csv_input.at[i,"Genre"]=genre
    csv_input.at[i,"isUSFilm"]=isUSA
    csv_input.at[i,"Production"]=production

#
# print(csv_input[:50])
# print(csv_input.columns)

csv_input.to_csv('bechdel+imdb_test', encoding='utf-8', index=False)
print('csv write complete')
