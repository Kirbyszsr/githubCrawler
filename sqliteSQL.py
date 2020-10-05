FOREIGN_KEY_ON = "PRAGMA foreign_keys = ON"


GITHUB_REPO_INFO_DROP = """DROP TABLE IF EXISTS github_repo_info;"""
GITHUB_REPO_INFO_CREATE = """CREATE TABLE github_repo_info(
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            url VARCHAR(256),
                            name VARCHAR(256),
                            language VARCHAR(32)
                            );"""
GITHUB_REPO_INFO_INSERT = """INSERT INTO 
                            github_repo_info(url,name,language)
                            VALUES(?,?,?);
                            """
GITHUB_REPO_INFO_SELECT = """SELECT * FROM github_repo_info;"""
GITHUB_REPO_INFO_SELECT_ID = """SELECT id FROM github_repo_info WHERE name = (?);"""

GITHUB_BRANCHES_INFO_DROP = """DROP TABLE IF EXISTS github_branches;"""
GITHUB_BRANCHES_INFO_CREATE = """CREATE TABLE github_branches(
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                repo_id INTEGER,
                                version VARCHAR(256),
                                branch_url VARCHAR(256),
                                download_url VARCHAR(256),
                                FOREIGN KEY (repo_id) REFERENCES github_repo_info(id)
                                on delete cascade on update cascade
                                );
                            """
GITHUB_BRANCHES_INFO_INSERT = """INSERT INTO
                                github_branches(repo_id,version,branch_url,download_url)
                                values(?,?,?,?);
                                """
GITHUB_BRANCHES_INFO_SELECT = """SELECT * FROM github_branches;"""

GITHUB_PULL_REQUESTS_INFO_DROP = """DROP TABLE IF EXISTS pull_request_info;"""
GITHUB_PULL_REQUESTS_INFO_CREATE = """CREATE TABLE pull_request_info(
                                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                                        repo_id INTEGER,
                                        pull_number INTEGER,
                                        pull_title text,
                                        pull_version VARCHAR(256),
                                        pull_version_url VARCHAR(256),
                                        FOREIGN KEY (repo_id) REFERENCES github_repo_info(id)
                                        on delete cascade on update cascade                                        
                                        );
                                    """
GITHUB_PULL_REQUESTS_INFO_INSERT = """INSERT INTO
                                    pull_request_info(repo_id,pull_number,pull_title,pull_version,pull_version_url)
                                    values(?,?,?,?,?);
                                    """
GITHUB_PULL_REQUESTS_INFO_SELECT = """SELECT * FROM pull_request_info;"""

GITHUB_ISSUES_INFO_DROP = """DROP TABLE IF EXISTS github_issues_info;"""
GITHUB_ISSUES_INFO_CREATE = """CREATE TABLE github_issues_info(
                                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                                    repo_id INTEGER,
                                    issue_url VARCHAR(256),
                                    issue_title TEXT,
                                    issue_number int,
                                    issue_text TEXT,
                                    FOREIGN KEY (repo_id) REFERENCES github_repo_info(id)
                                    on delete cascade on update cascade                                                                
                            );"""
GITHUB_ISSUES_INFO_INSERT = """INSERT INTO
                            github_issues_info(repo_id,issue_url,issue_title,issue_number,issue_text)
                            values(?,?,?,?,?);
                            """
GITHUB_ISSUES_INFO_SELECT = """SELECT * FROM github_issues_info;"""
GITHUB_ISSUES_INFO_SELECT_ID = """SELECT id FROM github_issues_info WHERE repo_id = (?) and issue_number = (?);"""

GITHUB_ISSUE_COMMENTS_INFO_DROP = """DROP TABLE IF EXISTS github_issues_comments;"""
GITHUB_ISSUE_COMMENTS_INFO_CREATE = """CREATE TABLE github_issues_comments(
                                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                                    issue_id INTEGER,
                                    comment_username VARCHAR(256),
                                    comment_create_time CHAR(20),
                                    comment_edit_time CHAR(20),
                                    comment_text TEXT,
                                    FOREIGN KEY (issue_id) REFERENCES github_issues_info(id)
                                    on delete cascade on update cascade   
                                    );
                                    """
GITHUB_ISSUE_COMMENTS_INFO_INSERT = """INSERT INTO
                                    github_issues_comments(issue_id,comment_username,comment_create_time,
                                    comment_edit_time,comment_text)
                                    values(?,?,?,?,?);
                                    """