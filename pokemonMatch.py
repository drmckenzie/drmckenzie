# -*- coding: utf-8 -*-
"""
Created on Fri Mar 12 10:28:31 2021

"""

def runAllTypesTopX(calcyFilename,gamepressFilename,topX):
    """ 
    Inputs: filenames of calcyIV and gamepress csv files. Select top X results 
    Method: goes through the calcy database and matches any from the gampress
    database that has the best attacking moves (defined by DPS^3*TDO)
    Output: For each type, returns ratio of pokemon with best moves.
    """    
    
    typeList = ["Normal", "Fire", "Water", "Grass", "Flying", "Fighting", "Poison", "Electric", "Ground", "Rock", "Psychic", "Ice", "Bug", "Ghost", "Steel", "Dragon", "Dark", "Fairy"]
    
    import pandas as pd
    
    allData = pd.DataFrame(columns=["Pokemon","#","Type","Count","Caught","DPS^3*TDO"])
    
    for typeFilter in typeList:
        Result,topResult = calculatePokemonWithBestMoves(calcyFilename,gamepressFilename,typeFilter,topX)

        # get the data we're interested in. Name and score
        ResultTopX = Result[["Pokemon","#","Fast move","Special move","DPS^3*TDO"]].copy()
          
        # NOTE: this controls whether we see the same pokemon with different moves in the result
        #TODO make this a flag
        # ResultTopX.drop_duplicates(subset=['Pokemon','#'], inplace=True)  
                                           
        if len(ResultTopX)==0:
            ResultTopX = pd.DataFrame(columns=["Pokemon","#","Type","Fast move","Special move","Count","Caught","DPS^3*TDO"])
            ResultTopX.loc[0] = ['',0,typeFilter,"","",0,'No',1]
        else:
            ResultTopX["Count"] = 1
                                           
        ResultTopX["Type"] = typeFilter
        ResultTopX["Caught"] = "Yes"
        
        # get the difference, what we have not caught:
        notCaught = topResult[topResult.Pokemon.isin(Result.Pokemon) == False]
        notCaughtTopX = notCaught[["Pokemon","#","Fast move","Special move","DPS^3*TDO"]].copy()
        notCaughtTopX["Type"] = typeFilter
        notCaughtTopX["Caught"] = "No"
        notCaughtTopX["Count"] = "1"
        
        allData = pd.concat([allData,ResultTopX,notCaughtTopX],sort=False)
              
        foundTypeTopX = "You have the top "+str(len(ResultTopX))+" of the "+str(topX)+" most powerful "+typeFilter+" type Pokemon"                                   
        print(foundTypeTopX)
        
    return allData

def getGamepressData(gamepressFilename,typeFilter,topX):
    """ 
    Inputs: filenames of gamepress csv files 
    Method: goes through the gamepress database and loads. Filters by type.
    Output: Results dataframe of pokemon sorted by "DPS^3*TDO" and filtered by type.
    """    
    
    if (topX==[]):
        topX = 999999999
    
    # import csv sheet
    import pandas as pd
    
    # read the csv files into dataframes
    gamepressData = pd.read_csv(gamepressFilename, encoding='utf8')
    
    # get the data we're interested in. Name and score
    gamepress = gamepressData[["Pokemon","Fast Move","Charged Move","DPS","TDO","DPS^3*TDO"]]
    
    #TODO do something with Geodude Normal etc.
       
    # rename columns                                 
    gamepress = gamepress.rename(columns={'Charged Move': 'Special move'})
    gamepress = gamepress.rename(columns={'Fast Move': 'Fast move'})
    
    # Duplicate the special move column for later on
    gamepress['Special move 2'] = gamepress['Special move']
    
    # get the number, type and name from the lookup:
    PokemonNoType =  getPokemonNumberType()

    # match pokemon to type:
    gamepressType = gamepress.merge(PokemonNoType,how='inner', on=['Pokemon'])
     
    if typeFilter==[]:
        gpResultBoth = gamepressType.copy()
    else:
        # filter by type. Careful, there's two columns.
        gpResult1 = gamepressType[gamepressType["Type1"]==typeFilter]
        gpResult2 = gamepressType[gamepressType["Type2"]==typeFilter]
           
        gpResultBoth = pd.concat([gpResult1,gpResult2],sort=False)
        
        # NOTE: this controls whether we see the same pokemon with different moves in the result
        #TODO make this a flag
        #gpResultBoth.drop_duplicates(subset=['Pokemon','#'], inplace=True)
        
    # sort by ..
    gpResultBoth.sort_values(by=["DPS^3*TDO",'#'], inplace=True, ascending=False)

    # extract topX if required:
    if (topX>0)&( topX<=len(gpResultBoth) ):
            gpResult = gpResultBoth.head(topX)
    else:
        gpResult = gpResultBoth.copy()
                                 
    return gpResult


