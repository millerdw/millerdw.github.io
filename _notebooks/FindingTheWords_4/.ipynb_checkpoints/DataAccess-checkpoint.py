
from newsapi import NewsApiClient
import requests
from bs4 import BeautifulSoup as bs
import datetime

"""accesses any articles published by a hardcoded range of vendors, within the last 4 weeks"""
def getArticles():
    #Don't worry, I update by API key every time I publish this on Github
    news = NewsApiClient(api_key='405cbb818b64428ab934b95bfec1426d')
    
    newsSources = 'bbc-news,the-verge,abc-news,ary news,associated press,wired,aftenposten,bbc news,bild,blasting news,bloomberg,business insider,engadget,google news,the verge'
    
    toDate = datetime.datetime.now().date()
    fromDate = toDate-datetime.timedelta(weeks=-4)
    
    ## Collect new contents
    all_news = []
    for i in range(1,11):
        all_news.append(news.get_everything(sources=newsSources,
                                            from_param=format(fromDate),
                                            to=format(toDate),
                                            language='en',
                                            page_size=100,
                                            page=i))
    
    ## Create List of Articles
    rawArticles=[]
    for news in all_news:
        rawArticles=rawArticles+news['articles']
    
    # dict comprehension syntax - similar to usage in f#, or the foreach library in R
    rawArticles = {i : rawArticles[i] for i in range(len(rawArticles))}
    
    return rawArticles

"""collects the contents of a webpage based on it's URL, then parses it into an array of paragraphs"""   
def scrapeArticleUrl(url):
 
    page = requests.get(url)
    soup = bs(page.text, 'html.parser')
    
    for x in soup("script"): x.decompose()
    for x in soup("meta"): x.decompose()
    for x in soup("link"): x.decompose()    
    for x in soup("span"): x.decompose()
    for x in soup("header"): x.decompose()
    for x in soup("nav"): x.decompose()
    for x in soup("li"): x.decompose()
        
    return [ p.get_text()+' endofpar ' for p in soup('p') if len(p.get_text().split(' '))>1]



#def WriteArticlesToCSV: