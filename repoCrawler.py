import json
import requests
from urllib.parse import urljoin
from urlParser import url_parser
from csvParser import read_csv
#github api URL
API_BASE_URL = "https://api.github.com/"
REPO_BASE_URL = "https://www.github.com/repos/"
BRANCH_BASE_URL = "https://github.com/"

BRANCH_DOWNLOAD_SUB_URL = "/archive"
TREE_SUB_URL = "/tree"
BRANCH_SUB_URL = "/branches"
PULL_SUB_URL = "/pulls"
ISSUE_SUB_URL = "/issues"

#personal token to access github api(only for accessing)
AUTHO_TOKEN='*YOUR GITHUB AUTHORIRIZE TOKEN*'

def repo_crawler(repoLists,typefilter_enabled=True,filter_type='Java'):
    infos = []

    repo_list_to_crawl = type_filter(repoLists,typefilter_enabled,filter_type)
    for [userName,repoName] in repo_list_to_crawl:
        repo_info = {}
        basic_infos = repo_info_crawler(userName,repoName)

        repo_info["github_url"] =  basic_infos["html_url"]

        github_info = {}
        github_info["name"] = basic_infos["full_name"]
        github_info["language"] = basic_infos["language"]
        repo_info["github_info"] = github_info

        repo_info["github_branches"] = branch_info_crawler(userName,repoName)

        repo_info["github_pull_requests"] = pull_info_crawler(userName,repoName)

        repo_info["github_issues"] = issue_info_crawler(userName,repoName)

        infos.append(repo_info)


    return infos



def type_filter(repoLists,typefilter_enabled,filter_type):
    if not typefilter_enabled:
        #type_filter not enabled
        return repoLists
    returnvals = []
    #crawl repository by [userName,repositoryName]
    for [userName,repoName] in repoLists:
        try:
            basic_info = repo_info_crawler(userName,repoName)
            if basic_info['language'] == filter_type:
                #print('is' + filter_type + ':',[userName,repoName])
                returnvals += [[userName,repoName]]
        except:
            print('Type_filter Error:', userName, repoName)
    return returnvals


def repo_info_crawler(userName,repoName):
#use github api to crawl basic repo infomations
    returnval = []
    #print(userName, repoName)
    repo_url = urljoin(API_BASE_URL, 'repos/' + userName + '/' + repoName)
    rsp = requests.get(repo_url,
                       headers={'Accept': 'application/json',
                                'Authorization': 'token ' + AUTHO_TOKEN})
    if rsp.status_code == requests.codes.ok:
        returnval = json.loads(rsp.text)
    return returnval


def branch_info_crawler(userName,repoName):
    returnval = {"branch_datas" : []}

    repo_url = urljoin(API_BASE_URL, 'repos/' + userName + '/' + repoName + BRANCH_SUB_URL)
    try:
        rsp = requests.get(repo_url,
                           headers={'Accept': 'application/json',
                                    'Authorization': 'token ' + AUTHO_TOKEN})
        if rsp.status_code == requests.codes.ok:
            branches = json.loads(rsp.text)
            for branch in branches:
                branch_info = {}
                branch_info["branch_version"] = branch["name"]
                # branch_api_url = branch["commit"]["url"]
                branch_info["branch_url"] = BRANCH_BASE_URL + userName +"/" + repoName + TREE_SUB_URL + "/" + branch_info["branch_version"]
                branch_info["branch_download_url"] = BRANCH_BASE_URL + userName +"/" + repoName \
                                                     + BRANCH_DOWNLOAD_SUB_URL + "/" + branch_info["branch_version"] + ".zip"
                #rsp1 = requests.get(branch_api_url,
                #                    headers={'Accept': 'application/json',
                #                             'Authorization': 'token ' + AUTHO_TOKEN})
                #if rsp1.status_code == requests.codes.ok:
                #    branch_data = json.loads(rsp1.text)
                #    branch_info["branch_url"] = branch_data["html_url"]

                #else:
                #    branch_info["branch_url"] = ""
                #    branch_info["branch_download_url"] = ""
                returnval["branch_datas"].append(branch_info)
    except:
        print("branch_info_crawler ERROR",userName,repoName)
    return returnval



def pull_info_crawler(userName,repoName):
    returnval = {"pull_datas": []}
    pull_url = urljoin(API_BASE_URL, 'repos/' + userName + '/' + repoName + PULL_SUB_URL)
    try:
        rsp = requests.get(pull_url,
                           headers={'Accept': 'application/json',
                                    'Authorization': 'token ' + AUTHO_TOKEN})
        if rsp.status_code == requests.codes.ok:
            pulls = json.loads(rsp.text)
        for pull in pulls:
            pull_info = {}
            pull_info["pull_number"] = pull["number"]
            pull_info["pull_title"] = pull["title"]
            pull_info["pull_version"] = pull["base"]["label"]
            pull_info["pull_version_url"] = BRANCH_BASE_URL + userName +"/" + repoName + TREE_SUB_URL + "/" + pull["base"]["ref"]

            returnval["pull_datas"].append(pull_info)
    except:
        print("pull_info_crawler ERROR",userName,repoName)
    return returnval


def issue_info_crawler(userName,repoName):
    returnval = {"issue_datas": []}
    return {}

if __name__ == "__main__":
    #lists_sorted = url_parser(read_csv('./import/github_urlist.csv'),True)
    #returnvals = repo_crawler(lists_sorted)
    #print(returnvals)
    """
    [['spacewalkproject', 'spacewalk'], ['Jasig', 'cas'], ['wildfly-security', 'jboss-negotiation'], 
    ['eclipse', 'jetty.project'], ['netty', 'netty'], ['alkacon', 'opencms-core'], 
    ['orientechnologies', 'orientdb'], ['picketlink', 'picketlink-bindings'], ['apache', 'activemq-artemis'], 
    ['elastic', 'elasticsearch'], ['isucon', 'isucon5-qualify'], ['floodlight', 'floodlight'], 
    ['jhy', 'jsoup'], ['googlei18n', 'sfntly'], ['miltonio', 'milton2'], ['theguly', 'DecryptOpManager']]
    """


    print(repo_crawler([['netty', 'netty']]))
