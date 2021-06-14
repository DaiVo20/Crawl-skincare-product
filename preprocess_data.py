import pandas as pd
import os
import glob

# use glob to get all the csv files
# in the folder
path = "cmt_ratings/"
csv_files = glob.glob(os.path.join(path, "*.csv"))

for i in csv_files:
    print(pd.read_csv(i))
