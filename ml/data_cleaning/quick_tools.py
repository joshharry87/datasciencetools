'''
Set of functions for quick cleaning

'''

import numbers
import pandas as pd
import numpy as np

import data_cleaning as  dc


    

def quick_clean(df):
    '''
    Takes a pandas dataframe and runs generic quick clean for EA purposes.
    Returns information on data removed and changes.
    '''
    cols = dc.find_null_columns(df)
    
    nrows = df.shape[0]
    
    for col in cols:
        numeric = []
        strings = []
        dummies = []
        if dc.check_type_numeric(col, df):
            df[col].fillna(df[col].mean())
            numeric.append(col)
        else:
            df = df[df[col] != np.nan | df[col] != None | df[col] != np.NaN]
            if dc.check_categories_by_threshold(df, col, 3):
                dummies.append(col)
                df = pd.get_dummies(df, columns=[col, ])
                for cola in df.columns:
                    if col + '_value' in cola:
                        numeric.append(col)
            else:
                strings.append(col)
                df[col] = df[col].str.lower()
                              
    dropped_rows = nrows -  df.shape[0]
    
    return (df, {
        "numeric_columns" : numeric.length(),
        "string_columns" : strings.length(),
        "dummy_columns" : dummies,
        "n_rows" : nrows,
        "dropped_rows" : dropped_rows
        })