# -*- coding: utf-8 -*-
"""
 
"""

import pandas as pd
import numpy as np
import pokemonMatch as match

# setting the filters
typeFilter = []
topX = 0

pvpTopX = 100

setDataTopX,keepList,trashList = match.calculatePvpRating(typeFilter,topX,pvpTopX)


# set this back to something else for table sorting:

## make the NaN a big value:
#setDataTopX.loc[setDataTopX['GLx'].isna(),"GLx"] = ''
#setDataTopX.loc[setDataTopX['ULx'].isna(),"ULx"] = ''
#setDataTopX.loc[setDataTopX['MLx'].isna(),"MLx"] = ''
#setDataTopX.loc[setDataTopX['RLx'].isna(),"RLx"] = ''
#setDataTopX.loc[setDataTopX['XGx'].isna(),"XGx"] = ''
#setDataTopX.loc[setDataTopX['CLx'].isna(),"CLx"] = ''

# three bits to the file:header, middle and footer
header = "html//header.html"
footer = "html//footer.html"
# read the files:
f = open(header,"r")
stringHeader = f.read()
f.close()

f = open(footer,"r")
stringFooter = f.read()
f.close()

stringHeader += "<p>Best Pokemon Go moves for PvP (league battles), results for top "+str(int(pvpTopX))+" pokemon in each league listed</p> \n\n <p>Search on all fields of the table: Name, Number, Score. <b>(click table header to sort)</b> </p> \n \n"
stringHeader += "<p>Leagues:<br>GL=Great League ; \nXG=Remix (great) ; \nRL=Retro (Great) ; \nUL=Ultra League ; \nPL=Premier (Ultra) ; \nML=Master League ; \nCL=Classic Master </p> \n"
stringHeaderScore = stringHeader + "<p>Note: GL is the <b>score</b> in that league (high=good). "
stringHeaderRank = stringHeader + "GLx is the <b>place</b> in that league (low=good). "
stringHeaderFinal = "<b>Best</b> is which leagues the pokemon are in the top x of, <b>BestNo</b> is how many leagues. </p>"
stringHeaderScore += stringHeaderFinal
stringHeaderRank += stringHeaderFinal

setDataTopXRank  = setDataTopX[['Pokemon', '#', 'GLx', 'XGx', 'RLx', 'KLx', 'ULx', 'PLx', 'MLx', 'CLx', 'SumRank', 'Best', 'BestNo']].copy()
setDataTopXScore = setDataTopX[['Pokemon', '#', 'GL',  'XG',  'RL',  'KL',  'UL',  'PL',  'ML',  'CL',  'SumRank', 'Best', 'BestNo']].copy()

# go through the data, for each pokemon, keep the higest score in each column.
setDataTopXRank  = match.dropDuplicatesPlz(setDataTopXRank,"min")
setDataTopXScore = match.dropDuplicatesPlz(setDataTopXScore,"max")

# reindex sumrank
setDataTopXRank['SumRank'] = setDataTopXRank.loc[:,['GLx','XGx','RLx','KLx','ULx','PLx','MLx','CLx']].sum(axis=1)
colsToOperate = setDataTopXRank.columns[2:-3]
setDataTopXRank.drop_duplicates(subset=colsToOperate,inplace=True, keep='first')
 
setDataTopXScore['SumRank'] = setDataTopXScore.loc[:,['GL','XG','RL','KL','UL','PL','ML','CL']].sum(axis=1)
colsToOperate = setDataTopXScore.columns[2:-3]
setDataTopXScore.drop_duplicates(subset=colsToOperate,inplace=True, keep='first')
                                
