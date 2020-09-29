#!/usr/bin/python
# -*- coding: UTF-8 -*-
import csv
from urlParser import url_parser

def read_csv(file):
    # read csv file and convert the urls into lists
    result = []
    with open(file, 'r') as f:
        reader = csv.reader(f)
        # is_header = True
        for row in reader:
            result.append(row[1])
    return result

def url_parser_csv(filename,check_duplicated=True):
    urls = read_csv(filename)
    repository_lists = url_parser(urls,check_duplicated)
    return repository_lists

if __name__ == "__main__" :
    lists = read_csv('./import/github_urlist.csv')
    print(lists)
    parsed_list = url_parser_csv('./import/github_urlist.csv',False)
    print(parsed_list)
    parsed_list_checked = url_parser_csv('./import/github_urlist.csv',True)
    print(parsed_list_checked)
