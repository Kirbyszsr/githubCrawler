# githubCrawler
**a github repository using Github API v3 by kirbyszsr**

version 0.8

# What is githubCrawler?

一个用于爬取github仓库的python爬虫程序，可以用于爬取目标仓库的基本信息。

可以爬取的信息是：仓库基本信息，分支信息，版本信息，合并请求信息及仓库各分支的配置文件。

# Settings
python 3.7
使用csv,zipfile,shutil,requests,json依赖库

## input
在根目录的import文件夹下使用csv文件存储的github url信息。
示例见本工程的import文件夹。

注意：只有url中带有http://github.com或https://github.com的github仓库会被正常读取。

## output
爬取的信息全部放置在工程文件夹的output文件夹下

各个合法url仓库的基本信息会放置在./output/[ownerName]/[repoName]/[repoName]_info.json中以json文件存储。

该仓库各个分支的配置文件信息会放置在./output/[ownerName]/[repoName]/[branchName]文件夹下。

**这些文件均会维持其在原分支的文件位置。例如某文件是netty/netty仓库3.2分支下licence子文件夹下内容，则该文件的下载位置会在/output/netty-3.2/licence/文件夹下。**

## How to use it?

由于Github API v3限制未认证ip每小时只有60次请求，需要使用您的个人Access Token进行验证。

登录github网站后，进入https://github.com/settings/tokens

点击Generate new token后，按照提示创建一个token。注意，您只需要授权user相关权限即可。

将得到的Token填入repoCrawler.py的AUTHO_TOKEN=字段，运行repoCrawler即可。注意，需要保留AUTHO_TOKEN前后的引号。

## How is it generated?

###csvParser.py
用于将.csv文件中的github url中所含的url提取出来形成url列表。

###urlParser.py
将url列表中每个url的仓库基本信息提取出来。只提取其中的拥有者名和仓库名。

###repoCrawler.py
使用提取出来的仓库基本信息爬取仓库各项数据，保存文件并生成仓库描述json信息。

###sqliteParser.py
暂时未开发，用于将获得的json信息存入sqlite数据库。