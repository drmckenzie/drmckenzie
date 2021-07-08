
# set the league data back to NaN before export:
setDataTopXRank.loc[setDataTopXRank['ELx']==999,"ELx"] = np.nan
setDataTopXRank.loc[setDataTopXRank['GLx']==999,"GLx"] = np.nan
setDataTopXRank.loc[setDataTopXRank['XGx']==999,"XGx"] = np.nan
setDataTopXRank.loc[setDataTopXRank['RLx']==999,"RLx"] = np.nan
setDataTopXRank.loc[setDataTopXRank['KLx']==999,"KLx"] = np.nan
setDataTopXRank.loc[setDataTopXRank['ULx']==999,"ULx"] = np.nan
setDataTopXRank.loc[setDataTopXRank['PLx']==999,"PLx"] = np.nan
setDataTopXRank.loc[setDataTopXRank['MLx']==999,"MLx"] = np.nan
setDataTopXRank.loc[setDataTopXRank['CLx']==999,"CLx"] = np.nan
