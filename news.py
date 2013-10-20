import requests
import json
import sys


feedzilla = 'http://api.feedzilla.com'
cityFile = 'imp-cities.csv'

def getDBName(cityId):
    return "db/"+str(cityId)
    
def search(query, count=10, title_only=False):
    api = feedzilla + '/v1/articles/search.json'
    payload = {'q': query, 'count': count, 'title_only': int(title_only), 'order':'relevance'}
    r = requests.get(api, params=payload)
    return r.json()

def getNews(cityId, articleCount):
    dbFile = getDBName(cityId)
    db = open(dbFile, 'r')
    s = json.load(db)
    db.close()
    articles = s['articles']
    return articles[0:articleCount]
    

def createDataBase():
    f = open(cityFile, 'r')
    l = f.readline()
    while l:
        l = l.strip()
        fields = l.split(',')
        cityId = int(fields[0])
        query = fields[2]
        print "Querying for %d, %s" %(cityId, query)
        news = json.dumps(search(query))
        
        dbfile = getDBName(cityId)
        db = open(dbfile, 'w')
        db.write(news)
        db.close()
        
        l = f.readline()
    f.close()


if __name__ == '__main__':
    if len(sys.argv) >= 2:
        q = ' '.join(sys.argv[1:])
        print 'Now querying {} ...'.format(q)
        result = search(q, title_only=True, count=5)
        print json.dumps(result, indent = 4)
    elif len(sys.argv) == 1:
        createDataBase()
