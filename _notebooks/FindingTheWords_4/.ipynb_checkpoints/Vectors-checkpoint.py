import numpy as np
from WordClouds import STOPWORDS
import Preprocessing

def buildVocabulary(processedArticles):
    # generate list of all vocabulary
    vocabulary = []
    for i,article in processedArticles.items():
        vocabulary = vocabulary + article
    
    vocabulary = list(set(vocabulary))
    vocabulary.sort(key=str)

    #return as dictionary
    vocabularyDict = {i:vocabulary[i] for i in range(len(vocabulary))}
    vocabularyToIndexMap = {w:i for i,w in vocabularyDict.items()}
    
    return vocabularyDict, vocabularyToIndexMap

"""takes text and generates a vector from vocabulary map"""
def vectoriseText(vocabToIndexMap,text):
    # encode words as their index in the vocabulary (e.g. possibly 'aardvark' => 23)
    indexArray=[vocabToIndexMap[word] for word in text]
    # transform each
    frequencyVector=[float(np.sum([i==j for j in indexArray])) for i in range(len(vocabToIndexMap))]
    return frequencyVector/np.linalg.norm(frequencyVector)

def vectoriseTexts(vocabToIndexMap,texts):
    return np.vstack([vectoriseText(vocabToIndexMap,text) for i,text in enumerate(texts)])

def vectoriseCorpus(processedTexts):
    # build vocabulary
    vocabulary, vocabToIndexMap = buildVocabulary(processedTexts)
    # convert to 2d numpy array of vectors
    vectorisedTexts = vectoriseTexts(vocabToIndexMap,processedTexts)
    
    return vectorisedTexts, vocabulary

def removeStopwordColumns(vectorisedArticles, vocabulary) :
    stopWords = set(Preprocessing.stemText(STOPWORDS|{'endofsen','endofpar','said','say','will'}))
    vocabGoWordIndexes = [i for i in range(len(vocabulary)) if vocabulary[i] not in stopWords]
    goVocab = [vocabulary[i] for i in range(len(vocabulary)) if vocabulary[i] not in stopWords]

    return vectorisedArticles[:,vocabGoWordIndexes], goVocab