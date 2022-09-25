import re
import networkx
import pandas as pd
import pickle
import numpy as np
import matplotlib.pyplot as plt
import networkx as nx

dfBook = pd.read_pickle("dfBook.pkl")
dfBookReview = pd.read_pickle("dfBookReview.pkl")

dfBooknew = dfBook.iloc[:, [1,3]]

dfBookReview.drop(["Group","Votes","Helpful"], axis=1, inplace=True)

dfMerged= pd.merge(dfBooknew,dfBookReview, on=["ASIN"])

G=nx.from_pandas_edgelist(dfBookReview, 'Customer', 'ASIN', edge_attr='Rating',create_using=nx.DiGraph())
colors = []
for node in G:
    if node in dfMerged["ASIN"].values:
        colors.append("red")
    else: 
        colors.append("blue")

dfMergednew = dfMerged.iloc[:, [0,1]]
dfMergednew = dfMergednew.drop_duplicates()
salesRank_attr = dfMergednew.set_index('ASIN').to_dict('index')
nx.set_node_attributes(G, salesRank_attr)


dfMerged.Rating = dfMerged.Rating.astype(float)
dfMerged2 = dfMerged.groupby(['ASIN'], as_index=False)['Rating'].mean()
rating_attr = dfMerged2.set_index('ASIN').to_dict('index')
nx.set_node_attributes(G, rating_attr)

dfMerged.Votes = dfMerged.Votes.astype(float)
dfMerged2 = dfMerged.groupby(['Customer'],as_index=False)['Votes'].sum()

dfMerged.Helpful = dfMerged.Helpful.astype(float)
dfMergedHELP = dfMerged.groupby(['Customer'],as_index=False)['Helpful'].sum()

dfResult = pd.DataFrame([],columns=["Customer","Helpful"])
dfResult["Customer"] = dfMerged2["Customer"]
dfResult["Helpful"] = dfMergedHELP['Helpful']/dfMerged2['Votes']
dfResult["Helpful"] = dfResult['Helpful'].replace(np.nan,0)
helpful_attr = dfResult.set_index('Customer').to_dict('index')
print(helpful_attr)
nx.set_node_attributes(G,helpful_attr)

"""nx.draw(G,node_size=30,node_color=colors)
plt.show()"""

"""pos = nx.spring_layout(G)
nx.draw(G, pos,node_size=30,node_color=colors)
node_labels = nx.get_node_attributes(G,'SalesRank')
nx.draw_networkx_labels(G, pos, labels = node_labels)
edge_labels = nx.get_edge_attributes(G,'Rating')
nx.draw_networkx_edge_labels(G, pos, edge_labels = edge_labels)
plt.show()"""

nx.write_gpickle(G,"bookReview.gpickle")