# -*- coding: utf-8 -*-
"""PvPrating.py

Original file is located at
    https://drmckenzie.github.io/

# Pokemon Match (PvP)

This file calculates the best leagues for pokemon for battle (PvP). It lists:
- a summary of the pokemon for each league
- a combined summary of all pokemon of all types at the end

"""

# This controls the score filter:
pvpFilter = 80
 
# This controls the filter taking the top however many of the leage results, e.g. top 100:
pvpTopX = 10

import pandas as pd
import pokemonMatch as match
 
# PvPpoke filenames
greatFilename = 'data/great_overall.csv'
ultraFilename = 'data/ultra_overall.csv'
masterFilename = 'data/master_overall.csv'
retroFilename = 'data/retro_overall.csv'
 
remixFilename = 'data/great_remix_overall.csv'
classicFilename = 'data/master_classic_overall.csv'
 
# setting the filters
typeFilter = []
topX = 0
 
# load data
greatData=match.getPvpPokeData(greatFilename,typeFilter,topX)
ultraData=match.getPvpPokeData(ultraFilename,typeFilter,topX)
masterData=match.getPvpPokeData(masterFilename,typeFilter,topX)
retroData=match.getPvpPokeData(retroFilename,typeFilter,topX)
 
remixData=match.getPvpPokeData(remixFilename,typeFilter,topX)
classicData=match.getPvpPokeData(classicFilename,typeFilter,topX)

#reduce data
columnList=["Pokemon","#","Score"]

greatData = greatData[columnList]
ultraData = ultraData[columnList]
masterData = masterData[columnList]
retroData = retroData[columnList]

remixData = remixData[columnList]
classicData = classicData[columnList]
 
greatData.rename(columns={"Score": "GL"},inplace=True)
ultraData.rename(columns={"Score": "UL"},inplace=True)
masterData.rename(columns={"Score": "ML"},inplace=True)
retroData.rename(columns={"Score": "RL"},inplace=True)
 
remixData.rename(columns={"Score": "XG"},inplace=True)
classicData.rename(columns={"Score": "CL"},inplace=True)
 
# add index for all dataframes
greatData = match.addNewIndexCol(greatData,'GLx')
ultraData = match.addNewIndexCol(ultraData,'ULx')
masterData = match.addNewIndexCol(masterData,'MLx')
retroData = match.addNewIndexCol(retroData,'RLx')

remixData = match.addNewIndexCol(remixData,'XGx')
classicData = match.addNewIndexCol(classicData,'CLx')

setData = pd.DataFrame()
 
#merge
mergeList=["Pokemon","#"]
setData=greatData.merge(ultraData, left_on=mergeList, right_on=mergeList, how="outer")
setData=setData.merge(masterData, left_on=mergeList, right_on=mergeList, how="outer")
setData=setData.merge(retroData, left_on=mergeList, right_on=mergeList, how="outer")

setData=setData.merge(remixData, left_on=mergeList, right_on=mergeList, how="outer")
setData=setData.merge(classicData, left_on=mergeList, right_on=mergeList, how="outer")

# control the type:
setData.astype({'#': 'int32'}).dtypes

#reorder column order:
#setData = setData.reindex(columns=['Pokemon','#','GL','GLx','UL','ULx','ML','MLx','RL','RLx'])
setData = setData.reindex(columns=['Pokemon','#','GL','GLx','XG','XGx','RL','RLx','UL','ULx','ML','MLx','CL','CLx'])
#setData = setData.reindex(columns=['Pokemon','#','GL','UL','ML','RL','GLx','ULx','MLx','RLx'])
setData = setData.reindex(columns=['Pokemon','#','GL','XG','RL','UL','ML','CL','GLx','XGx','RLx','ULx','MLx','CLx'])

# control what gets shown:
StP = str(pvpFilter)
dispData  = setData.query('GL>='+StP+' or XG>='+StP+' or RL>='+StP+' or UL>='+StP+' or ML>='+StP+' or CL>='+StP )
trashData = setData.query('GL<'+StP+' and XG<'+StP+' and RL<'+StP+' and UL<'+StP+' and ML<'+StP+' and CL<'+StP  )
 
setDataTopX = pd.DataFrame()
 
#merge
mergeList=["Pokemon","#"]
setDataTopX=  greatData.merge(ultraData, left_on=mergeList, right_on=mergeList, how="outer")
setDataTopX=setDataTopX.merge(masterData, left_on=mergeList, right_on=mergeList, how="outer")
setDataTopX=setDataTopX.merge(retroData, left_on=mergeList, right_on=mergeList, how="outer")
 
setDataTopX=setDataTopX.merge(remixData, left_on=mergeList, right_on=mergeList, how="outer")
setDataTopX=setDataTopX.merge(classicData, left_on=mergeList, right_on=mergeList, how="outer")
 
