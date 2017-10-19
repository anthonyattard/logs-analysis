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
	query = "select articles.title, count(log_slug) as views from articles join log_slug on articles.slug = log_slug.slug group by articles.title order by views desc limit 3;"
	c.execute(query)
	top3 = c.fetchall()
	db.close()

	for item in top3:
		print("{0} - {1} views".format(item[0], item[1]))



# 2. Who are the most popular article authors of all time? That is, when you sum up all of the articles each author has written, which authors get the most page views? Present this as a sorted list with the most popular author at the top.
	# Example:
	# Ursula La Multa - 2304 views
	# Rudolf von Treppenwitz - 1985 views
	# Markoff Chaney - 1723 views
	# Anonymous Contributor - 1023 views



# 3. On which days did more than 1% of requests lead to errors? The log table includes a column status that indicates the HTTP status code that the news site sent to the user's browser.
	# Example:
	# July 29, 2016 - 2.5% errors



# Function calls section
top3ArticlesAllTime()



