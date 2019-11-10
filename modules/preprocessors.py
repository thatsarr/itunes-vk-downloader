import json


def shazam_json_to_artist_song_pair(json_str: str):
    song_dict = json.loads(json_str)
    return "{} - {}".format(song_dict["track"]["subtitle"], song_dict["track"]["title"])


def preprocess_itunes_playlist():
    pass


def preprocess_shazam_database(database_fname):
    import sqlite3
    from sqlite3 import Error
    """ create a database connection to a SQLite database """
    conn = None
    songs_info = None
    try:
        conn = sqlite3.connect(database_fname)
        cur = conn.cursor()
        cur.execute("SELECT json FROM tag where status == \"SUCCESSFUL\"")
        rows = cur.fetchall()
        songs_info = []
        for row in rows:
            if row[0]:
                songs_info.append(shazam_json_to_artist_song_pair(row[0]))
    except Error as e:
        print(e)
    finally:
        if conn:
            conn.close()
    return songs_info
