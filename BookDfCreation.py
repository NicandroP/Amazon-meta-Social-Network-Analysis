import re
import networkx
import pandas as pd
import pickle
import numpy as np
import string
from nltk.corpus import stopwords

fhr = open('./amazon-meta.txt', 'r', encoding='utf-8', errors='ignore')

productList = []
for line in fhr :
    line = line.strip()
    # a product block started
    if(line.startswith("Id")):
        Id = line[3:].strip()
    elif(line.startswith("ASIN")):
        ASIN = line[5:].strip()
    elif(line.startswith("group")):
        Group = line[6:].strip()
    elif(line.startswith("salesrank")):
        SalesRank = line[10:].strip()
    elif(line.startswith("similar")):
        Similar = line.strip().split()
        similarList=[]
        if(len(Similar)>2):
            for k in range(2,len(Similar),1):
                similarList.append(Similar[k])
    elif(line.startswith("categories")):
        ls = line.split()
        if(ls[1]!="0"):        
            Categories = ' '.join((fhr.readline()).lower() for i in range(1))
            Categories=Categories.split("|")
        else:
            Categories=""
    elif(line.startswith("reviews")):
        ls = line.split()
        TotalReviews = ls[2].strip()
        AvgRating = ls[7].strip()

    # a product block ended
    # write out fields to list
    elif (line==""):
        try:
            MetaData = []
            MetaData.append(Id)
            MetaData.append(ASIN)
            MetaData.append(Group)
            MetaData.append(SalesRank)
            MetaData.append(similarList)
            MetaData.append(Categories)
            MetaData.append(TotalReviews)
            MetaData.append(AvgRating)
            productList.append(MetaData)
        except NameError:
            continue
fhr.close()

# create books-specific list exclusively for books
bookList = []
count=0
for product in productList:
        if (product[2]=='Book'):
            if(len(product[5])>3):
                Categories=product[5][3]
                Categories=Categories[0: Categories.index("["):]
                product[5]=Categories
            bookList.append(product)
            count+=1
        if count == 200000:
            break

dfBook = pd.DataFrame(bookList, columns = ['Id', 'ASIN',"Group",'SalesRank','Similar','Categories','TotalReviews','AvgRating',])
print(dfBook)

dfBook.to_pickle("dfBook.pkl")