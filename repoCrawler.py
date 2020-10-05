import json
import requests
import os
import shutil
import zipfile
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

OUT_PUT_LIB = "./output"

#personal token to access github api(only for accessing)
AUTHO_TOKEN='*YOUR TOKEN*'

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
            if basic_info != []:
                if basic_info['language'] == filter_type:
                    print('is' + filter_type + ':',[userName,repoName])
                    returnvals += [[userName,repoName]]
                else:
                    print('Type_filter: repository',userName+ '/' +repoName,"is not a",filter_type,"project,type=",basic_info['language'])
            else:
                print('Type_filter: repository',userName, repoName," not found")
        except Exception as e:
            print('Type_filter Error:', userName, repoName, e)
    return returnvals


def repo_info_crawler(userName,repoName):
#use github api to crawl basic repo infomations
    returnval = []
    #print(userName, repoName)
    repo_url = urljoin(API_BASE_URL, 'repos/' + userName + '/' + repoName)
    try:
        print("repo_info_crawler:", userName, repoName)
        rsp = requests.get(repo_url,
                           headers={'Accept': 'application/json',
                                    'Authorization': 'token ' + AUTHO_TOKEN})
        if rsp.status_code == requests.codes.ok:
            returnval = json.loads(rsp.text)
    except:
        returnval = []
    return returnval


def branch_info_crawler(userName,repoName):
    returnval = {"branch_datas" : []}

    repo_url = urljoin(API_BASE_URL, 'repos/' + userName + '/' + repoName + BRANCH_SUB_URL)
    try:
        print("branch_info_crawler:", userName, repoName)
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
    except Exception as e:
        print("branch_info_crawler ERROR",userName,repoName,e)
    return returnval


def pull_info_crawler(userName,repoName):
    returnval = {"pull_datas": []}
    pull_url = urljoin(API_BASE_URL, 'repos/' + userName + '/' + repoName + PULL_SUB_URL)
    try:
        print("pull_info_crawler:", userName, repoName)
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
    except Exception as e:
        print("pull_info_crawler ERROR",userName,repoName, e)
    return returnval


def issue_info_crawler(userName,repoName):
    returnval = {"issue_datas": []}
    issue_url = urljoin(API_BASE_URL, 'repos/' + userName + '/' + repoName + ISSUE_SUB_URL)
    try:
        print("issue_info_crawler:", userName, repoName)
        rsp = requests.get(issue_url,
                           headers={'Accept': 'application/json',
                                    'Authorization': 'token ' + AUTHO_TOKEN})
        if rsp.status_code == requests.codes.ok:
            issues = json.loads(rsp.text)
        for issue in issues:
            issue_info = {}
            issue_info["issue_url"] = BRANCH_BASE_URL + userName + "/" + repoName + ISSUE_SUB_URL + "/" + str(issue["number"])
            issue_info["issue_title"] = issue["title"]
            issue_info["issue_number"] = issue["number"]
            issue_info["issue_text"] = issue["body"]
            issue_info["issue_comments"] = []
            issue_comment_url = urljoin(issue_url + '/', str(issue_info["issue_number"]) + '/comments')
            com_rsp = requests.get(issue_comment_url,
                                   headers={'Accept':'application/json',
                                            'Authorization': 'token '+ AUTHO_TOKEN})
            if com_rsp.status_code == requests.codes.ok:
                comments = json.loads(com_rsp.text)
            else:
                comments = []
            for comment in comments:
                comment_info = {}
                comment_info["comment_username"] = comment["user"]["login"]
                comment_info["comment_create_time"] = comment["created_at"]
                comment_info["comment_edit_time"] = comment["updated_at"]
                comment_info["comment_text"] = comment["body"]

                issue_info["issue_comments"].append(comment_info)
            returnval["issue_datas"].append(issue_info)
    except Exception as e:
        print("issue_info_crawler ERROR", userName, repoName, e)
    return returnval


def repo_file_crawler(repo_infos):
    #input: repo info crawled in function repo_crawler
    #output: completed repo files. Organized as below:
    #./output
    #     |repo1
    #        |----branch1
    #               \------branch1-folder1
    #               \------branch1-folder2
    #                             \------branch1-flie..
    #        |----branch2
    #...
    #     | repo2
    #.....etc.
    for repo in repo_infos:
        repo_name = repo["github_info"]["name"]
        branches = repo["github_branches"]["branch_datas"]
        for branch in branches:
            print('repo file download: branch downloading - ', repo_name, branch["branch_version"])
            #use http to download branch data zip
            version = branch["branch_version"]
            download_url = branch["branch_download_url"]
            try:
                r = requests.get(download_url)
                file_dir = './output/' + repo_name + '/' + version
                if os.path.exists(file_dir):
                    shutil.rmtree(file_dir)
                os.makedirs(file_dir)

                zip_dir = file_dir + '/' + version + '.zip'
                print(zip_dir + ' download started..')
                with open(zip_dir,"wb+") as f:
                    print(os.path.abspath(zip_dir))
                    f.write(r.content)
                    print(zip_dir + ' download succeed')
                    f.close()

                #extract zip file
                    zip_file = zipfile.ZipFile(zip_dir)
                    zip_list = zip_file.namelist()
                    for file in zip_list:
                        if is_setting_file(file):
                            zip_file.extract(file,file_dir)
                    zip_file.close()

                #delete zip file
                os.remove(zip_dir)
            except Exception as e:
                print("repo file download exception:",repo_name,version,download_url,e)
    return None