def getPvpPokeData(pvpPokeFilename,typeFilter,topX):
    """ 
    Inputs: filenames of gamepress csv files 
    Inputs column: Pokemon	Score	Type 1	Type 2	Attack	Defense	Stamina	Stat Product	Level	Fast Move	Charged Move 1	Charged Move 2
    Method: goes through the gamepress database and loads. Filters by type (of pokemon).
    Output: Results dataframe of pokemon sorted by "DPS^3*TDO" and filtered by type.
    """    
    
    if (topX==[]):
        topX = 999999999
    
    # import csv sheet
    import pandas as pd
    
    # read the csv files into dataframes
    pvpPokeData = pd.read_csv(pvpPokeFilename, encoding='utf8')
    
    # get the data we're interested in. Name and score
    pvpPoke = pvpPokeData[["Pokemon","Fast Move","Charged Move 1","Charged Move 2","Score","Level"]]
    
    #TODO do something with Geodude Normal etc.
       
    # rename columns                                 
    # pvpPoke = pvpPoke.rename(columns={'Charged Move 1': 'Special move'})
    #pvpPoke = pvpPoke.rename(columns={'Fast Move': 'Fast move'})
    
    # get the number, type and name from the lookup:
    PokemonNoType =  getPokemonNumberType()

    # match pokemon to type:
    pvpPokeType = pvpPoke.merge(PokemonNoType,how='inner', on=['Pokemon'])
     
    if typeFilter==[]:
        pvpResultBoth = pvpPokeType.copy()
    else:
        # filter by type. Careful, there's two columns.
        pvpResult1 = pvpPokeType[pvpPokeType["Type1"]==typeFilter]
        pvpResult2 = pvpPokeType[pvpPokeType["Type2"]==typeFilter]
           
        pvpResultBoth = pd.concat([pvpResult1,pvpResult2],sort=False)
        
        # NOTE: this controls whether we see the same pokemon with different moves in the result
        #TODO make this a flag
        #gpResultBoth.drop_duplicates(subset=['Pokemon','#'], inplace=True)
        
    # sort by ..
    pvpResultBoth.sort_values(by=["Score"], inplace=True, ascending=False)

    # extract topX if required:
    if (topX>0)&( topX<=len(pvpResultBoth) ):
            pvpResult = pvpResultBoth.head(topX)
    else:
        pvpResult = pvpResultBoth.copy()
        
    # drop nans if all columns are nan
    pvpResult = pvpResult.dropna(how='all')
                                 
    return pvpResult


def calculatePokemonWithBestMoves(calcyFilename,gamepressFilename,typeFilter,topX):
    """ 
    Inputs: filenames of calcyIV and gamepress csv files 
    Method: goes through the calcy database and matches any from the gampress
    database that has the best attacking moves (defined by DPS^3*TDO)
    Output: Results dataframe of matched pokemon with best moves.
    """    
    
    # import csv sheet
    import pandas as pd
    
    gamepress = getGamepressData(gamepressFilename,typeFilter,topX)
    
    # read the csv files into dataframes
    calcyData = pd.read_csv(calcyFilename, encoding='utf8')
    
    # get the data we're interested in. Name and score
    calcy = calcyData[["Name","Nr","Fast move","Special move","Special move 2","CP","Saved","Lucky","ShadowForm"]]
    
    # drop those that are not saved:
    calcy = calcy[calcy["Saved"]==1]
    
    #TODO do something with Geodude Normal etc.
       
    # rename shadow and XL to remove the quotation marks
    #calcy['Shadow'] = calcy['Shadow'].str.replace(r'"', '')
    
    # rename columns                                 
    calcy = calcy.rename(columns={'Name': 'Pokemon'})
    calcy = calcy.rename(columns={'Nr': '#'})
    
    # drop any blank fast/special moves:
    calcy = calcy[~calcy["Fast move"].str.startswith('-')]
    calcy = calcy[~calcy["Fast move"].str.startswith(" -")]
    calcy = calcy[~calcy["Special move"].str.startswith("-")]
    calcy = calcy[~calcy["Special move"].str.startswith(' -')]
    
    # rename - whitespace. Infuriating
    calcy['Fast move'] = calcy['Fast move'].str.replace(r'-', ' ')
    calcy['Special move'] = calcy['Special move'].str.replace(r'-', ' ')
    calcy['Special move 2'] = calcy['Special move 2'].str.replace(r'-', ' ')
    
    # move the "shadow" tag to the front rather than the back
    calcyShadowFound = calcy['Pokemon'].str.endswith('Shadow').copy()
    calcy['Pokemon'] = calcy['Pokemon'].str.replace(r' Shadow', '')
    calcy.loc[calcyShadowFound,'Pokemon'] = 'str' + calcy.loc[calcyShadowFound,'Pokemon'].astype(str)
    
    # filter for testing:
    # calcy = calcy[calcy["Pokemon"].str.startswith('Rhyp')]
    
    # merge : this needs to be a 2 step process
    Result1 = calcy.merge(gamepress,how='inner', on=['Pokemon',"#",'Fast move','Special move'])
    
    Result2 = calcy.merge(gamepress,how='inner', on=['Pokemon',"#",'Fast move','Special move 2'])
    
    # rename columns
    Result1 = Result1.rename(columns={'Special move 2_x': 'Special move 2'})
    Result1 = Result1.rename(columns={'Special move 2_y': 'Temp'})
    Result2 = Result2.rename(columns={'Special move_x': 'Special move'})
    Result2 = Result2.rename(columns={'Special move_y': 'Temp'})
    
    Result = pd.concat([Result1,Result2],sort=False)
    
    # drop the column
    Result.drop(columns=['Temp'], inplace=True)
    
    # drop duplicates - WARNING, may drop some pokemon with second special moves
    #TODO - maybe do this better??
    Result.drop_duplicates(subset=['Pokemon','CP'], inplace=True)
    
    # print(Result)
    
    # sort by ..
    Result.sort_values(by=['#', 'CP'], inplace=True)
                           
    # get the number, type and name from the lookup:
    #PokemonNoType =  getPokemonNumberType()

    # match pokemon to type:
    #ResultType = Result.merge(PokemonNoType,how='inner', on=['Pokemon',"#"])
                                        
    return Result,gamepress

