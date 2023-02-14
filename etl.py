import configparser
import psycopg2
from sql_queries import copy_table_queries, insert_table_queries


def load_staging_tables(cur, conn):
    """
    Executes SQL queries to copy data from S3 to Redshift staging tables.

    Args:
    - cur: psycopg2 cursor object
    - conn: psycopg2 connection object

    Returns: None
    """
    for query in copy_table_queries:
        cur.execute(query)
        conn.commit()


def insert_tables(cur, conn):
    """
    Executes SQL queries to insert data from Redshift staging tables to fact and dimension tables.

    Args:
    - cur: psycopg2 cursor object
    - conn: psycopg2 connection object

    Returns: None
    """
    for query in insert_table_queries:
        cur.execute(query)
        conn.commit()


def main():
    """
    Connects to Redshift cluster, loads data into staging tables, and inserts data into fact and dimension tables.

    Args: None

    Returns: None
    """
    config = configparser.ConfigParser()
    config.read('dwh.cfg')
    conn = psycopg2.connect("host={} dbname={} user={} password={} port={}".format(*config['DB'].values()))
    cur = conn.cursor()
    
    load_staging_tables(cur, conn)
    insert_tables(cur, conn)

    conn.close()


if __name__ == "__main__":
    main()