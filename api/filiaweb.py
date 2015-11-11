import os
import csv
import psycopg2
from pandas import DataFrame
from io import StringIO

from urllib.parse import urlparse

url = urlparse(os.environ["DATABASE_URL"])

conn = psycopg2.connect(
    database=url.path[1:],
    user=url.username,
    password=url.password,
    host=url.hostname,
    port=url.port
)

def persist_csv_data(file_name, file_text):
    """ Persists into database the
    file_name and file_text from csv files"""

    cur = conn.cursor()

    cur.execute(
        """INSERT INTO rs.filiaweb_csv (file_name, file_text)
        VALUES (%s, %s);""", (file_name, file_text))
    cur.execute(
        """select id from rs.filiaweb_csv
        where file_name = %s order by created_at DESC limit 1""",
        (file_name,))

    id = cur.fetchone()[0]

    conn.commit()
    cur.close()

    return id

def process_csv_data(id, file_text):
    """ Search by emails on csv data on afialiados """

    cur = conn.cursor()
    csv_data = StringIO(file_text)
    data_frame = DataFrame.from_csv(csv_data)
    result = []

    for email in data_frame.Email:
        cur.execute(
            """ select user_id, status, filiaweb
            from rs.afiliados where lower(email) = lower(%s)""",
            (email,))

        user = cur.fetchone()

        if user is None:
            cur.execute(
                """insert into rs.filiaweb_csv_logs
                (filiaweb_csv_id, email, found) VALUES
                (%s,%s,%s)""",(id, email, False))
            result.append({'email': email, 'found': False})
        else:
            cur.execute(
                """update rs.afiliados
                set status=3,
                set filiaweb=true
                where user_id = %s""", (user[0]))
            cur.execute(
                """insert into rs.filiaweb_csv_logs
                (filiaweb_csv_id, email, found) VALUES
                (%s,%s,%s)""",(id, email, True))
            result.append({'email': email, 'found': True})

    conn.commit()
    cur.close()

    return result


