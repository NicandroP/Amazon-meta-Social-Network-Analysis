import re
import networkx
import pandas as pd
import pickle
import numpy as np

fhr = open('./amazon-meta.txt', 'r', encoding='utf-8', errors='ignore')

reviewList = []

for line in fhr :
    line = line.strip()
    # a product block started
    if(line.startswith("ASIN")):
        ASIN = line[5:].strip()
    elif(line.startswith("group")):
        Group = line[6:].strip()
    elif(line.startswith("20")):
        ls = line.split()
        Customer = ls[2].strip()
        Rating = ls[4].strip()
        Votes = ls[6].strip()
        Helpful = ls[8].strip()
        try:
            MetaData = []
            MetaData.append(ASIN)
            MetaData.append(Group)
            MetaData.append(Customer)
            MetaData.append(Rating)
            MetaData.append(Votes)
            MetaData.append(Helpful)            
            reviewList.append(MetaData)
        except NameError:
            continue

    # a product block ended
    # write out fields to list
fhr.close()

# create books review-specific list exclusively for books reviews
bookReviewList = []
count=0
for review in reviewList:
        if (review[1]=='Book'):
            bookReviewList.append(review)
            count+=1
        if count == 200000:
            break

dfBookReview = pd.DataFrame(bookReviewList, columns = ['ASIN',"Group",'Customer','Rating','Votes','Helpful'])
print(dfBookReview)

dfBookReview.to_pickle("dfBookReview.pkl")