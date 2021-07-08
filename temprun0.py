
myDF = setDataTopXRank

minmax = 'min'


# go through the data, for each pokemon, keep the higest score in each column.
listOfPokemon = myDF["Pokemon"]
listOfPokemon = list(set(listOfPokemon))
#listOfPokemon = ["Machamp","Medicham"]
colsToOperate = myDF.columns[2:-3]
for mon in listOfPokemon:
    print(mon)
    for col in colsToOperate:
        if minmax.lower() == "min":
            minmaxValue = myDF.loc[myDF.Pokemon==mon,col].min()
        if minmax.lower() == "max":
            minmaxValue = myDF.loc[myDF.Pokemon==mon,col].max()
        #print(minValue)
        # set all column at this min value
        myDF.loc[myDF.Pokemon==mon,col]=minmaxValue