# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


import sqlite3
import operator

class JobscraperPipeline(object):
    def process_item(self, item, spider):
        return item


class SqlitePipeline(object):
    CREATE_TABLE_QUERY = """
    CREATE TABLE IF NOT EXISTS jobs(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT,
    company TEXT,
    zip_code TEXT,
    city TEXT,
    salary TEXT,
    contract TEXT,
    url TEXT UNIQUE,
    publication_date DATE
    )
    """

    INSERT_ROW_QUERY = """
    INSERT INTO jobs(title, company, zip_code, city, salary, contract, url, publication_date)
    VALUES(?, ?, ?, ?, ?, ?, ?, ?)
    """

    # TODO: Use from_crawler
    def __init__(self, dbname='../data/jobs.db'):
        self.dbname = dbname

    def open_spider(self, spider):
        self.conn = sqlite3.connect(self.dbname)
        self._execute_query(SqlitePipeline.CREATE_TABLE_QUERY)

    def close_spider(self, spider):
        self.conn.close()

    def _execute_query(self, query, args=[]):
        cur = self.conn.cursor()
        cur.execute(query, args)
        self.conn.commit()

    def process_item(self, item, spider):
        make_row = operator.itemgetter('title', 'company', 'zip_code', 'city', 'salary', 'contract', 'url', 'publication_date')
        self._execute_query(SqlitePipeline.INSERT_ROW_QUERY, make_row(item))
        return item

        
