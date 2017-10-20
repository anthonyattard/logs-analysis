#!/usr/bin/env python
# 
# logs-analysis.py -- analyze user logs from news database
#

import psycopg2


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=news")


# 1. What are the most popular three articles of all time? Which articles have been accessed the most? Present this information as a sorted list with the most popular article at the top.
	# Example:
	# "Princess Shellfish Marries Prince Handsome" - 1201 views
	# "Baltimore Ravens Defeat Rhode Island Shoggoths" - 915 views
	# "Political Scandal Ends In Political Scandal" - 553 views
def top3ArticlesAllTime():
	db = connect()
	c = db.cursor()
	query = "select * from articles_views limit 3;"
	c.execute(query)
	top3 = c.fetchall()
	db.close()

	for item in top3:
		print("{0} - {1} views".format(item[0], item[2]))



# 2. Who are the most popular article authors of all time? That is, when you sum up all of the articles each author has written, which authors get the most page views? Present this as a sorted list with the most popular author at the top.
	# Example:
	# Ursula La Multa - 2304 views
	# Rudolf von Treppenwitz - 1985 views
	# Markoff Chaney - 1723 views
	# Anonymous Contributor - 1023 views
def mostPopularAuthors():
	db = connect()
	c = db.cursor()
	query = "select authors.name, sum(articles_views.views) as total_author_views from authors join articles_views on authors.id = articles_views.author group by authors.name order by total_author_views desc"
	c.execute(query)
	authors = c.fetchall()
	db.close()

	for item in authors:
		print("{0} - {1} views".format(item[0], item[1]))



# 3. On which days did more than 1% of requests lead to errors? The log table includes a column status that indicates the HTTP status code that the news site sent to the user's browser.
	# Example:
	# July 29, 2016 - 2.5% errors
def highErrorDays():
	db = connect()
	c = db.cursor()
	query = "select to_char(log_date, 'FMMonth DD, YYYY') as log_date_fmt, percent_errors from log_date_percent_errors where percent_errors > 1.00"
	c.execute(query)
	days = c.fetchall()
	db.close()

	for item in days:
		print("{0} - {1}% errors".format(item[0], item[1]))



# Function calls section
top3ArticlesAllTime()
mostPopularAuthors()
highErrorDays()



