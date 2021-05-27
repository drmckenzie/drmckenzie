
# set the league data back to NaN before export:
setDataTopX.loc[setDataTopX['GLx']==999,"GLx"] = np.nan
setDataTopX.loc[setDataTopX['XGx']==999,"XGx"] = np.nan
setDataTopX.loc[setDataTopX['RLx']==999,"RLx"] = np.nan
setDataTopX.loc[setDataTopX['KLx']==999,"KLx"] = np.nan
setDataTopX.loc[setDataTopX['ULx']==999,"ULx"] = np.nan
setDataTopX.loc[setDataTopX['PLx']==999,"PLx"] = np.nan
setDataTopX.loc[setDataTopX['MLx']==999,"MLx"] = np.nan
setDataTopX.loc[setDataTopX['CLx']==999,"CLx"] = np.nan
