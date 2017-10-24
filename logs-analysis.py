#!/usr/bin/env python
#
# logs-analysis.py -- analyze user logs from news database
#

import psycopg2


def connect(database_name):
    """Connect to the PostgreSQL database. Returns a database connection."""
    try:
        db = psycopg2.connect("dbname={}".format(database_name))
        c = db.cursor()
        return db, c
    except psycopg2.Error as e:
        print "Unable to connect to the database"
        sys.exit(1)


def execute_query(query):
    db, c = connect('news')
    c.execute(query)
    results = c.fetchall()
    db.close()
    return results


def top3ArticlesAllTime():
    """Returns the most popular 3 articles of all time."""
    query = "select * from articles_views " \
            "limit 3;"
    top3 = execute_query(query)
    for item in top3:
        print("{0} - {1} views".format(item[0], item[2]))


def mostPopularAuthors():
    """Returns the most popular authors of all time."""
    query = "select authors.name, " \
            "sum(articles_views.views) as total_author_views " \
            "from authors join articles_views " \
            "on authors.id = articles_views.author " \
            "group by authors.name " \
            "order by total_author_views desc"
    authors = execute_query(query)

    for item in authors:
        print("{0} - {1} views".format(item[0], item[1]))


def highErrorDays():
    """Returns the days where more than 1% of requests were errors."""
    query = "select to_char(log_date, 'FMMonth DD, YYYY') as log_date_fmt, " \
            "percent_errors from log_date_percent_errors " \
            "where percent_errors > 1.00"
    days = execute_query(query)

    for item in days:
        print("{0} - {1}% errors".format(item[0], item[1]))

if __name__ == '__main__':
    top3ArticlesAllTime()
    mostPopularAuthors()
    highErrorDays()
