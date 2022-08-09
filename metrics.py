from pandas import read_csv
from statistics import mean, median
import os
import csv

result_df = read_csv("metricsdata.csv")



#  "https://github.com/castellonmayra/mc-freestyle/blob/main/metricsdata.csv"

print(type(result_df))
#print(result_df)
print(result_df.columns)
print(len(result_df))

print(result_df.head(3))

#####

mv_col = result_df["MARKET VALUE"]
print(mv_col)

print(mv_col.max())



###

from plotly.express import bar

fig = bar(data_frame=result_df, 
            y="SECURITY", 
            x="MARKET VALUE",
            orientation="h",
            title="Market Value By Security", 
            
            # from the docs: "The keys of this dict should correspond to column names, 
            # and the values should correspond to the desired label to be displayed.
            labels={"SECURITY": "Security", "MARKET VALUE": "Market Value"},
          
            color="MARKET VALUE")
fig.show()