def calcyImportAndReturnTopNumbers(calcyFilename,allData):
    """ 
    Inputs: filenames of calcyIV csv files and allData (pre-sorted DataFrame with x number of top pokemon attackers by type) 
    Method: goes through the calcy database and matches any from the gampress
    database that has the best attacking moves (defined by DPS^3*TDO)
    Output: Results dataframe of matched pokemon with best moves.
    """    
    
    # import csv sheet
    import pandas as pd
    
    # read the csv files into dataframes
    calcyData = pd.read_csv(calcyFilename, encoding='utf8')
    
    # get the data we're interested in. Name and score
    calcy = calcyData[["Name","Nr","Fast move","Special move","Special move 2","CP","Saved","Lucky","ShadowForm"]]
    
    # drop those that are not saved:
    calcy = calcy[calcy["Saved"]==1]
    
    #TODO do something with Geodude Normal etc.
       
    # rename shadow and XL to remove the quotation marks
    #calcy['Shadow'] = calcy['Shadow'].str.replace(r'"', '')
    
    # rename columns                                 
    calcy = calcy.rename(columns={'Name': 'Pokemon'})
    calcy = calcy.rename(columns={'Nr': '#'})
    
    # drop any blank fast/special moves:
    calcy = calcy[~calcy["Fast move"].str.startswith('-')]
    calcy = calcy[~calcy["Fast move"].str.startswith(" -")]
    calcy = calcy[~calcy["Special move"].str.startswith("-")]
    calcy = calcy[~calcy["Special move"].str.startswith(' -')]
    
    # rename - whitespace. Infuriating
    calcy['Fast move'] = calcy['Fast move'].str.replace(r'-', ' ')
    calcy['Special move'] = calcy['Special move'].str.replace(r'-', ' ')
    calcy['Special move 2'] = calcy['Special move 2'].str.replace(r'-', ' ')
    
    # move the "shadow" tag to the front rather than the back
    calcyShadowFound = calcy['Pokemon'].str.endswith('Shadow').copy()
    calcy['Pokemon'] = calcy['Pokemon'].str.replace(r' Shadow', '')
    calcy.loc[calcyShadowFound,'Pokemon'] = 'str' + calcy.loc[calcyShadowFound,'Pokemon'].astype(str)

    # create shadow tag
    calcy["Shadow"] = False
    calcy.loc[calcyShadowFound,'Shadow'] = True
    
    # filter for testing:
    # calcy = calcy[calcy["Pokemon"].str.startswith('Rhyp')]
    
    # merge : this needs to be a 2 step process
    Result1 = calcy.merge(allData,how='inner', on=['Pokemon',"#",'Fast move','Special move'])
    
    Result2 = calcy.merge(allData,how='inner', on=['Pokemon',"#",'Fast move','Special move 2'])
    
    # rename columns
    Result1 = Result1.rename(columns={'Special move 2_x': 'Special move 2'})
    Result1 = Result1.rename(columns={'Special move 2_y': 'Temp'})
    Result2 = Result2.rename(columns={'Special move_x': 'Special move'})
    Result2 = Result2.rename(columns={'Special move_y': 'Temp'})
    
    Result = pd.concat([Result1,Result2],sort=False)
    
    # drop the column
    Result.drop(columns=['Temp'], inplace=True)
    
    # drop duplicates - WARNING, may drop some pokemon with second special moves
    #TODO - maybe do this better??
    Result.drop_duplicates(subset=['Pokemon','CP'], inplace=True)
    
    # print(Result)
    
    # sort by ..
    Result.sort_values(by=['#', 'CP'], inplace=True)
                           
    # get the number, type and name from the lookup:
    #PokemonNoType =  getPokemonNumberType()

    # match pokemon to type:
    #ResultType = Result.merge(PokemonNoType,how='inner', on=['Pokemon',"#"])
                                        
    return Result



