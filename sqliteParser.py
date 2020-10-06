import sqlite3
import sqliteSQL
import json

def sqlite_parser(repo_info,sqlite_database="./output/sqlite_database.db"):
    #input: repo info crawled in function repo_crawler,
    #       target sqlite database to write repo info
    #output: sqlite database
    try:
        conn = sqlite3.connect(sqlite_database)
        print('connection succeed')
        cursor = conn.cursor()
        #create databases
        create_databases(cursor)
        conn.commit()
        for repo in repo_info:
            cursor.execute(sqliteSQL.GITHUB_REPO_INFO_INSERT,
                           (repo["github_url"],repo["github_info"]["name"],repo["github_info"]["language"]))
            print('repo_info succeed')
            conn.commit()
            repo_id = cursor.execute(
                sqliteSQL.GITHUB_REPO_INFO_SELECT_ID,
                (repo["github_info"]["name"],)).fetchone()[0]
            print('repo id:',repo_id)
            for branches in repo["github_branches"]["branch_datas"]:
                cursor.execute(sqliteSQL.GITHUB_BRANCHES_INFO_INSERT,
                               (repo_id,branches["branch_version"],branches["branch_url"],branches["branch_download_url"],))
                conn.commit()
                print('branches succeed')
            for pull_data in repo["github_pull_requests"]["pull_datas"]:
                cursor.execute(sqliteSQL.GITHUB_PULL_REQUESTS_INFO_INSERT,
                               (repo_id,pull_data["pull_number"],pull_data["pull_title"],
                               pull_data["pull_version"],pull_data["pull_version_url"],))
                conn.commit()
                print('pull_data succeed')
            for issue in repo["github_issues"]["issue_datas"]:
                cursor.execute(sqliteSQL.GITHUB_ISSUES_INFO_INSERT,
                               (repo_id,issue["issue_url"],issue["issue_title"],issue["issue_number"],issue["issue_text"],))
                conn.commit()
                print('issue succeed')
                issue_id = cursor.execute(
                    sqliteSQL.GITHUB_ISSUES_INFO_SELECT_ID,
                    (repo_id,issue["issue_number"],)).fetchone()[0]
                for comment in issue["issue_comments"]:
                    cursor.execute(sqliteSQL.GITHUB_ISSUE_COMMENTS_INFO_INSERT,
                                   (issue_id,comment["comment_username"],comment["comment_create_time"],
                                    comment["comment_edit_time"],comment["comment_text"],))
                    conn.commit()
                print('comment succeed')
    except Exception as e:
        print('sqlite_parser ERROR:',sqlite_database,e)
    return

def create_databases(cursor_):
    try:
        cursor_.execute(sqliteSQL.GITHUB_REPO_INFO_DROP)
        cursor_.execute(sqliteSQL.GITHUB_REPO_INFO_CREATE)

        cursor_.execute(sqliteSQL.GITHUB_BRANCHES_INFO_DROP)
        cursor_.execute(sqliteSQL.GITHUB_BRANCHES_INFO_CREATE)

        cursor_.execute(sqliteSQL.GITHUB_PULL_REQUESTS_INFO_DROP)
        cursor_.execute(sqliteSQL.GITHUB_PULL_REQUESTS_INFO_CREATE)

        cursor_.execute(sqliteSQL.GITHUB_ISSUES_INFO_DROP)
        cursor_.execute(sqliteSQL.GITHUB_ISSUES_INFO_CREATE)

        cursor_.execute(sqliteSQL.GITHUB_ISSUE_COMMENTS_INFO_DROP)
        cursor_.execute(sqliteSQL.GITHUB_ISSUE_COMMENTS_INFO_CREATE)
    except Exception as e:
        print('create_databases ERROR',e)
    return

def repo_insert():
    return

if __name__ == "__main__":
    json_file = open('./import/info.json','rb')
    info_json = json.load(json_file)
    print(info_json)
    sqlite_parser(info_json)