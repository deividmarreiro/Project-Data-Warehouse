import configparser
import psycopg2
from sql_queries import create_table_queries, drop_table_queries


def drop_tables(cur, conn):
    """
    Executes SQL queries to drop tables in Redshift cluster.

    Args:
    - cur: psycopg2 cursor object
    - conn: psycopg2 connection object

    Returns: None
    """
    for query in drop_table_queries:
        cur.execute(query)
        conn.commit()


def create_tables(cur, conn):
    """
    Executes SQL queries to create tables in Redshift cluster.

    Args:
    - cur: psycopg2 cursor object
    - conn: psycopg2 connection object

    Returns: None
    """
    for query in create_table_queries:
        cur.execute(query)
        conn.commit()


def main():
    """
    Connects to Redshift cluster, drops tables and creates new tables based on SQL queries.

    Args: None

    Returns: None
    """
    config = configparser.ConfigParser()
    config.read('dwh.cfg')

    conn = psycopg2.connect("host={} dbname={} user={} password={} port={}".format(*config['DB'].values()))
    cur = conn.cursor()

    drop_tables(cur, conn)
    create_tables(cur, conn)

    conn.close()


if __name__ == "__main__":
    main()