def getNoCpFromResults(Result):
    """ 
    Input: Result dataframe 
    Method: spit out the list of all pokemon that have the best moves in the
    format number and CP for entering into the Pokemon Go search bar.
    e.g. 1,2,3,50&CP20,CP40,CP50,CP60
    Output: CSV file (all results) and text file (above string).
    """    
        
    # filtering to get the # an CP
    ResultsCP = Result[["Pokemon","#","CP"]]
    # get a unique list of pokemon:
    ResultsPokemon = list(Result.Pokemon.unique())

    # print the # and CP list to file:
    keepFileNoCP = 'results_pokemon_No_CP_best_moves.txt'
    with open(keepFileNoCP, 'w') as file:
        file.write('')
        #file.write(ResultsPokemonCPBestMoves)
    
    #iterate to get CP values:
    iter = 0
    strNo = ''
    strCP = ''
    ResultsPokemonCPBestMoves = ''
    
    # how many chunks do we want?
    splitEvery = 7
    
    for pokemon in ResultsPokemon:
        iter = iter + 1
        
        if iter >= (splitEvery+1):
            with open(keepFileNoCP, 'a') as file:
                file.write(ResultsPokemonCPBestMoves)
                file.write('\n')
                file.write('\n')
            strNo = ''
            strCP = ''
            iter = 0
        
        getNo = ResultsCP[ResultsCP["Pokemon"]==pokemon]["#"].unique() 
        getCP = ResultsCP[ResultsCP["Pokemon"]==pokemon]["CP"].unique()
        strNo = str(strNo)+str(*getNo)+','
        for cp in getCP:
            strCP = strCP+'CP'+str(cp)+','
            
        ResultsPokemonCPBestMoves = strNo[:-1] + "&" + strCP[:-1]

    return
    
def getPokemonNumberType():
    """ 
    Input: none 
    Method: inputs database of pokemon information.
    Output: lookup table of pokemon and type.
    """    

    # import csv sheet
    import pandas as pd
    
    # filenames
    #csvFilename = 'great_overall.csv'
    lookupFilename = 'Pokemon_Lookup.csv'
    
    # read the csv files into dataframes
    # rawData = pd.read_csv(csvFilename, encoding='utf8')
    lookupData = pd.read_csv(lookupFilename, encoding='utf8')
    
    # drop nan s from these columns
    lookupData = lookupData.dropna(subset=['#'])
    # the lookup data should be integers
    lookupData.astype({'#': 'int32'}).dtypes
    
    lookupNameNumber = lookupData[["Name","#","Type 1","Type 2","Released_2021_03_13"]]
                                   
    # drop those that are not released yet:
    lookupNameNumber = lookupNameNumber[lookupNameNumber["Released_2021_03_13"]==True]
    
    # rename for better handling of spaces:
    lookupNameNumber.rename(columns={"Type 1": "Type1"}, inplace=True)
    lookupNameNumber.rename(columns={"Type 2": "Type2"}, inplace=True)
                                   
    # duplicate this list because of the way Gamepress do the shadow names
    lookupNameNumberShadow = lookupNameNumber.copy()
    lookupNameNumberShadow['Name'] = 'Shadow ' + lookupNameNumberShadow['Name'].astype(str)
    
    # duplicate this list because of the way Gamepress do the shadow names
    lookupNameNumberShadowPVP = lookupNameNumber.copy()
    lookupNameNumberShadowPVP['Name'] = lookupNameNumberShadowPVP['Name'].astype(str)+' (Shadow)'
    
    lookupNameNumberBoth = pd.concat([lookupNameNumber,lookupNameNumberShadow,lookupNameNumberShadowPVP])
    
    lookupNameNumberBoth.drop_duplicates(subset=['Name','#'], inplace=True)
                                                 
    lookupNameNumberBoth.rename(columns={'Name': 'Pokemon'}, inplace=True)
                                   
    return lookupNameNumberBoth

