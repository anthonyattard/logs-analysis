# Logs Analysis
This project reads in data from a large database and derives insights on that data using SQL.

## Instructions

Download the database from [Udacity](https://d17h27t6h515a5.cloudfront.net/topher/2016/August/57b5f748_newsdata/newsdata.zip)

Run the following lines in your database to create the views needed for the code to work.

```sql
create view log_slug as
select log.path, log.ip, log.method, log.status, log.time, log.id, replace(log.path, '/article/', '') as slug from log;
```

```sql
create view articles_views as
select articles.title, articles.author, count(log_slug) as views from articles join log_slug on articles.slug = log_slug.slug group by articles.title, articles.author order by views desc
```

```sql
create view log_date_status as
select log.time::timestamp::date as log_date, log.status from log;
```

```sql
create view log_requests_errors as
select log_date, count(*) as total_requests, count(*) filter (where status like '%404%') as total_errors from log_date_status group by log_date;
```

```sql
create view log_date_percent_errors as
select log_date, round(100.00 * ( cast(total_errors as decimal)/total_requests), 2) as percent_errors from log_requests_errors;
```

Run the program from the project directory with `python logs-analysis.py`

Enjoy!