def repo_info_outputer(repo_infos):
    for repo in repo_infos:
        repo_name = repo["github_info"]["name"]
        file_dir = './output/' + repo_name
        file_name = file_dir + '/' + repo_name[repo_name.find('/') + 1:] + '_info.json'
        if not os.path.exists(file_dir):
            os.makedirs(file_dir)
        try:
            print('repo_info_outputer:',repo_name,file_dir)
            with open(file_name,'w+') as file:
                json.dump(repo,file)
        except Exception as e:
            print("repo_info_outputer ERROR:",repo_name,file_dir,file_name,e)
    return

def is_setting_file(filename):
    #thanks to oppenoffice.org
    # #http://www.openoffice.org/dev_docs/source/file_extensions.html
    codefile_suffixs = ['.a','.asm','.asp','.awk','.bat',
                        '.btm','.BTM','.c','.class','.cmd',
                        '.h','.h','.cpp','.py','.pyc','.DES',
                        '.dll','don','.dpc','.dpj','.dump',
                        '.dxp','.eng','.exe','.flt','.fmt',
                        '.hpp','.hrc','.html','.hxx','.Hxx',
                        '.HXX','.ico','.idl','IDL','ih',
                        '.omc','.inf','.java','.jar','.js',
                        '.jsp','.lib','lnk','.kbx','.o',
                        '.obj','.s','.src','.srs','.y','.yxx']
    sourcefile_suffixs = ['.bmp','.csv','.cur','.cxx','.CXX',
                          '.db','.def','.jpg','.png','.dlg',
                          '.font','.ft','.gif','.LOG','.pfa',
                          '.PS','.ttf','.TTF','.wav','.zip']
    for suffix in codefile_suffixs + sourcefile_suffixs:
        if filename.endswith(suffix):
            return False
    return True

if __name__ == "__main__":
    lists_sorted = url_parser(read_csv('./import/github_urlist.csv'),True)
    #returnvals = repo_crawler(lists_sorted)
    returnvals = repo_crawler([['spacewalkproject', 'spacewalk'], ['Jasig', 'cas'], ['wildfly-security', 'jboss-negotiation'],
     ['eclipse', 'jetty.project'], ['netty', 'netty'], ['alkacon', 'opencms-core'],
     ['orientechnologies', 'orientdb'], ['picketlink', 'picketlink-bindings'], ['apache', 'activemq-artemis'],
     ['elastic', 'elasticsearch'], ['isucon', 'isucon5-qualify'], ['floodlight', 'floodlight'],
     ['jhy', 'jsoup'], ['googlei18n', 'sfntly'], ['miltonio', 'milton2'], ['theguly', 'DecryptOpManager']],False)
    print(returnvals)
    """
    returnvals = [['spacewalkproject', 'spacewalk'], ['Jasig', 'cas'], ['wildfly-security', 'jboss-negotiation'],
     ['eclipse', 'jetty.project'], ['netty', 'netty'], ['alkacon', 'opencms-core'],
     ['orientechnologies', 'orientdb'], ['picketlink', 'picketlink-bindings'], ['apache', 'activemq-artemis'],
     ['elastic', 'elasticsearch'], ['isucon', 'isucon5-qualify'], ['floodlight', 'floodlight'],
     ['jhy', 'jsoup'], ['googlei18n', 'sfntly'], ['miltonio', 'milton2'], ['theguly', 'DecryptOpManager']]
    """
    """
    [['spacewalkproject', 'spacewalk'], ['Jasig', 'cas'], ['wildfly-security', 'jboss-negotiation'], 
    ['eclipse', 'jetty.project'], ['netty', 'netty'], ['alkacon', 'opencms-core'], 
    ['orientechnologies', 'orientdb'], ['picketlink', 'picketlink-bindings'], ['apache', 'activemq-artemis'], 
    ['elastic', 'elasticsearch'], ['isucon', 'isucon5-qualify'], ['floodlight', 'floodlight'], 
    ['jhy', 'jsoup'], ['googlei18n', 'sfntly'], ['miltonio', 'milton2'], ['theguly', 'DecryptOpManager']]
    """
    #returnvals = [['theguly', 'DecryptOpManager']]
    #info = repo_crawler(returnvals)

    #repo_info_crawler('netty', 'netty')
    #repo_file_crawler([['netty', 'netty']])
    #repo_info_crawler(info)
    #print(info)