from platform import node
import re
import networkx
import pandas as pd
import pickle
import numpy as np
import matplotlib.pyplot as plt
import networkx as nx
import powerlaw
dfBook = pd.read_pickle("dfBook.pkl")
uniqueAsin=dfBook['ASIN'].unique()
edgesList=[]
for j in range(len(dfBook)):
    for k in range(len(dfBook.iloc[j,]['Similar'])):
        if(dfBook.iloc[j,]['Similar'][k] in uniqueAsin):
            singleEdge=[]
            singleEdge.append(dfBook.iloc[j,]['ASIN'])
            singleEdge.append(dfBook.iloc[j,]['Similar'][k])
            edgesList.append(singleEdge)

dfEdge = pd.DataFrame(edgesList, columns = ['source', 'target'])

G=nx.from_pandas_edgelist(dfEdge, 'source', 'target')

#nx.draw(G,node_size=30)
#plt.show()
nodeList = list(G.nodes())

bookCategory=[]
for k in range(len(nodeList)):
    bookCategoryCouple=[]
    idx=dfBook.loc[dfBook['ASIN'] == nodeList[k]].index[0]
    bookCategoryCouple.append(nodeList[k])
    bookCategoryCouple.append(dfBook.iloc[idx]["Categories"])
    bookCategory.append(bookCategoryCouple)

dfBookCategory = pd.DataFrame(bookCategory, columns = ['ASIN', 'Category'])
CategoryAttribute = dfBookCategory.set_index('ASIN').to_dict('index')
nx.set_node_attributes(G, CategoryAttribute)

bookSales=[]
for k in range(len(nodeList)):
    bookSalesCouple=[]
    idx=dfBook.loc[dfBook['ASIN'] == nodeList[k]].index[0]
    bookSalesCouple.append(nodeList[k])
    bookSalesCouple.append(float(dfBook.iloc[idx]["SalesRank"]))
    bookSales.append(bookSalesCouple)

dfBookSales = pd.DataFrame(bookSales, columns = ['ASIN', 'SalesRank'])
SalesAttribute = dfBookSales.set_index('ASIN').to_dict('index')
nx.set_node_attributes(G, SalesAttribute)

bookReview=[]
for k in range(len(nodeList)):
    bookReviewCouple=[]
    idx=dfBook.loc[dfBook['ASIN'] == nodeList[k]].index[0]
    bookReviewCouple.append(nodeList[k])
    bookReviewCouple.append(float(dfBook.iloc[idx]["TotalReviews"]))
    bookReview.append(bookReviewCouple)

dfBookReview = pd.DataFrame(bookReview, columns = ['ASIN', 'TotalReviews'])
ReviewAttribute = dfBookReview.set_index('ASIN').to_dict('index')
nx.set_node_attributes(G, ReviewAttribute)

bookAvgRating=[]
for k in range(len(nodeList)):
    bookAvgRatingCouple=[]
    idx=dfBook.loc[dfBook['ASIN'] == nodeList[k]].index[0]
    bookAvgRatingCouple.append(nodeList[k])
    bookAvgRatingCouple.append(float(dfBook.iloc[idx]["AvgRating"]))
    bookAvgRating.append(bookAvgRatingCouple)

dfBookAvgRating = pd.DataFrame(bookAvgRating, columns = ['ASIN', 'AvgRating'])
AvgRatingAttribute = dfBookAvgRating.set_index('ASIN').to_dict('index')
nx.set_node_attributes(G, AvgRatingAttribute)

nx.write_gpickle(G,"bookCopurchasing.gpickle")