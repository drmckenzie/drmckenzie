
import pokemonMatch as match

thisLeague = 'ultra'
pvpTopX = 100

setDataTopXUltraRank  = setDataTopXRank[['Pokemon', '#', 'PLx', 'ULx', 'SumRank', 'Best', 'BestNo']].copy()

# drop nans if all columns are nan
setDataTopXUltraRank = setDataTopXUltraRank.dropna(how='all',subset=['PLx','ULx'])
setDataTopXUltraRank = setDataTopXUltraRank.reset_index(drop=True)

# reindex sumrank
setDataTopXUltraRank['SumRank'] = setDataTopXUltraRank.loc[:,['PLx','ULx']].sum(axis=1)
#colsToOperate = setDataTopXUltraRank.columns[2:-3]
#setDataTopXUltraRank.drop_duplicates(subset=colsToOperate,inplace=True, keep='first')
 
setDataTopXUltraRank["Best"] = ''
setDataTopXUltraRank["BestNo"] = 0

# reorder leagues which are printed out in "best"
setDataTopXUltraRank  = match.whichLeagues(setDataTopXUltraRank ,thisLeague,pvpTopX)
                                
# ugh, this is so hacky. Forcing the html formats to behave:
# sort by rank
rankFormats = {'#': '{:,.0f}'.format,'BestNo': '{:,.0f}'.format,'SumRank': '{:,.0f}'.format,'GLx': '{:,.0f}'.format,'ULx': '{:,.0f}'.format,'PLx': '{:,.0f}'.format,'MLx': '{:,.0f}'.format,'RLx': '{:,.0f}'.format,'XGx': '{:,.0f}'.format,'KLx': '{:,.0f}'.format,'CLx': '{:,.0f}'.format}
rankStringTable = setDataTopXUltraRank.to_html(classes="sortable", table_id="myTable", index=False, formatters=rankFormats)

stringInput =  "\n<input type=\"text\" id=\"myInput\" onkeyup=\"myFunction()\" placeholder=\"Search table for names, moves\"> \n</input> \n"

# concatentate the strings to produce the text:
rankFileCat = stringHeaderRank + stringInput + rankStringTable  + stringFooter


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

