import matplotlib.pyplot as plt
from wordcloud import WordCloud, STOPWORDS

"""returns all articles in a cluster"""
def ListClusterTexts(articles,articleCentroidIds,K) :
    return [articles[i] for i in range(articleCentroidIds.shape[0]) if articleCentroidIds[i]==K]

"""concatinates all tokenised article texts in an article cluster into a single pseudo-natural text"""
def ConcatinateClusterTexts(articles,articleCentroidIds,K) :
    clusterText = ''
    for article in ListClusterTexts(articles,articleCentroidIds,K) :
        clusterText+=' '.join(article) 
    return clusterText

"""counts the number of articles in a cluster"""
def CountClusterArticles(articles,articleCentroidIds,K) :
    return len(ListClusterTexts(articles,articleCentroidIds,K))

"""creates a WordCloud object from natural text, which can be cast as an image or array of word frequencies"""
def CreateWordCloud(text) :
    #removes STOPWORDS from the chart to make more readable
    return WordCloud(stopwords=Preprocessing.stemText(STOPWORDS|{'endofsen','endofpar','said','say','will'}),
                     background_color="white",
                     width=500,
                     height=500                    ).generate(text)

"""converts natural text into a WordCloud object, and plots it using Matplotlib"""
def PlotWordCloud(text) :
    wordcloud = CreateWordCloud(text)
    # Display the generated image:
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.show()
    
"""takes an array of cluster IDs and converts it into an array of wordclouds from the text within each cluster"""
def PlotClusterWordCloudArray(articles,articleCentroidIds,Ks) :
    fig, axes = plt.subplots(Ks.shape[0], Ks.shape[1], figsize=(12,12))
    for i in range(Ks.shape[0]) :
        for j in range(Ks.shape[1]) :
            axes[i, j].imshow(CreateWordCloud(ConcatinateClusterTexts(articles,articleCentroidIds,Ks[i,j])))
            axes[i, j].axis("off")
            axes[i, j].set_title("Cluster "+str(Ks[i,j])+"; count="+str(CountClusterArticles(articles,articleCentroidIds,Ks[i,j])))
