from repoCrawler import repo_crawler,repo_info_crawler
from urlParser import url_parser
from csvParser import read_csv
from sqliteParser import sqlite_parser

import json,requests
from requests.auth import HTTPBasicAuth

AUTHO_SITE = "https://api.github.com/authorizations"
data = '{"scopes":["repo"]}'
def get_token(usrname,pswd):
    return True,"YOUR TOKEN"
    try:
        res = requests.post(AUTHO_SITE,data=data,auth=HTTPBasicAuth(usrname, pswd))
        response = res.json()
        if ('token' in response.keys()):
            return True,response['token']
        else:
            return False,"Authorization Failed"
    except Exception as e:
        return False,e

if __name__ == "__main__":
    import_filename = './import/github_urlist.csv'
    is_succeed,oauth_token = get_token('kirbyszsr','Jinan200908')

    if is_succeed:
        lists_sorted = url_parser(read_csv(import_filename),True)
        info = repo_crawler(lists_sorted,oauth_token)
        print(info)
        repo_info_crawler(info)
        sqlite_parser(info)
    else:
        print(oauth_token)