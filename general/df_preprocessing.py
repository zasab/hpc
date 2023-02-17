import numpy as np


def apply(dataframe):
    dataframe = dataframe[~dataframe['COMMAND'].isin(['(null)'])]
    proccessed_command_list = []
    for x in dataframe['COMMAND']:
        proccessed_command_list.append(str(x).split('/')[-1])
    
    dataframe['PROCESSED_COMMAND'] = proccessed_command_list
    dataframe = dataframe[~dataframe['CURRENT_TIMESTAMP'].isin([np.nan])]
    dataframe = dataframe[dataframe["ST"].isin(["PD", "R", "CG"])]

    return dataframe