def getListOfPokemonNotCaught(calcyFilename,gamepressFilename):
    
    # import csv sheet
    import pandas as pd
    
    # switch off copy warning
    pd.set_option("mode.chained_assignment",None)
    
    # read the csv files into dataframes
    calcyData = pd.read_csv(calcyFilename, encoding='utf8')
    
    # read the csv files into dataframes
    gamepressData = pd.read_csv(gamepressFilename, encoding='utf8')
    
    # get the data we're interested in. Name and score
    gamepress = gamepressData[["Pokemon","Fast Move","Charged Move","DPS","TDO","DPS^3*TDO"]]
    # drop duplicates - 
    gamepress.drop_duplicates(subset=['Pokemon'], inplace=True)
    
    # get the data we're interested in. Name and score
    #calcy = calcyData[["Name","Nr","Fast move","Special move","Special move 2","CP","Saved","Lucky","ShadowForm"]]
    calcy = calcyData[["Name","Nr"]].copy()
    

       
    # rename shadow and XL to remove the quotation marks
    #calcy['Shadow'] = calcy['Shadow'].str.replace(r'"', '')
    
    # rename columns                                 
    calcy = calcy.rename(columns={'Name': 'Pokemon'})
    calcy = calcy.rename(columns={'Nr': '#'})    
                                  
    # drop duplicates - WARNING, may drop some pokemon with second special moves
    calcy.drop_duplicates(subset=['Pokemon','#'], inplace=True)
                                  
    #TODO do something with Geodude Normal etc.
    # rename - whitespace. Infuriating
    calcy['Pokemon'] = calcy['Pokemon'].str.replace(r' Normal', '')                              
    calcy['Pokemon'] = calcy['Pokemon'].str.replace(r' Alolan', '')                              
    calcy['Pokemon'] = calcy['Pokemon'].str.replace(r' Spring', '')                              
    calcy['Pokemon'] = calcy['Pokemon'].str.replace(r' Winter', '')                              
    calcy['Pokemon'] = calcy['Pokemon'].str.replace(r' Summer', '')                              
    calcy['Pokemon'] = calcy['Pokemon'].str.replace(r' Autumn', '')                              
    calcy['Pokemon'] = calcy['Pokemon'].str.replace(r' Plant', '')                              
    calcy['Pokemon'] = calcy['Pokemon'].str.replace(r' Sandy', '')                              
    calcy['Pokemon'] = calcy['Pokemon'].str.replace(r' Trash', '')
    calcy['Pokemon'] = calcy['Pokemon'].str.replace(r' Purified', '')
    calcy['Pokemon'] = calcy['Pokemon'].str.replace(r' Shadow', '')
    calcy['Pokemon'] = calcy['Pokemon'].str.replace(r'(Rainy)', '')
    calcy['Pokemon'] = calcy['Pokemon'].str.replace(r'(Snowy)', '')
    calcy['Pokemon'] = calcy['Pokemon'].str.replace(r'(Sunny)', '')
    calcy['Pokemon'] = calcy['Pokemon'].str.replace(r'Castform (Rainy)', 'Castform')
    calcy['Pokemon'] = calcy['Pokemon'].str.replace(r'Castform (Snowy)', 'Castform')
    calcy['Pokemon'] = calcy['Pokemon'].str.replace(r'Castform (Sunny)', 'Castform')
    calcy['Pokemon'] = calcy['Pokemon'].str.replace(r' Blue Striped', '')
    calcy['Pokemon'] = calcy['Pokemon'].str.replace(r' Red Striped', '')
    calcy['Pokemon'] = calcy['Pokemon'].str.replace(r' West Sea', '')
    calcy['Pokemon'] = calcy['Pokemon'].str.replace(r' East Sea', '')
    calcy['Pokemon'] = calcy['Pokemon'].str.replace(r' Overcast', '')
    calcy['Pokemon'] = calcy['Pokemon'].str.replace(r' Sunshine', '')
    calcy['Pokemon'] = calcy['Pokemon'].str.replace(r' Galarian', '')
    calcy['Pokemon'] = calcy['Pokemon'].str.replace(r' Incarnate', '')
    calcy['Pokemon'] = calcy['Pokemon'].str.replace(r' Therian', '')
    
           

    # make a column with "caught"
    calcy['Caught'] = True                                  
                                  
    # get the number, type and name from the lookup:
    PokemonNoTypeAll =  getPokemonNumberType()
    PokemonNoType = PokemonNoTypeAll[["Pokemon","#","Released_2021_03_13"]].copy()
        
    # merge 
    Result1 = gamepress.merge(PokemonNoType,how='inner', on=['Pokemon'])
    
    # This should be the list of released pokemon so far.
    releasedPokemon = Result1[["Pokemon"]].copy()
    releasedPokemon.drop_duplicates(subset=['Pokemon'], inplace=True)

    # a list of pokemon /we/ have is:
    caughtPokemon = calcy[["Pokemon"]].copy()
    caughtPokemon.drop_duplicates(subset=['Pokemon'], inplace=True)
    
    #what we have /not' caught is:
    notCaught = releasedPokemon[releasedPokemon.Pokemon.isin(calcy.Pokemon) == False]
    # sort by ..
    notCaught.sort_values(by=['Pokemon'], inplace=True)
        
    # drop the column
    #Result.drop(columns=['Temp'], inplace=True)
    
    # drop duplicates - WARNING, may drop some pokemon with second special moves
    #TODO - maybe do this better??
    #Result.drop_duplicates(subset=['Pokemon','CP'], inplace=True)
    
    # print(Result)
    
    # sort by ..
    #Result.sort_values(by=['#'], inplace=True)
                           
    return releasedPokemon,caughtPokemon,notCaught

