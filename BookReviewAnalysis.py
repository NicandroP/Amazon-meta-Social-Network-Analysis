from platform import node
import re
import networkx
import pandas as pd
import pickle
import numpy as np
import matplotlib.pyplot as plt
import networkx as nx
import powerlaw
import warnings
from scipy.stats import pearsonr
warnings.filterwarnings("ignore")

G=nx.read_gpickle("bookReview.gpickle")

def degree_distribution():
    degrees=list(dict(G.degree()).values())
    print(degrees)
    fig, (ax1, ax2) = plt.subplots(1, 2, sharex=False, sharey=False)
    ax1.set_yscale("log")
    ax1.hist(degrees, bins=30)
    ax2.set_yscale("log")
    ax2.set_xscale("log")
    ax2.hist(degrees, bins="auto")
    fig.supxlabel('Degree')
    fig.supylabel('Frequency')
    plt.show()
    #plt.pause(0.1)
    plt.clf()
    fit = powerlaw.Fit(degrees, discrete=True, xmin=1)
    print("Power law alpha: ", fit.alpha,
            " Power law xmin: ", fit.xmin)
    axis = fit.plot_ccdf()
    fit.power_law.plot_ccdf(ax=axis, color='r', linestyle='--')
    fit.lognormal.plot_ccdf(ax=axis, color='g', linestyle='--')
    fit.stretched_exponential.plot_ccdf(ax=axis, color='b', linestyle='--')
    plt.legend(['Observed network', 'Power law',
                'Lognormal', 'Stretched exp.'])
    plt.xlabel("Degree")
    plt.ylabel("CCDF")
    plt.show()
    power_law_lognormal = fit.distribution_compare(
        "power_law", "lognormal", normalized_ratio=True)
    power_law_stretched = fit.distribution_compare(
        "power_law", "stretched_exponential", normalized_ratio=True)
    log_normal_stretched = fit.distribution_compare(
        "lognormal", "stretched_exponential", normalized_ratio=True)
    print("Power law vs lognormal: ", power_law_lognormal,
          " Power law vs stretched exponential", power_law_stretched, " Lognormal vs stretched exponential ", log_normal_stretched)

def pearsonCoefficient():
    inDegree=list(G.in_degree)
    #computig the pearson coefficient between SalesRank and number of reviews of a book
    booksDegree=[]
    for k in range(len(inDegree)):
        if(inDegree[k][1]>0):
            booksDegree.append(inDegree[k][1])
    SalesRanklist=nx.get_node_attributes(G, "SalesRank")
    booksSalesRank=list(SalesRanklist.values())
    booksSalesRank = [int(i) for i in booksSalesRank]

    #scatterplot between in degrees of books and books' salesrank
    dictionary = dict(zip(booksSalesRank, booksDegree))
    dictionary2={key:val for key, val in dictionary.items() if val <400}
    dictionary2={key:val for key, val in dictionary2.items() if key <2000000}
    plt.clf()
    plt.scatter(list(dictionary2.keys()), list(dictionary2.values()))
    plt.xlabel("Books SalesRank")
    plt.ylabel("Books' degree")
    from matplotlib.ticker import ScalarFormatter, FormatStrFormatter
    ax = plt.gca()
    ax.xaxis.set_major_formatter(FormatStrFormatter('%.0f'))
    plt.show()
    plt.clf()

    pearsonCoeff=pearsonr(booksDegree, booksSalesRank)
    print("Paerson coeff between Booksdegree and SalesRank: ",pearsonCoeff)
    
    my_rho = np.corrcoef(booksDegree, booksSalesRank)
    print("Correlation coeff between Booksdegree and SalesRank: ",my_rho)
    
    #computig the pearson coefficient between SalesRank and average rating of a book
    AvgRatingList=nx.get_node_attributes(G, "Rating")
    BookAvg=list(AvgRatingList.values())
    pearsonCoeff=pearsonr(BookAvg, booksSalesRank)
    print("Paerson coeff between AvgRating and SalesRank: ",pearsonCoeff)
    
    my_rho = np.corrcoef(BookAvg, booksSalesRank)
    print("Correlation coeff between AvgRating and SalesRank: ",my_rho)

def influencer():
    BooksandSalesRank=nx.get_node_attributes(G, "SalesRank")
        
    books = [node for node in G.nodes if G.out_degree(node) == 0]
    
    neighborForBook=[]
    for book in books:
        neighborForBook.append(list(nx.all_neighbors(G,book)))
    
    influencersReviewsForBook=[]
    for k in range(len(neighborForBook)):
        nReviewsList=[]
        for j in range(len(neighborForBook[k])):
            nReviewsList.append(G.out_degree(neighborForBook[k][j]))
        maxReviews=max(nReviewsList)
        influencersReviewsForBook.append(maxReviews)

    bookSalesRank=list(BooksandSalesRank.values())
    bookSalesRank=[float(i) for i in bookSalesRank]

    pearsonCoeff=pearsonr(influencersReviewsForBook, bookSalesRank)
    print("Paerson coeff between SalesRank and num reviews of the book'influencer: ",pearsonCoeff)
    
    avgHelpful = []
    avgHelpful =nx.get_node_attributes(G, "Helpful")
    influecerHelpfulList=[]
    for i in range(len(influencerList)):
        influencerHelpfulVal = avgHelpful.get(influencerList[i])
        influecerHelpfulList.append(influencerHelpfulVal)

    pearsonCoeff=pearsonr(influecerHelpfulList,bookSalesRank)
    print("Paerson coeff between SalesRank and percentage of helpful of the book'influencer: ",pearsonCoeff)

if __name__=="__main__":
    degree_distribution()
    #pearsonCoefficient()
    #influencer()