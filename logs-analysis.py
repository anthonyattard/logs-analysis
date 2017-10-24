#!/usr/bin/env python
#
# logs-analysis.py -- analyze user logs from news database
#

import psycopg2


# Connect to the PostgreSQL database. Returns a database connection.
def connect(database_name):
    try:
        db = psycopg2.connect("dbname={}".format(database_name))
        c = db.cursor()
        return db, c
    except psycopg2.Error as e:
        print "Unable to connect to the database"
        sys.exit(1)


# Returns the most popular 3 articles of all time
def top3ArticlesAllTime():
    db, c = connect('news')
    query = "select * from articles_views " \
            "limit 3;"
    c.execute(query)
    top3 = c.fetchall()
    db.close()

    for item in top3:
        print("{0} - {1} views".format(item[0], item[2]))


# Returns the most popular authors of all time
def mostPopularAuthors():
    db, c = connect('news')
    query = "select authors.name, " \
            "sum(articles_views.views) as total_author_views " \
            "from authors join articles_views " \
            "on authors.id = articles_views.author " \
            "group by authors.name " \
            "order by total_author_views desc"
    c.execute(query)
    authors = c.fetchall()
    db.close()

    for item in authors:
        print("{0} - {1} views".format(item[0], item[1]))


# Returns the days where more than 1% of requests were errors
def highErrorDays():
    db, c = connect('news')
    query = "select to_char(log_date, 'FMMonth DD, YYYY') as log_date_fmt, " \
            "percent_errors from log_date_percent_errors " \
            "where percent_errors > 1.00"
    c.execute(query)
    days = c.fetchall()
    db.close()

    for item in days:
        print("{0} - {1}% errors".format(item[0], item[1]))

# Function calls section
top3ArticlesAllTime()
mostPopularAuthors()
highErrorDays()
