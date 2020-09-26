#!/usr/bin/python
# -*- coding: UTF-8 -*-
import csv


def read_csv(file):
    # read csv file and convert the urls into lists
    result = []
    with open(file, 'r') as f:
        reader = csv.reader(f)
        # is_header = True
        for row in reader:
            result.append(row[1])
    return result

def url_parser_csv(filename):
    urls = read_csv(filename)
    repository_lists = url_parser(urls)
    return repository_lists

if __name__ == "__main__" :
    lists = read_csv('./import/github_urlist.csv')
    print(lists)
    parsed_list = url_parser_csv('./import/github_urlist.csv')
    print(parsed_list)