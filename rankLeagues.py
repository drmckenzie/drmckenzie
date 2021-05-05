# -*- coding: utf-8 -*-
"""

"""

# setting the filters
typeFilter = []
topX = 100
# pvpTopX = 10

import pandas as pd
 
import pokemonMatch as match

# PvPpoke filenames
greatFilename = 'data/great_overall.csv'
remixFilename = 'data/great_remix_overall.csv'
retroFilename = 'data/retro_overall.csv'

ultraFilename = 'data/ultra_overall.csv'
premierFilename = 'data/ultra_premier_overall.csv'
 
masterFilename = 'data/master_overall.csv'
classicFilename = 'data/master_classic_overall.csv'
 
# load data
greatData   =match.getPvpPokeData(greatFilename,typeFilter,topX)
remixData   =match.getPvpPokeData(remixFilename,typeFilter,topX)
retroData   =match.getPvpPokeData(retroFilename,typeFilter,topX)

ultraData   =match.getPvpPokeData(ultraFilename,typeFilter,topX)
premierData =match.getPvpPokeData(ultraFilename,typeFilter,topX)

masterData  =match.getPvpPokeData(masterFilename,typeFilter,topX)
classicData =match.getPvpPokeData(classicFilename,typeFilter,topX)

#reduce data
columnList=["Pokemon","#","Score"]

greatData = greatData[columnList]
ultraData = ultraData[columnList]
masterData = masterData[columnList]
retroData = retroData[columnList]

remixData = remixData[columnList]
classicData = classicData[columnList]
 
greatData.rename(columns={"Score": "GL"},inplace=True)
retroData.rename(columns={"Score": "RL"},inplace=True)
remixData.rename(columns={"Score": "XG"},inplace=True)

ultraData.rename(columns={"Score": "UL"},inplace=True)
premierData.rename(columns={"Score": "PL"},inplace=True)

masterData.rename(columns={"Score": "ML"},inplace=True)
classicData.rename(columns={"Score": "CL"},inplace=True)
 
# add index for all dataframes
greatData   = match.addNewIndexCol(greatData,'GLx')
retroData   = match.addNewIndexCol(retroData,'RLx')
remixData   = match.addNewIndexCol(remixData,'XGx')

ultraData   = match.addNewIndexCol(ultraData,'ULx')
premierData = match.addNewIndexCol(premierData,'PLx')

masterData  = match.addNewIndexCol(masterData,'MLx')
classicData = match.addNewIndexCol(classicData,'CLx')

setGreatsDataTopX  = pd.DataFrame()
setUltrasDataTopX  = pd.DataFrame()
setMastersDataTopX = pd.DataFrame()
 
#merge
mergeList=["Pokemon","#"]
setGreatsDataTopX= greatData.merge(        retroData, left_on=mergeList, right_on=mergeList, how="outer")
setGreatsDataTopX= setGreatsDataTopX.merge(remixData, left_on=mergeList, right_on=mergeList, how="outer")

setUltrasDataTopX=ultraData.merge(premierData, left_on=mergeList, right_on=mergeList, how="outer")
 
setMastersDataTopX=masterData.merge(classicData, left_on=mergeList, right_on=mergeList, how="outer")
 
# control the type:
setGreatsDataTopX.astype({'#': 'int32'}).dtypes
setUltrasDataTopX.astype({'#': 'int32'}).dtypes
setMastersDataTopX.astype({'#': 'int32'}).dtypes
 
#reorder column order:
#setDataTopX = setDataTopX.reindex(columns=['Pokemon','#','GL','GLx','XG','XGx','RL','RLx','UL','ULx','ML','MLx','CL','CLx'])
setGreatsDataTopX  = setGreatsDataTopX.reindex( columns=['Pokemon','#','GL','XG','RL','GLx','XGx','RLx'])
setUltrasDataTopX  = setUltrasDataTopX.reindex( columns=['Pokemon','#','UL','PL','ULx','PLx'])
setMastersDataTopX = setMastersDataTopX.reindex(columns=['Pokemon','#','ML','CL','MLx','CLx'])
                                                         
                                                         
# combine trash data mon:
keepListGreat = [int(i) for i in setGreatsDataTopX['#'] ]
keepListGreat = list(sorted(set(keepListGreat)))
keepListGreatString = match.concatenateListOfMon(keepListGreat)

keepListUltra = [int(i) for i in setUltrasDataTopX['#'] ]
keepListUltra = list(sorted(set(keepListUltra)))
keepListUltraString = match.concatenateListOfMon(keepListUltra)

keepListMaster = [int(i) for i in setMastersDataTopX['#'] ]
keepListMaster = list(sorted(set(keepListMaster)))
keepListMasterString = match.concatenateListOfMon(keepListMaster)

print("\n")
print("For Great leagues, top"+str(topX)+", keep:")
print(keepListGreatString+"CP-1500")

print("\n")
print("For Ultra leagues, top"+str(topX)+", keep:")
print(keepListUltraString+"CP-2500")

print("\n")
print("For Master leagues, top"+str(topX)+", keep:")
print(keepListMasterString)

newData = setDataTopXRank[["Pokemon","#","GLx"]]
newData.sort_values(by=["GLx"], inplace=True, ascending=True)
# extract topX if required:
pvpResult = newData.head(topX)