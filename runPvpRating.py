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
stringHeader += "<p>Leagues:<br>GL=Great League ; \nXG=Remix (great) ; \nRL=Retro (Great) ; \nUL=Ultra League ; \nUP=Premier (Ultra) ; \nML=Master League ; \nCL=Classic Master </p> \n"
stringHeader += "<p>Note: GL is the <b>score</b> in that league (high=good). GLx is the <b>place</b> in that league (low=good). <b>Best</b> is which leagues the pokemon are in the top x of, <b>BestNo</b> is how many leagues. </p>"

# ugh, this is so hacky. Forcing the html formats to behave:
myFormats = {'#': '{:,.0f}'.format,'SumRank': '{:,.0f}'.format,'GLx': '{:,.0f}'.format,'ULx': '{:,.0f}'.format,'MLx': '{:,.0f}'.format,'RLx': '{:,.0f}'.format,'XGx': '{:,.0f}'.format,'CLx': '{:,.0f}'.format}
stringTable = setDataTopX.to_html(classes="sortable", table_id="myTable", index=False, formatters=myFormats)
stringInput =  "\n<input type=\"text\" id=\"myInput\" onkeyup=\"myFunction()\" placeholder=\"Search table for names, moves\"> \n</input> \n"

# concatentate the strings to produce the text:
fileCat = stringHeader + stringInput + stringTable  + stringFooter

# dump to html:
outHtmlFilename = 'Top_X_pokemon_by_leagues.html'
# write html to file
text_file = open(outHtmlFilename, "w")
text_file.write(fileCat)
text_file.close()


# set the league data back to NaN before export:
setDataTopX.loc[setDataTopX['GLx']==999,"GLx"] = np.nan
setDataTopX.loc[setDataTopX['ULx']==999,"ULx"] = np.nan
setDataTopX.loc[setDataTopX['MLx']==999,"MLx"] = np.nan
setDataTopX.loc[setDataTopX['RLx']==999,"RLx"] = np.nan
setDataTopX.loc[setDataTopX['XGx']==999,"XGx"] = np.nan
setDataTopX.loc[setDataTopX['CLx']==999,"CLx"] = np.nan

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


