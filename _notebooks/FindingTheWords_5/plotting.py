import matplotlib.pyplot as plt
from wordcloud import WordCloud, STOPWORDS
from preprocessing import stemText


whatwords = {"who","who's","where","where's","when","when's","why","why's","what","what's","how","how's","which"}
stopwords = STOPWORDS.difference(whatwords)

def ListClusterTexts(articles,articleCentroidIds,K) :
    """returns all articles in a cluster"""
    return [articles[i] for i in range(articleCentroidIds.shape[0]) if articleCentroidIds[i]==K]

def ConcatinateClusterTexts(articles,articleCentroidIds,K) :
    """concatinates all tokenised article texts in an article cluster into a single pseudo-natural text"""
    return ' '.join(ListClusterTexts(articles,articleCentroidIds,K))

def CountClusterArticles(articles,articleCentroidIds,K) :
    """counts the number of articles in a cluster"""
    return len(ListClusterTexts(articles,articleCentroidIds,K))

def CreateWordCloud(text,remove_stopwords=True,remove_whatwords=False) :
    """creates a WordCloud object from natural text, which can be cast as an image or array of word frequencies"""
    #removes STOPWORDS from the chart to make more readable
    return WordCloud(stopwords=stemText({'endofsen','endofpar'}.union(stopwords if remove_stopwords else {}).union(whatwords if remove_whatwords else {})),
                     background_color="white",
                     width=500,
                     height=500 ).generate(text)


def PlotWordCloud(text, remove_stopwords=True, remove_whatwords=False, ax=None) :
    """converts natural text into a WordCloud object, and plots it using Matplotlib"""
    if ax is None:
        ax=plt.gca()
    wordcloud = CreateWordCloud(text,remove_stopwords,remove_whatwords)
    # plot the generated image:
    ax.imshow(wordcloud, interpolation='bilinear')
    
    
def PlotWordCloudArray(articles,articleCentroidIds,Ks,remove_stopwords=True,remove_whatwords=False) :
    """takes an array of cluster IDs and converts it into an array of wordclouds from the text within each cluster"""
    fig, axes = plt.subplots(Ks.shape[0], Ks.shape[1], figsize=(16,16*(Ks.shape[0]/Ks.shape[1])))
    for i in range(Ks.shape[0]) :
        for j in range(Ks.shape[1]) :
            axes[i, j].axis("off")
            if Ks[i,j] is not None:
                PlotWordCloud(ConcatinateClusterTexts(articles,articleCentroidIds,Ks[i,j]),
                              remove_stopwords,remove_whatwords,
                              ax = axes[i, j])
                axes[i, j].set_title("Cluster "+str(Ks[i,j])+"; count="+str(CountClusterArticles(articles,articleCentroidIds,Ks[i,j])))
             
            
     