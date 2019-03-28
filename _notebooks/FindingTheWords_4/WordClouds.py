import Clustering
import Preprocessing
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt
import numpy as np

"""creates a WordCloud object from natural text, which can be cast as an image or array of word frequencies"""
def createWordCloud(text) :
    #removes STOPWORDS from the chart to make more readable
    return WordCloud(stopwords=Preprocessing.stemText(STOPWORDS|{'endofsen','endofpar','said','say','will'}),
                     background_color="white",
                     width=500,
                     height=500                    ).generate(text)

"""converts natural text into a WordCloud object, and plots it using Matplotlib"""
def plotWordCloud(text) :
    wordcloud = createWordCloud(text)
    # Display the generated image:
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.show()
    
"""takes an array of cluster IDs and converts it into an array of wordclouds from the text within each cluster"""
def plotClusterWordCloudArray(articles,articleCentroidIds,Ks) :
    fig, axes = plt.subplots(Ks.shape[0], Ks.shape[1], figsize=(12,12))
    for i in range(Ks.shape[0]) :
        for j in range(Ks.shape[1]) :
            axes[i, j].imshow(createWordCloud(Clustering.concatinateClusterTexts(articles,articleCentroidIds,Ks[i,j])))
            axes[i, j].axis("off")
            axes[i, j].set_title("Cluster "+str(Ks[i,j])+"; count="+str(Clustering.countClusterArticles(articles,articleCentroidIds,Ks[i,j])))

