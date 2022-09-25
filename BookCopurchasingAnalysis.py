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
import math
warnings.filterwarnings("ignore")

G=nx.read_gpickle("bookCopurchasing.gpickle")

def centrality():
    degreeCentrality = nx.degree_centrality(G)
    eigenvectorCentrality = nx.eigenvector_centrality(G)
    closenessCentrality = nx.closeness_centrality(G)
    betweennessCentrality = nx.betweenness_centrality(G)
    katzCentrality = nx.katz_centrality(G)

def degree_distribution():
    degrees=list(dict(G.degree()).values())
    fig, (ax1, ax2) = plt.subplots(1, 2, sharex=False, sharey=False)
    ax1.set_yscale("log")
    ax1.hist(degrees, bins=30)
    ax2.set_yscale("log")
    ax2.set_xscale("log")
    ax2.hist(degrees, bins="auto")
    fig.supxlabel('Degree')
    fig.supylabel('Frequency')
    plt.show()
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

def average_path_lenght():
    paths=[]
    for C in (G.subgraph(c).copy() for c in nx.connected_components(G)):
        paths.append(nx.average_shortest_path_length(C))
    print("Average path lenght is: ",sum(paths)/len(paths))
    print("log(len(g.nodes)): ",math.log(len(G.nodes())))

def k_cores():
    n_nodes = range(1, 7)
    k_cores = [nx.k_core(
        G, k).order() for k in n_nodes]
    print("K-cores analysis: ", k_cores)
    plt.clf()
    plt.plot(n_nodes, k_cores, marker="s")
    plt.xlabel("K")
    plt.ylabel("Nodes")
    plt.show()

def clusteringCoefficient():
    clusteringCoefficient = nx.average_clustering(G)
    print("Clustering coefficient is: ",clusteringCoefficient)

def assortativity():
    degree_assortativity=nx.degree_assortativity_coefficient(G)
    avgRating_assortativity=nx.numeric_assortativity_coefficient(G, attribute="AvgRating")
    sales_assortativity=nx.numeric_assortativity_coefficient(G, attribute="SalesRank")
    review_assortativity=nx.numeric_assortativity_coefficient(G, attribute="TotalReviews")
    categories_assortativity=nx.attribute_assortativity_coefficient(G, attribute="Category")
    
    print("Degree assortativity: ",degree_assortativity,"\nCategories assortativity: ",
        categories_assortativity,"\nSalesRank assortativity: ",
        sales_assortativity,"\nTotal review assortativity: ",review_assortativity,"\nAvgRating assorativity: ",avgRating_assortativity)

def truncate(number, digits) -> float:
    # Improve accuracy with floating point operations, to avoid truncate(16.4, 2) = 16.39 or truncate(-1.13, 2) = -1.12
    nbDecimals = len(str(number).split('.')[1]) 
    if nbDecimals <= digits:
        return number
    stepper = 10.0 ** digits
    return math.trunc(stepper * number) / stepper

def hits():
    h, a = nx.hits(G)
    #print("hits: ",h,a)
    hubss=[]
    hubs=list(h.values())
    for k in range(len(hubs)):
        #hubs[k]=hubs[k]*10000000000000000
        hubs[k]=truncate(hubs[k],3)
        if(hubs[k]!=0):
            hubss.append(hubs[k])
    print(hubss)
    fig, (ax1, ax2) = plt.subplots(1, 2, sharex=False, sharey=False)
    ax1.set_yscale("log")
    ax1.hist(hubs, bins=30)
    ax2.set_yscale("log")
    ax2.set_xscale("log")
    ax2.hist(hubs, bins="auto")
    fig.supxlabel('Hub value')
    fig.supylabel('Frequency')
    plt.show()

def subgraph():
    plt.clf()
    Gi=list((G.subgraph(c) for c in nx.connected_components(G)))
    largestGraph=sorted(Gi, key=len, reverse=True)[0]
    #nx.draw(largestGraph,node_size=30)
    #plt.show()

    import matplotlib.colors as mcolors
    import matplotlib.cm as cm
    deg_centrality = nx.degree_centrality(largestGraph)
    cent = np.fromiter(deg_centrality.values(), float)
    sizes = cent / np.max(cent) * 200
    normalize = mcolors.Normalize(vmin=cent.min(), vmax=cent.max())
    colormap = cm.viridis
    scalarmappaple = cm.ScalarMappable(norm=normalize, cmap=colormap)
    scalarmappaple.set_array(cent)
    pos = nx.kamada_kawai_layout(largestGraph)
    ax=plt.gca()
    plt.colorbar(scalarmappaple,ax=ax)
    nx.draw(largestGraph, pos, node_size=sizes, node_color=sizes,cmap=colormap)
    plt.show()
    
def smallWorld():
    smallWorldCoeff=nx.omega(G)
    print("Small world coefficient is: ",smallWorldCoeff)

if __name__=="__main__":
    centrality()
    #degree_distribution()
    #average_path_lenght()
    #k_cores()
    #clusteringCoefficient()
    #assortativity()
    #hits()
    #subgraph()
    #smallWorld()