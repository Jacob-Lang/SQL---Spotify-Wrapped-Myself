# Utility functions for spotify_wrapped_myself.ipynb

import pandas as pd   # use to show tables nicely.
from IPython.display import HTML

import numpy as np

# for showing tables nicely
def show_table(cur, n_rows):
    col_name_list = [tuple[0] for tuple in cur.description]  # get column names
    rows = cur.fetchall()                                    # get table data
    rows = [list(row) for row in rows]                       # convert row tuples to list (to make compatible with df.dataframe)
    df = pd.DataFrame(rows, columns=col_name_list)           # convert to pandas dataframe
    return HTML(df.head(n_rows).to_html(index=False))        # print first n_rows without index

# find the number of hours played per month for a given artist
def hours_played_by_month(cur, artist_name):
    sql_command = """SELECT STRFTIME('%m', endTime) as valMonth, SUM(msPlayed)/(60.0*60*1000) 
                        FROM history 
                        WHERE artistName = (?) 
                        AND STRFTIME('%Y', endTime) = '2019' 
                        GROUP BY valMonth 
                        ORDER BY valMonth""" 

    cur.execute(sql_command, [artist_name])
    results = cur.fetchall()
    
    months = np.array([n for n in range(1,13)])
    hours_played = np.zeros(12)
    
    for entry in results:
        month_index = int(entry[0]) - 1
        hours_played[month_index] = entry[1]
    
    return months, hours_played
