import pandas as pd
import os
import glob
import numpy as np
import warnings
warnings.filterwarnings("ignore")

products = pd.read_csv("products.csv")
product_detail = products[["itemid", "shopid", "name"]].values

path = "cmt_ratings/"
files = os.listdir(path)
for f in files:
    df = pd.read_csv(path+f)
    temp = np.array(f.replace(".csv", "").split(","))
    id = np.where(product_detail[:,0]== int(temp[0]))[0][0]
    name = np.full((len(df), 1), product_detail[id,2])
    df.insert(0, "name", name)
    df.to_csv(path+f, index=False)