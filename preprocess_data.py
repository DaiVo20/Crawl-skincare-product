from numpy.core.numeric import NaN
import pandas as pd
import os
import glob
import numpy as np
import time
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
        # if price = Null, delete that row
        if(product["price"][j] == ""):
            product = product.drop(j)
    product = product.dropna(subset=['comment'])

    product = product.to_numpy()
    # Remove 00000 to get true price
    for j, k in enumerate(product[:, 1]):
        product[j, 1] = sum([int(int(m)/100000) for m in k.split(", ")])

    full_data.append(product)

dataset = np.concatenate(full_data)
combined_csv = pd.DataFrame(data=dataset, columns=[
                            "variations", "price", "rating_star", "comments"])

# export to csv
combined_csv.to_csv("combined_file.csv", index=False, encoding='utf-8')

# export to txt
np.savetxt("combined_file.txt", dataset, fmt=[
           '%s', '%d', '%d', '%s'], delimiter="\t", encoding='utf-8')