# ugh, this is so hacky. Forcing the html formats to behave:
# sort by rank
rankFormats = {'#': '{:,.0f}'.format,'SumRank': '{:,.0f}'.format,'GLx': '{:,.0f}'.format,'ULx': '{:,.0f}'.format,'PLx': '{:,.0f}'.format,'MLx': '{:,.0f}'.format,'RLx': '{:,.0f}'.format,'XGx': '{:,.0f}'.format,'KLx': '{:,.0f}'.format,'CLx': '{:,.0f}'.format}
rankStringTable = setDataTopXRank.to_html(classes="sortable", table_id="myTable", index=False, formatters=rankFormats)
# sort by score
scoreFormats = {'#': '{:,.0f}'.format,'SumRank': '{:,.0f}'.format,'GL': '{:,.0f}'.format,'UL': '{:,.0f}'.format,'PL': '{:,.0f}'.format,'ML': '{:,.0f}'.format,'RL': '{:,.0f}'.format,'XG': '{:,.0f}'.format,'KL': '{:,.0f}'.format,'CL': '{:,.0f}'.format}
scoreStringTable = setDataTopXScore.to_html(classes="sortable", table_id="myTable", index=False, formatters=scoreFormats)

stringInput =  "\n<input type=\"text\" id=\"myInput\" onkeyup=\"myFunction()\" placeholder=\"Search table for names, moves\"> \n</input> \n"

# concatentate the strings to produce the text:
rankFileCat = stringHeaderRank + stringInput + rankStringTable  + stringFooter
scoreFileCat = stringHeaderScore + stringInput + scoreStringTable  + stringFooter

# dump to html:
rankHtmlFilename = 'Top_X_pokemon_by_leagues_rank.html'
# write html to file
text_file = open(rankHtmlFilename, "w")
text_file.write(rankFileCat)
text_file.close()

scoreHtmlFilename = 'Top_X_pokemon_by_leagues_score.html'
text_file = open(scoreHtmlFilename, "w")
text_file.write(scoreFileCat)
text_file.close()

# set the league data back to NaN before export:
setDataTopX.loc[setDataTopX['GLx']==999,"GLx"] = np.nan
setDataTopX.loc[setDataTopX['ULx']==999,"ULx"] = np.nan
setDataTopX.loc[setDataTopX['MLx']==999,"MLx"] = np.nan
setDataTopX.loc[setDataTopX['RLx']==999,"RLx"] = np.nan
setDataTopX.loc[setDataTopX['XGx']==999,"XGx"] = np.nan
setDataTopX.loc[setDataTopX['CLx']==999,"CLx"] = np.nan
setDataTopX.loc[setDataTopX['PLx']==999,"PLx"] = np.nan
setDataTopX.loc[setDataTopX['KLx']==999,"KLx"] = np.nan

# dump this to CSV file, top directory:
outCsvFilename = 'csv_Top_X_pokemon_by_leagues.csv'
setDataTopX.to_csv(outCsvFilename)

print("The score cutoff for top number of pokemon in the league is set at top: "+str(pvpTopX))
print("")
 
# combine keep / trash data mon:
keepListString = match.concatenateListOfMon(keepList)
trashListString = match.concatenateListOfMon(trashList)

print("This is the list to KEEP pokemon for PvP - any ranked below the top "+str(pvpTopX))
print(keepListString)
print("")
print("This is the list to TRASH pokemon not for PvP - ALL ranked above the top "+str(pvpTopX))
print(trashListString)


allLeagues = ['GLx','XGx','RLx','KLx','ULx','PLx','MLx','CLx']

# return the top 100 PVP pokemon
leagueRankFilename = 'allLeaguesRankedPokemonSearchString100.txt'
text_file = open(leagueRankFilename, "w")
text_file.write("\n all Leagues Ranked - Pokemon Search String - top 100 \n")
for lg in allLeagues:
    printThis = match.printTopxForLeague(setDataTopXRank,lg,pvpTopX)
    print(printThis)
    text_file.write(printThis)
text_file.close()

# return the top 10 PVP pokemon
pvpTopX = 10
leagueRankFilename = 'allLeaguesRankedPokemonSearchString10.txt'
text_file = open(leagueRankFilename, "w")
text_file.write("\n all Leagues Ranked - Pokemon Search String - top 10 \n")
for lg in allLeagues:
    printThis = match.printTopxForLeague(setDataTopXRank,lg,pvpTopX)
    print(printThis)
    text_file.write(printThis)
text_file.close()
