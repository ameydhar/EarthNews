import requests
import json
import sys


feedzilla = 'http://api.feedzilla.com'


def search(query, count=10, title_only=False):
    api = feedzilla + '/v1/articles/search.json'
    payload = {'q': query, 'count': count, 'title_only': int(title_only)}
    r = requests.get(api, params=payload)
    return r.json()





if __name__ == '__main__':
    if len(sys.argv) < 2:
        print 'python {} <keyword>'.format(sys.argv[0])
        sys.exit(-1)
    q = ' '.join(sys.argv[1:])
    print 'Now querying {} ...'.format(q)
    
    result = search(q, title_only=True, count=5)
    print json.dumps(result, sort_keys=True, indent=4)
