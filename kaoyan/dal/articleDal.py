#coding=utf-8
import pymysql as pymysql
import re
import time
conn = pymysql.connect(host='192.168.30.128', port=3306, user='root', passwd='root',db='caiji',charset='utf8',cursorclass = pymysql.cursors.DictCursor)
cur  = conn.cursor()

def insertArticle( row ):

    createdTime =time.strftime('%Y-%m-%d %H:%M:%S')
    title   = pymysql.escape_string(row['title'])
    tag     = pymysql.escape_string( row['tag'])
    content = pymysql.escape_string( row['content'])
    url     = pymysql.escape_string( row['url'])
    source_id  = row['source_id']
    contentType = row['contentType'] if row['contentType'] else 'article'
    sql = "insert into items(title,createdTime,tag,content,url,source_id,contentType)  " \
          "values('%s','%s','%s','%s','%s','%s','%s')"%\
          (title,createdTime,tag,content,url,source_id,contentType)
    #print(sql)
    try:
        cur.execute(sql)
    except Exception:
        print('mysql 插入数据异常')
        return None;

#conn.close()