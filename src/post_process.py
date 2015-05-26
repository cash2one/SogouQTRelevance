#! -*- coding: utf-8 -*-
'''
1. query == title ? score = 3;
2. query == title_del_sub(����ո�+��������������������()������)������score > 2.4 or sub_title_len < 13 ? score = 3;
3. title��del_sub_title��['#name?', '�û���¼', '��ʾ��Ϣ', '��¼', '404', '404ҳ��', '����404', '404-����Ͱ�']��title����['������ʾ', ''] ? score = 0
4. title�� ���ʡ��ѹ��ڡ��ģ�score < 1�Ľ�Ϊ0.0
'''

import sys
from util import *

def post_process(result_file, output):
    bad_title_set = set(['#name?', '�û���¼', '��ʾ��Ϣ', '��¼', '404', '404ҳ��', '����404', '404-����Ͱ�'])
    count_list = [0 for i in range(4)]
    with open(output, 'w') as fout:
        with open(result_file) as fin:
            for line in fin:
                query, title, id, score = line.rstrip().split('\t')
                # query = gbk2unicode(query)
                # title = gbk2unicode(title)
                title_del_sub, sub_title = del_sub_title(title)
                title_del_sub = process_title(title_del_sub)
                sub_title = process_title(sub_title)
                if query == title:
                    # print 'query: %s, title: %s' % (query, title)
                    score = 3
                    count_list[0] += 1
                elif query == title_del_sub and (len(gbk2unicode(sub_title)) < 5 or float(score) > 2.7):
                    pass
                    print 'query: %s, title: %s, title_del_sub: %s, score: %s, sub_title_len: %d' % (query, title, title_del_sub, score, len(gbk2unicode(sub_title)))
                    score = 3
                    count_list[1] += 1
                elif title in bad_title_set or title_del_sub in bad_title_set or '������ʾ' in title or '���ʳ���' in title:
                    print 'bad title: %s' % title
                    score = 0
                    count_list[2] += 1
                elif '�ѹ���' in title and float(score) < 1:    # useless
                    print 'query: %s, bad title: %s' % (query, title)
                    score = 0
                    count_list[3] += 1
                fout.write(query + '\t' + title + '\t' + id + '\t' + str(score) + '\n')
            print count_list
def main():
    if len(sys.argv) != 3:
        print 'Usage: python ./post_process.py final_rs.txt final.txt'
    else:
        post_process(sys.argv[1], sys.argv[2])

if __name__ == '__main__':
    main()
