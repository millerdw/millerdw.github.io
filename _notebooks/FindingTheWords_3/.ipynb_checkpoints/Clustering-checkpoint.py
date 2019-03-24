import numpy as np

def cosineSimilarity(vectorA,vectorB):
    vectorA = [float(element) for element in vectorA]
    vectorB = [float(element) for element in vectorB]
    return np.dot(vectorA,vectorB)/(np.linalg.norm(vectorA)*np.linalg.norm(vectorB))

def centroidDistances(centroids,article):
    return { k:cosineSimilarity(centroid,article) for k,centroid in centroids.items() }

def generateCentroid(vectorisedArticles):
    randId=np.random.randint(vectorisedArticles.shape[0], size=1)
    return vectorisedArticles[randId]

def interCentroidDistances(centroids) :
    return 1-np.dot(centroids,centroids.T)

def meanInterCentroidDistance(centroids) :
    K = centroids.shape[0]
    #factor of 2 to use only half the matrix
    #factor of K*(K-1) to average over all non-diagonal distances
    #all diagonal distances=0
    return np.sum(np.sum(interCentroidDistances(centroids)))/(2*K*(K-1))

def intraCentroidDistances(vectorisedArticles,centroids) :
    return 1-np.dot(vectorisedArticles,centroids.T)

def meanIntraCentroidDistance(intraCentroidDistances) :
    return np.mean(intraCentroidDistances)


def kMeansCluster(vectorisedArticles,K,G):

    centroids = np.vstack([ generateCentroid(vectorisedArticles) for k in range(K) ])
    articleCentroidIds = []
    performance=[]
    g = 0
    centroidsChanged=True
    while (g<G and centroidsChanged):
        # generate simple cosine distance on normalised vectors between all articles and centroids
        centroidDistances=1-np.dot(vectorisedArticles,centroids.T)

        # use numpy argmin to find index (column) of nearest centroid by article (row)
        articleCentroidIds=np.argmin(centroidDistances,axis=1)
        articleCentroidDistances=np.min(centroidDistances,axis=1)
        
        # create new centroids by averaging positions of all article vectors in cluster
        newCentroids=[]
        for k in range(K):
            clusterMembers=vectorisedArticles[[i for i in range(articleCentroidIds.shape[0]) if articleCentroidIds[i]==k],:]
            clusterSize = clusterMembers.shape[0]
            if clusterSize==0:
                newCentroid=generateCentroid(vectorisedArticles)
            else:
                newCentroid=np.mean(clusterMembers,axis=0)
            newCentroids.append(newCentroid)
        newCentroids=np.vstack(newCentroids)

        # update existing centroids
        centroidsChanged = (np.sum(np.diag(np.dot(centroids,newCentroids.T))<1.0)>0)
        centroids=newCentroids
        g+=1
        
        interCentroidDistance = np.sum(np.sum(1-np.dot(newCentroids,newCentroids.T)))/(2*K*(K-1))
        intraCentroidDistance = np.mean(articleCentroidDistances)
        performance.append([g,interCentroidDistance,intraCentroidDistance,intraCentroidDistance/interCentroidDistance])
        
    return articleCentroidIds,centroids,np.vstack(performance)

