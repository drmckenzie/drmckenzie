
# set the league data back to NaN before export:
setDataTopXRank.loc[setDataTopXRank['GLx']==999,"GLx"] = 0
setDataTopXRank.loc[setDataTopXRank['XGx']==999,"XGx"] = 0
setDataTopXRank.loc[setDataTopXRank['RLx']==999,"RLx"] = 0
setDataTopXRank.loc[setDataTopXRank['KLx']==999,"KLx"] = 0
setDataTopXRank.loc[setDataTopXRank['ULx']==999,"ULx"] = 0
setDataTopXRank.loc[setDataTopXRank['PLx']==999,"PLx"] = 0
setDataTopXRank.loc[setDataTopXRank['MLx']==999,"MLx"] = 0
setDataTopXRank.loc[setDataTopXRank['CLx']==999,"CLx"] = 0
