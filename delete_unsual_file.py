"""
    Remove unusual file in cmt_ratings folder

"""
import pandas as pd
import os
import glob
import numpy as np

# use glob to get all the csv files
# in the folder
path = "cmt_ratings/"

files = os.listdir(path)

temp=[]
for f in files:
    f=np.array(f.replace(".csv",""))
    temp.append(f)

products = pd.read_csv("products.csv")
product_detail = products[["itemid", "shopid"]].values
file_name=[]
for i in range(len(product_detail)):
    file_name.append("{},{}".format(product_detail[i,0], product_detail[i,1]))

for i,j in enumerate(temp):
    if (j not in file_name):
        os.remove("cmt_ratings/{}.csv".format(j))