import configparser


# CONFIG
config = configparser.ConfigParser()
config.read('dwh.cfg')

# DROP TABLES

staging_events_table_drop = "DROP TABLE IF EXISTS stage_events"
staging_songs_table_drop = "DROP TABLE IF EXISTS stage_songs"
songplay_table_drop = "DROP TABLE IF EXISTS fact_songplay"
user_table_drop = "DROP TABLE IF EXISTS dim_user"
song_table_drop = "DROP TABLE IF EXISTS dim_song"
artist_table_drop = "DROP TABLE IF EXISTS dim_artist"
time_table_drop = "DROP TABLE IF EXISTS dim_time"

# CREATE TABLES

staging_events_table_create= ("""
    CREATE TABLE IF NOT EXISTS stage_events (
        artist TEXT,
        auth TEXT,
        firstName TEXT,
        gender TEXT,
        itemInSession INTEGER,
        lastName TEXT,
        length FLOAT,
        level TEXT,
        location TEXT,
        method TEXT,
        page TEXT,
        registration FLOAT,
        sessionId INTEGER,
        song TEXT,
        status INTEGER,
        ts BIGINT,
        userAgent TEXT,
        user_id TEXT
    )
""")

staging_songs_table_create = ("""
    CREATE TABLE IF NOT EXISTS stage_songs
    (
        song_id VARCHAR(512),
        title VARCHAR(512),
        duration DOUBLE PRECISION,
        year SMALLINT,
        artist_id VARCHAR(512),
        artist_name VARCHAR(512),
        artist_latitude DOUBLE PRECISION,
        artist_longitude DOUBLE PRECISION,
        artist_location VARCHAR(512),
        num_songs INTEGER
    );
""")

songplay_table_create = ("""
    CREATE TABLE IF NOT EXISTS fact_songplay (
        songplay_id INTEGER IDENTITY(0, 1),
        start_time TIMESTAMP,
        user_id TEXT,
        level TEXT,
        song_id VARCHAR(512),
        artist_id VARCHAR(512),
        session_id INTEGER,
        location TEXT,
        user_agent TEXT,
        PRIMARY KEY (songplay_id)
    )
""")

user_table_create = ("""
    CREATE TABLE IF NOT EXISTS dim_user (
        user_id TEXT,
        first_name TEXT,
        last_name TEXT,
        gender TEXT,
        level TEXT,
        PRIMARY KEY(user_id)
    )
""")

song_table_create = ("""
    CREATE TABLE IF NOT EXISTS dim_song (
        song_id VARCHAR(512),
        title VARCHAR(512)
        artist_id VARCHAR(512),
        year SMALLINT,
        duration DOUBLE PRECISION,
        PRIMARY KEY(song_id)
    )
""")

artist_table_create = ("""
    CREATE TABLE IF NOT EXISTS dim_artist (
        artist_id VARCHAR(512),
        name VARCHAR(512),
        location TEXT,
        latitude DOUBLE PRECISION,
        longitude DOUBLE PRECISION,
        PRIMARY KEY(artist_id)
    )
""")

time_table_create = ("""
    CREATE TABLE IF NOT EXISTS dim_time (
        start_time TIMESTAMP,
        hour INTEGER,
        day INTEGER,
        week INTEGER,
        month INTEGER,
        year INTEGER,
        weekday INTEGER,
        PRIMARY KEY(start_time)
    )
""")

# STAGING TABLES

staging_events_copy = ("""
                       COPY {} FROM {}
                       CREDENTIALS 'aws_iam_role={}'
                       JSON {} REGION '{}'
""").format(
    'stage_events', 
    config.get("S3", "LOG_DATA"),
    config.get("IAM_ROLE", "ARN"),
    config.get("S3", "LOG_JSONPATH"), 
    config.get("AWS", "REGION_NAME_S3"))

staging_songs_copy = ("""
                      COPY {} FROM {}
                      CREDENTIALS 'aws_iam_role={}'
                      JSON 'auto' REGION '{}'
""").format(
    'stage_songs', 
    config.get("S3", "SONG_DATA"), 
    config.get("IAM_ROLE", "ARN"), 
    config.get("AWS", "REGION_NAME_S3")
)

# FINAL TABLES

songplay_table_insert = ("""
    INSERT INTO fact_songplay (start_time, user_id, level, song_id, artist_id, session_id, location, user_agent)
    SELECT timestamp 'epoch' + ts/1000 * interval '1 second' AS start_time,
        user_id,
        level,
        ss.song_id,
        ss.artist_id,
        sessionId AS session_id,
        se.location,
        userAgent AS user_agent
    FROM stage_events se
    JOIN stage_songs ss ON se.song = ss.title AND se.artist = ss.artist_name
    WHERE se.page = 'NextSong'
""")

user_table_insert = ("""
    INSERT INTO dim_user (user_id, first_name, last_name, gender, level)
    SELECT
        user_id,
        firstname as first_name,
        lastname as last_name,
        gender,
        level
    FROM stage_events
    where page = 'NextSong'
""")

song_table_insert = ("""
    INSERT INTO dim_song (song_id, title, artist_id, year, duration)
    SELECT
        song_id,
        title,
        artist_id,
        year,
        duration
    FROM stage_songs
""")

artist_table_insert = ("""
    INSERT INTO dim_artist (artist_id, name, location, latitude, longitude)
    SELECT
        artist_id,
        artist_name as name,
        artist_location as location,
        artist_latitude as latitude,
        artist_longitude as longitude
    FROM stage_songs
    WHERE artist_id IS NOT NULL
""")

time_table_insert = ("""
    INSERT INTO dim_time (start_time, hour, day, week, month, year, weekDay)
    SELECT start_time, 
        extract(hour from start_time),
        extract(day from start_time),
        extract(week from start_time), 
        extract(month from start_time),
        extract(year from start_time), 
        extract(dayofweek from start_time)
    FROM fact_songplay
""")

# QUERY LISTS

create_table_queries = [staging_events_table_create, staging_songs_table_create, songplay_table_create, user_table_create, song_table_create, artist_table_create, time_table_create]
drop_table_queries = [staging_events_table_drop, staging_songs_table_drop, songplay_table_drop, user_table_drop, song_table_drop, artist_table_drop, time_table_drop]
copy_table_queries = [staging_events_copy, staging_songs_copy]
insert_table_queries = [songplay_table_insert, user_table_insert, song_table_insert, artist_table_insert, time_table_insert]
