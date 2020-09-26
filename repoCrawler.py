import json
import requests
from urllib.parse import urljoin

from urlParser import url_parser
from csvParser import read_csv
#github api URL
BASE_URL = "https://api.github.com/"
#personal token to access github api(only for accessing)
AUTHO_TOKEN = "b67a27f531e38dcfe5d2980b4ffe4ed8325c92b0"


def repo_crawler(repoLists,typefilter_enabled=True,filter_type='Java'):
    return type_filter(repoLists,typefilter_enabled,filter_type)

def type_filter(repoLists,typefilter_enabled,filter_type):
    if not typefilter_enabled:
        return repoLists
    returnvals = []
    #crawl repository by [userName,repositoryName]
    for [userName,repoName] in repoLists:
        print(userName,repoName)
        repo_url = urljoin(BASE_URL, 'repos/' + userName + '/' + repoName)
        try:
            rsp = requests.get(repo_url,
                               headers={'Accept': 'application/json',
                                        'Authorization': 'token ' + AUTHO_TOKEN})
            if rsp.status_code == requests.codes.ok:
                returnval = json.loads(rsp.text)
                if returnval['language'] == filter_type:
                    print('is' + filter_type + ':',[userName,repoName])
                    returnvals += [[userName,repoName]]
        except:
            print('Error:',userName,repoName,rsp)
            continue
    return returnvals



if __name__ == "__main__":
    lists_sorted = url_parser(read_csv('./import/github_urlist.csv'),True)
    returnvals = repo_crawler(lists_sorted)
    print(returnvals)
    """
    [['spacewalkproject', 'spacewalk'], ['Jasig', 'cas'], ['wildfly-security', 'jboss-negotiation'], 
    ['eclipse', 'jetty.project'], ['netty', 'netty'], ['alkacon', 'opencms-core'], 
    ['orientechnologies', 'orientdb'], ['picketlink', 'picketlink-bindings'], ['apache', 'activemq-artemis'], 
    ['elastic', 'elasticsearch'], ['isucon', 'isucon5-qualify'], ['floodlight', 'floodlight'], 
    ['jhy', 'jsoup'], ['googlei18n', 'sfntly'], ['miltonio', 'milton2'], ['theguly', 'DecryptOpManager']]
    """