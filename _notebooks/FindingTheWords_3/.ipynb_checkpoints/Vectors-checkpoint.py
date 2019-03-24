import numpy as np

def buildVocabulary(processedArticles):
    # generate list of all vocabulary
    vocabulary = []
    for i,article in processedArticles.items():
        vocabulary = vocabulary + article
    
    vocabulary = list(set(vocabulary))
    vocabulary.sort(key=str)

    #return as dictionary
    return {i:vocabulary[i] for i in range(len(vocabulary))}

def vectoriseText(vocabToIndexMap,article):
    # encode words as their index in the vocabulary (e.g. possibly 'aardvark' => 23)
    indexArray=[vocabToIndexMap[word] for word in article]
    # transform each
    frequencyVector=[float(np.sum([i==j for j in indexArray])) for i in range(len(vocabToIndexMap))]
    return frequencyVector/np.linalg.norm(frequencyVector)

def vectoriseArticles(processedArticles):
    # build vocabulary
    vocabulary = buildVocabulary(processedArticles)
    # create map of word to vocabulary index
    vocabToIndexMap={w:i for i,w in vocabulary.items()}
    # convert to 2d numpy array of vectors
    vectorisedArticles = np.vstack([vectoriseText(vocabToIndexMap,article) for i,article in processedArticles.items()])
    return vectorisedArticles, vocabulary
    