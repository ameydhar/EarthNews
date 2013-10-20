#----------------------------------------------------------------------------#
# Imports.
#----------------------------------------------------------------------------#

import os
from flask import * # do not use '*'; actually input the dependencies.
import logging
from logging import Formatter, FileHandler
import json
from news import *

#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
app.config.from_object('config')

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#

@app.route('/')
def home():
    return render_template('pages/index.html')

@app.route('/query',methods=['GET'])
def handleQuery():
    """
    Query Types:
       1. ?qtype=cityList&lat1=topRightLat&long1=topRightLong&lat2=bottomLeftLat&long2=bottomLeftLog
       2. ?qtype=news&lat1=topRightLat&long1=topRightLong&lat2=bottomLeftLat&long2=bottomLeftLog
    """
    query = request.args
    qdict = {}
    for queryItem in query.iteritems():
        qdict[queryItem[0]] = queryItem[1]
    if qdict['qtype'] == "cityList":
        s = getCityList(float(qdict['lat1']),float(qdict['long1']), float(qdict['lat2']),float(qdict['long2'])) 
    if qdict['qtype'] == "news":
        r = getCityList(float(qdict['lat1']),float(qdict['long1']), float(qdict['lat2']),float(qdict['long2']))
        s = buildNews(r)   
    return json.dumps(s)
# Error handlers.

#@app.errorhandler(500)
#def internal_error(error):
    #db_session.rollback()
#    print '500'

@app.errorhandler(404)
def internal_error(error):
    return '404'

if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(Formatter('%(asctime)s %(levelname)s: %(message)s '
    '[in %(pathname)s:%(lineno)d]'))
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Helping functions
#----------------------------------------------------------------------------#

cityFile = 'imp-cities.csv'
cityList = []

def getNewsItemsCount(cityCount):
    if cityCount == 1:
        return 10
    if cityCount == 2:
        return 5
    if cityCount == 3:
        return 3
    if cityCount == 5:
        return 2
    if cityCount > 5:
        return 1

def buildNews(mappedCities):
    n  = len(mappedCities)
    newsItems = getNewsItemsCount(n)
    news = {}
    news['articles'] = []
    for item in mappedCities:
        lat = item[-2]
        lg = item[-1]
        cityId = item[0]
        cityName = item[2]
        articles = getNews(cityId, newsItems)
        for article in articles:
            article['latitude'] = lat
            article['longitude'] = lg
            article['cityName'] = cityName
            news['articles'].append(article)
    return news
        
        
    
def buildCityList():
    f = open(cityFile, 'r')
    lines = f.readlines()
    f.close()
    
    global cityList
    for line in lines:
        line = line.strip()
        fields = line.split(',')
        fields[0] = int(fields[0])
        fields[3] = int(fields[3])
        fields[4] = float(fields[4])
        fields[5] = float(fields[5])
        cityList.append(fields)

def getCityList(lat1, long1, lat2, long2):
    l = []
    for item in cityList:
        lat = item[-2]
        lg = item[-1]
        cityId = item[0]
        cityName = item[2]
        if contains(lat1, long1, lat2, long2, lat, lg):
            l.append(item)
    return l

def contains(lat1, long1, lat2, long2, lat, lg):
    if lat <= lat1 and lat >=lat2 and lg <= long1 and lg >= long2:
        return 1
    return 0        
#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#
    
if __name__ == '__main__':
    # pre req
    buildCityList()
    # Specify port manually:
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
    # Default port:
    #app.run()
    
    