def replaceNameStrings(smallData):
    # making sure we can do something with variants of pokemon with special text
    smallData["PokemonBase"] = smallData["Pokemon"].copy()
    # mostly PVPpoke data
    smallData['PokemonBase'] = smallData['PokemonBase'].apply(lambda x: x.replace(' (Shadow)', ''))
    smallData['PokemonBase'] = smallData['PokemonBase'].apply(lambda x: x.replace(' (Shadow XL)', ''))
    smallData['PokemonBase'] = smallData['PokemonBase'].apply(lambda x: x.replace(' (Galarian)', ''))
    smallData['PokemonBase'] = smallData['PokemonBase'].apply(lambda x: x.replace(' (Galarian XL)', ''))
    smallData['PokemonBase'] = smallData['PokemonBase'].apply(lambda x: x.replace(' (Alolan)', ''))
    smallData['PokemonBase'] = smallData['PokemonBase'].apply(lambda x: x.replace(' (Alolan XL)', ''))
    smallData['PokemonBase'] = smallData['PokemonBase'].apply(lambda x: x.replace(' (Rainy)', ''))
    smallData['PokemonBase'] = smallData['PokemonBase'].apply(lambda x: x.replace(' (Snowy)', ''))
    smallData['PokemonBase'] = smallData['PokemonBase'].apply(lambda x: x.replace(' (Sunny)', ''))
    smallData['PokemonBase'] = smallData['PokemonBase'].apply(lambda x: x.replace(' (Overcast)', ''))
    smallData['PokemonBase'] = smallData['PokemonBase'].apply(lambda x: x.replace(' (Sunshine)', ''))
    smallData['PokemonBase'] = smallData['PokemonBase'].apply(lambda x: x.replace(' (Standard)', ''))
    smallData['PokemonBase'] = smallData['PokemonBase'].apply(lambda x: x.replace(' (Defense)', ''))
    smallData['PokemonBase'] = smallData['PokemonBase'].apply(lambda x: x.replace(' (Speed)', ''))
    smallData['PokemonBase'] = smallData['PokemonBase'].apply(lambda x: x.replace(' (Standard)', ''))
    smallData['PokemonBase'] = smallData['PokemonBase'].apply(lambda x: x.replace(' (East)', ''))
    smallData['PokemonBase'] = smallData['PokemonBase'].apply(lambda x: x.replace(' (West)', ''))
    smallData['PokemonBase'] = smallData['PokemonBase'].apply(lambda x: x.replace(' (Male)', ''))
    smallData['PokemonBase'] = smallData['PokemonBase'].apply(lambda x: x.replace(' (Female)', ''))
    smallData['PokemonBase'] = smallData['PokemonBase'].apply(lambda x: x.replace(' (Wash)', ''))
    smallData['PokemonBase'] = smallData['PokemonBase'].apply(lambda x: x.replace(' (Trash)', ''))
    smallData['PokemonBase'] = smallData['PokemonBase'].apply(lambda x: x.replace(' (Sandy)', ''))
    smallData['PokemonBase'] = smallData['PokemonBase'].apply(lambda x: x.replace(' (Plant)', ''))
    smallData['PokemonBase'] = smallData['PokemonBase'].apply(lambda x: x.replace(' (Burn)', ''))
    smallData['PokemonBase'] = smallData['PokemonBase'].apply(lambda x: x.replace(' (Origin)', ''))
    smallData['PokemonBase'] = smallData['PokemonBase'].apply(lambda x: x.replace(' (Altered)', ''))
    smallData['PokemonBase'] = smallData['PokemonBase'].apply(lambda x: x.replace(' (Incarnate)', ''))
    smallData['PokemonBase'] = smallData['PokemonBase'].apply(lambda x: x.replace(' (Therian)', ''))
    smallData['PokemonBase'] = smallData['PokemonBase'].apply(lambda x: x.replace(' (Armoured)', ''))
  
    # mostly gamepress data
    smallData['PokemonBase'] = smallData['PokemonBase'].apply(lambda x: x.replace('Shadow ', ''))

    return smallData

