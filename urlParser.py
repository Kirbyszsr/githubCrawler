from csvParser import read_csv

def url_parser(urls,check_duplicated=True):
    #parse urls into lists including [userName,repositoryName]
    INFO = '//github.com/'
    repos = []
    for url in urls:
        account_name_index = url.find(INFO)
        #only parse urls with 'github.com/'
        if account_name_index == -1:
            continue
        next_slash = url.find('/',account_name_index + len(INFO))
        account_name = url[account_name_index + len(INFO):next_slash]
        another_slash = url.find('/',next_slash + 1)
        if another_slash != -1:
            repo_name = url[next_slash + 1:another_slash]
        else:
            repo_name = url[next_slash + 1:]
        repos += [[account_name,repo_name]]
        #print([url,account_name,repo_name])

    repos_sorted = []
    if not check_duplicated:
        repos_sorted = repos
    else:
        for repo in repos:
        #check for duplicated repos
            is_duplicated = False
            for line in repos_sorted:
                if line[0] == repo[0] and line[1] == repo[1]:
                    is_duplicated = True
            if not is_duplicated:
                repos_sorted.append(repo)
    return repos_sorted

if __name__ == "__main__":
    lists = url_parser(read_csv('./import/github_urlist.csv'),False)
    print(lists)
    lists_sorted = url_parser(read_csv('./import/github_urlist.csv'),True)
    print(lists_sorted)