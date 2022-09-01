
import pokemonMatch as match

thisLeague = 'little'
pvpTopX = 100
# ,'HWx','MXx'
setDataTopXLittleRank  = setDataTopXRank[['Pokemon', '#', 'ELx', 'JJx', 'SumRank', 'Best', 'BestNo']].copy()

# drop nans if all columns are nan
setDataTopXLittleRank = setDataTopXLittleRank.dropna(how='all',subset=['ELx', 'JJx'])
setDataTopXLittleRank = setDataTopXLittleRank.reset_index(drop=True)
                                         
# reindex sumrank
setDataTopXLittleRank['SumRank'] = setDataTopXLittleRank.loc[:,['ELx','JJx']].sum(axis=1)
#colsToOperate = setDataTopXLittleRank.columns[2:-3]
#setDataTopXLittleRank.drop_duplicates(subset=colsToOperate,inplace=True, keep='first')
 
setDataTopXLittleRank["Best"] = ''
setDataTopXLittleRank["BestNo"] = 0

# reorder leagues which are printed out in "best"
setDataTopXLittleRank  = match.whichLeagues(setDataTopXLittleRank ,thisLeague,pvpTopX)
                                
# ugh, this is so hacky. Forcing the html formats to behave:
# sort by rank
rankFormats = {'#': '{:,.0f}'.format,'BestNo': '{:,.0f}'.format,'SumRank': '{:,.0f}'.format,'ELx': '{:,.0f}'.format,'JJx': '{:,.0f}'.format,'PLx': '{:,.0f}'.format,'MLx': '{:,.0f}'.format,'RLx': '{:,.0f}'.format,'XGx': '{:,.0f}'.format,'KLx': '{:,.0f}'.format,'CLx': '{:,.0f}'.format}
rankStringTable = setDataTopXLittleRank.to_html(classes="sortable", table_id="myTable", index=False, formatters=rankFormats)

stringInput =  "\n<input type=\"text\" id=\"myInput\" onkeyup=\"myFunction()\" placeholder=\"Search table for names, moves\"> \n</input> \n"

# concatentate the strings to produce the text:
rankFileCat = stringHeaderRank + stringInput + rankStringTable  + stringFooter


if thisLeague=='little':
    rankHtmlFilename = 'Top_X_pokemon_by_Little_leagues_rank.html'
if thisLeague=='great':
    rankHtmlFilename = 'Top_X_pokemon_by_Great_leagues_rank.html'
if thisLeague=='ultra':
    rankHtmlFilename = 'Top_X_pokemon_by_Ultra_leagues_rank.html'
if thisLeague=='master':
    rankHtmlFilename = 'Top_X_pokemon_by_Master_leagues_rank.html'

# dump to html:
# write html to file
text_file = open(rankHtmlFilename, "w")
text_file.write(rankFileCat)
text_file.close()