def replaceBaseNameStrings(strName,strNameBase):
    # do some filtering and replacing
    if strName.endswith(" (Shadow)"):
        strNameSearch = strNameBase + "&shadow"
    elif strName.startswith("Shadow "):
        strNameSearch = strNameBase + "&shadow"
    elif strName.endswith(" (Shadow XL)"):
        strNameSearch = strNameBase + "&shadow"
    elif strName.endswith(" (Galarian)"):
        strNameSearch = strNameBase + "&galar"
    elif strName.endswith(" (Galarian XL)"):
        strNameSearch = strNameBase + "&galar"
    elif strName.endswith(" (Alolan)"):
        strNameSearch = strNameBase + "&alola"
    elif strName.endswith(" (Alolan XL)"):
        strNameSearch = strNameBase + "&alola"
    elif strName.endswith(" (Standard)"):
        strNameSearch = strNameBase
    elif strName.startswith("Castform"):
        strNameSearch = strNameBase
    elif strName.startswith("Cherrim"):
        strNameSearch = strNameBase
    elif strName.startswith("Gastrodon"):
        strNameSearch = strNameBase
    elif strName.startswith("Deoxys"):
        strNameSearch = strNameBase
    elif strName.startswith("Meowstic"):
        strNameSearch = strNameBase
    elif strName.startswith("Rotom"):
        strNameSearch = strNameBase
    elif strName.startswith("Shellos"):
        strNameSearch = strNameBase
    elif strName.startswith("Wormadam"):
        strNameSearch = strNameBase
    elif strName.startswith("Genesect"):
        strNameSearch = strNameBase
    elif strName.startswith("Giratina"):
        strNameSearch = strNameBase
    elif strName.startswith("Landorus"):
        strNameSearch = strNameBase
    elif strName.startswith("Thundurus"):
        strNameSearch = strNameBase
    elif strName.startswith("Tornadus "):
        strNameSearch = strNameBase
    elif strName.startswith("Mewtwo (Armored)"):
        strNameSearch = strNameBase
    else:
        strNameSearch = strName
            
    return strNameSearch

def makeNicePvpPokeString(stringIn):
    
    strMiddle = stringIn
    
    # mostly PvPPoke data
    strMiddle = strMiddle.replace(' (','_')
    strMiddle = strMiddle.replace(')', '')
    
    strOut = strMiddle.lower()

    return strOut

def makeNiceGamepressString(stringIn,strNumber):
    
    strName = stringIn
    
    # do some filtering and replacing
    if strName.endswith(" (Shadow)"):
        strNameSearch = strNumber + "-shadow"
    elif strName.startswith("Shadow "):
        strNameSearch = strNumber + "-shadow"
    elif strName.endswith(" (Shadow XL)"):
        strNameSearch = strNumber + "-shadow"
    elif strName.endswith(" (Galarian)"):
        strNameSearch = strNumber + "-galarian"
    elif strName.endswith(" (Galarian XL)"):
        strNameSearch = strNumber + "-galarian"
    elif strName.endswith(" (Alolan)"):
        strNameSearch = strNumber + "-alolan"
    elif strName.endswith(" (Alolan XL)"):
        strNameSearch = strNumber + "-alolan"
    elif strName.endswith(" (Standard)"):
        strNameSearch = strNumber
    else:
        strNameSearch = strNumber
        
    #TODO: something with the other variants, such as castform, deoxy etc.

    strOut = strNameSearch.lower()

    return strOut

def typeAttackLookup(allData):
    
    import pandas as pd
    
    # files for type lookup:
    fastFilename = 'bulbapedia_fast_move_type.csv'
    chargedFilename = 'bulbapedia_special_move_type.csv'
     
    # load data
    fastData = pd.read_csv(fastFilename,encoding= 'unicode_escape')
    # rename columns                                 
    fastData = fastData.rename(columns={'Name': 'Fast move'})
    fastData = fastData.rename(columns={'Type': 'TypeFast'})
    # fastData.head(5)
     
    chargedData = pd.read_csv(chargedFilename,encoding= 'unicode_escape')
    # rename columns                                 
    chargedData = chargedData.rename(columns={'Name': 'Special move'})
    chargedData = chargedData.rename(columns={'Type': 'TypeSpecial'})
    # chargedData.head(5)
     
    # match pokemon to type:
    allData = allData.merge(fastData,how='inner')
    allData = allData.merge(chargedData,how='inner')
    # allData.head(5)
    
    return allData

