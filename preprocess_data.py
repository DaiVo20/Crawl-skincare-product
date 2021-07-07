import pandas as pd
import os
import glob
import numpy as np
import warnings
warnings.filterwarnings("ignore")

# use glob to get all the csv files
# in the folder
path = "cmt_ratings/"
csv_files = glob.glob(os.path.join(path, "*.csv"))
characters = ["['", "']", "'", "[None]", "['']", "[", "]"]


def replace_char(arg, characters):
    for c in characters:
        arg = arg.replace(c, "")
    return arg


raw_data = pd.concat([pd.read_csv(f) for f in csv_files])
raw_data.to_csv("raw_data.csv", index=False, encoding='utf-8')

full_data = []
# Clean data
for i in csv_files:
    product = pd.read_csv(i)
    print(i)
    for j in range(len(product)):
        # Remove unusual characters
        product["variations"][j] = replace_char(
            product["variations"][j], characters)
        product["price"][j] = replace_char(product["price"][j], characters)
        # if price = Null, assign -1
        if(product["price"][j] == ""):
            product=product.drop(j)

    product = product.dropna(subset=['comment'])
    product["variations"] = product["variations"].replace("", "0")

    product = product.to_numpy()
    # Remove 00000 to get true price
    for j, k in enumerate(product[:, 2]):
        product[j, 2] = sum([int(int(m)/100000) for m in k.split(", ")])

    full_data.append(product)

dataset = np.concatenate(full_data)
combined_csv = pd.DataFrame(data=dataset, columns=["name",
                                                   "variations", "price", "rating_star", "comments"])

# export to csv
combined_csv.to_csv("pre_data.csv", index=False, encoding='utf-8')
