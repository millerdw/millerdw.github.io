
import Stemmer as ps
import re
import DataAccess
from wordcloud import STOPWORDS

# create stemmer class
stemmer = ps.Stemmer('english')


def preprocessArticles(articles) :
    reEndOfSentence = re.compile('\\. ')
    reNonAlphaNumeric = re.compile('\'s|/\n/|/\t/|[\W]+ | ')
    processedArticles = {}
    for i,article in articles.items() :
        # collect contents
        contents = [str(article['description'])+' ']+DataAccess.scrapeArticleUrl(article['url'])
        # convert contents into words
        words = []
        for text in contents:
            # covert to lower case
            text = text.lower()
            # replace full stops with ENDOFSEN
            text = reEndOfSentence.sub(' endofsen ',text)
            # split text into individual words
            newWords = text.split(' ')
            # remove remaining non-alphanumerics
            newWords = [reNonAlphaNumeric.sub('',word) for word in newWords]
            words = words + [word for word in newWords if word!='']

        # combine into list of processed articles
        processedArticles[i] = words
        
    return processedArticles


def stemText(words) :
    return [stemmer.stemWord(word) for word in words]


def stemTexts(articles) :
    return {i:stemText(words) for i,words in articles.items()}

def removeStopwords(articles) :
    stopWords = set(stemText(STOPWORDS|{'endofsen','endofpar','said','say','will'}))
    return {i:[words[j] for j in range(len(words)) if words[j] not in stopWords] for i,words in articles.items()}