
import Stemmer as ps


# create stemmer class
stemmer = ps.Stemmer('english')


def stemText(words) :
    return [stemmer.stemWord(word) for word in words]


def stemArticles(articles) :
    return {i:stemText(words) for i,words in articles.items()}