def findBothAttackOfType(allData,thisType):
    # finding Pokémon with both attack types the same
     
    bothTypeIDX = allData['TypeFast']==allData['TypeSpecial']
     
    # finding Pokémon with type of something
    setData = allData[bothTypeIDX]
    # print(setData)
     
    singleTypeIDX = setData['TypeFast']==thisType
    setData = setData[singleTypeIDX]
     
    # sort by ..
    setData.sort_values(by=["DPS^3*TDO"], inplace=True, ascending=False)
     
    # print(setData[["Pokemon","DPS^3*TDO"]].head(10))
    
    # take the best move of each pokemon
    setData.drop_duplicates(subset=['Pokemon'], inplace=True)
    
    return setData
	
def concatenateListOfMon(nums):
	#see this for efficient number returns i.e 1,2,3,4 returns 1-4
	#https://stackoverflow.com/a/20725061
	
    ranges = sum((list(t) for t in zip(nums, nums[1:]) if t[0]+1 != t[1]), [])
    iranges = iter(nums[0:1] + ranges + nums[-1:])
    # print ', '.join([str(n) + '-' + str(next(iranges)) for n in iranges])
    
    returnString = ','.join([str(n) + '-' + str(next(iranges)) for n in iranges])
    
    largestNum = nums[-1] + 2
    
    for num in range(1,largestNum):
        returnString = returnString.replace(','+str(num)+'-'+str(num)+',', ','+str(num)+',')
    
    return returnString

def addNewIndexCol(df,colName):
	# add index for all dataframes
	df[colName] = int(0)
	df[colName].astype('int64')
	df[colName] = df[colName].apply(lambda x: "%d" % x)
	for i in range(len(df)):
		df.loc[i,colName] = int(i+1)
	return df

def calculatePvpRating(typeFilter,topX,pvpTopX):
    # setting the filters
    # typeFilter = []
    # topX = 0
    # pvpTopX = 10
    
    import pandas as pd
     
    # PvPpoke filenames
    greatFilename = 'data/great_overall.csv'
    ultraFilename = 'data/ultra_overall.csv'
    masterFilename = 'data/master_overall.csv'
    retroFilename = 'data/retro_overall.csv'
     
    remixFilename = 'data/great_remix_overall.csv'
    classicFilename = 'data/master_classic_overall.csv'
     
    # load data
    greatData=getPvpPokeData(greatFilename,typeFilter,topX)
    ultraData=getPvpPokeData(ultraFilename,typeFilter,topX)
    masterData=getPvpPokeData(masterFilename,typeFilter,topX)
    retroData=getPvpPokeData(retroFilename,typeFilter,topX)
     
    remixData=getPvpPokeData(remixFilename,typeFilter,topX)
    classicData=getPvpPokeData(classicFilename,typeFilter,topX)
    
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
    greatData   = addNewIndexCol(greatData,'GLx')
    ultraData   = addNewIndexCol(ultraData,'ULx')
    masterData  = addNewIndexCol(masterData,'MLx')
    retroData   = addNewIndexCol(retroData,'RLx')
    
    remixData   = addNewIndexCol(remixData,'XGx')
    classicData = addNewIndexCol(classicData,'CLx')
    
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
    setDataTopX.loc[setDataTopX['GLx'].isna(),"GLx"] = int(999)
    setDataTopX.loc[setDataTopX['ULx'].isna(),"ULx"] = int(999)
    setDataTopX.loc[setDataTopX['MLx'].isna(),"MLx"] = int(999)
    setDataTopX.loc[setDataTopX['RLx'].isna(),"RLx"] = int(999)
     
    setDataTopX.loc[setDataTopX['XGx'].isna(),"XGx"] = int(999)
    setDataTopX.loc[setDataTopX['CLx'].isna(),"CLx"] = int(999)
     
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
    keepListString = concatenateListOfMon(keepList)
     
    # combine trash data mon:
    trashList = [int(i) for i in trashDataTopX['#'] ]
    trashList = list(sorted(set(trashList)))
    trashListString = concatenateListOfMon(trashList)

    #print("This is the list to KEEP pokemon for PvP - any ranked below the top "+str(pvpTopX))
    #print(keepListString)
    #print("")
    #print("This is the list to TRASH pokemon not for PvP - ALL ranked above the top "+str(pvpTopX))
    #print(trashListString)
    
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
        if setDataTopX.loc[i,"Best"]==['-']:
            setDataTopX.loc[i,"BestNo"] = 0
     
    setDataTopX.sort_values(by=['BestNo','SumRank'],ascending=(False,True),inplace=True)
     
    #    # dump this to CSV file, top directory:
    #    outCsvFilename = '../csv_Top_X_pokemon_by_leagues.csv'
    #    setDataTopX.to_csv(outCsvFilename)
    #
    """Need to do something that separates the different types of Pokémon, Shadow, alolan etc to make copy paste easier.
    
    Also need to separate leagues, group great leagues together etc.
    """
    
    return setDataTopX,keepList,trashList