# control the type:
setDataTopX.astype({'#': 'int32'}).dtypes
 
#reorder column order:
#setDataTopX = setDataTopX.reindex(columns=['Pokemon','#','GL','GLx','XG','XGx','RL','RLx','UL','ULx','ML','MLx','CL','CLx'])
setDataTopX = setDataTopX.reindex(columns=['Pokemon','#','GL','XG','RL','UL','ML','CL','GLx','XGx','RLx','ULx','MLx','CLx'])
 
import numpy as np
 
# rank them by usefulness
setDataTopX['SumRank'] = setDataTopX.loc[:,['GLx','XGx','RLx','ULx','MLx','CLx']].sum(axis=1)
setDataTopX.loc[setDataTopX['SumRank'] == 0] = np.nan
setDataTopX.sort_values(by=['SumRank'],ascending=True,inplace=True)
 
# make the NaN a big value:
setDataTopX.loc[setDataTopX['GLx'].isna(),"GLx"] = 999
setDataTopX.loc[setDataTopX['ULx'].isna(),"ULx"] = 999
setDataTopX.loc[setDataTopX['MLx'].isna(),"MLx"] = 999
setDataTopX.loc[setDataTopX['RLx'].isna(),"RLx"] = 999
 
setDataTopX.loc[setDataTopX['XGx'].isna(),"XGx"] = 999
setDataTopX.loc[setDataTopX['CLx'].isna(),"CLx"] = 999
 
# control what gets shown:
StX = str(pvpTopX)
#dispDataTopX = setDataTopX.query('GLx <= 5' )
#trashDataTopX = setDataTopX.query('GLx > 10')+str(pvpTopX) )
 
dispDataTopX  = setDataTopX.query('GLx<='+StX+' or XGx<='+StX+' or RLx<='+StX+' or ULx<='+StX+' or MLx<='+StX+' or CLx<='+StX )
trashDataTopX = setDataTopX.query('GLx>'+StX+' and XGx>'+StX+' and RLx>'+StX+' and ULx>'+StX+' and MLx>'+StX+' and CLx>'+StX  )
 
print("The score cutoff for top number of pokemon in the league is set at top: "+str(pvpTopX))
print("")
 
# combine trash data mon:
keepList = [int(i) for i in dispDataTopX['#'] ]
keepList = list(sorted(set(keepList)))
keepListString = match.concatenateListOfMon(keepList)
print("This is the list to KEEP pokemon for PvP - any ranked below the top "+str(pvpTopX))
print(keepListString)
 
print("")
 
# combine trash data mon:
trashList = [int(i) for i in trashDataTopX['#'] ]
trashList = list(sorted(set(trashList)))
 
#print(trashList)
 
trashListString = match.concatenateListOfMon(trashList)
print("This is the list to TRASH pokemon not for PvP - ALL ranked above the top "+str(pvpTopX))
print(trashListString)

# which leagues is good for this pokemon?
# using the top x result, I think this is more consistent.
setDataTopX["Best"] = ''
setDataTopX["BestNo"] = 0
for i in range(len(setDataTopX)):
    setDataTopX.loc[i,"Best"] = [['']]
    if setDataTopX.loc[i,"GLx"]<pvpTopX:
        setDataTopX.loc[i,"Best"].append("GL")
    if setDataTopX.loc[i,"XGx"]<pvpTopX:
        setDataTopX.loc[i,"Best"].append("XG")
    if setDataTopX.loc[i,"RLx"]<pvpTopX:
        setDataTopX.loc[i,"Best"].append("RL")
    if setDataTopX.loc[i,"ULx"]<pvpTopX:
        setDataTopX.loc[i,"Best"].append("UL")
    if setDataTopX.loc[i,"MLx"]<pvpTopX:
        setDataTopX.loc[i,"Best"].append("ML")
    if setDataTopX.loc[i,"CLx"]<pvpTopX:
        setDataTopX.loc[i,"Best"].append("CL")
    if setDataTopX.loc[i,"Best"]==['']:
        setDataTopX.loc[i,"Best"].append("-")
    # remove the first ''
    setDataTopX.loc[i,"Best"].pop(0)
    setDataTopX.loc[i,"BestNo"] = len(setDataTopX.loc[i,"Best"])
 
 
setDataTopX.sort_values(by=['BestNo','SumRank'],ascending=(False,True),inplace=True)
 
# dump this to CSV file, top directory:
outCsvFilename = '../csv_Top_X_pokemon_by_leagues.csv'
setDataTopX.to_csv(outCsvFilename)
 
setDataTopX.head(200)

"""Need to do something that separates the different types of Pokémon, Shadow, alolan etc to make copy paste easier.

Also need to separate leagues, group great leagues together etc.
"""