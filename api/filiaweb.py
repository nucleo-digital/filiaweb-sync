import os
import psycopg2
from pandas import isnull
from io import StringIO
import pandas

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
        where file_name = %s order by created_at DESC limit 1;""",
        (file_name,))

    id = cur.fetchone()[0]

    conn.commit()
    cur.close()

    return id


def process_csv_data(id, file_text):
    """ Search by emails on csv data on afialiados """

    cur = conn.cursor()
    csv_data = StringIO(file_text)
    data_frame = pandas.read_csv(csv_data)
    result = []

    for index, item in data_frame[['Nome', 'Email']].iterrows():
        name = item.Nome
        email = item.Email

        print("checking for email or name --> {}".format(
            name if email is None else email))

        if isnull(email):
            cur.execute(
                """ select user_id, status, filiaweb
                from rs.afiliados where
                lower(unaccent(nome)) ~* lower(unaccent(%s))""",
                (name))
        else:
            cur.execute(
                """ select user_id, status, filiaweb
                from rs.afiliados where lower(email) = lower(%s)
                or lower(unaccent(nome)) ~* lower(unaccent(%s))""",
                (email, name))

        user = cur.fetchone()

        if user is None:
            cur.execute(
                """insert into rs.filiaweb_csv_logs
                (filiaweb_csv_id, name, email, found) VALUES
                (%s,%s,%s,%s);""", (id, name, email, False))
            result.append({'email': email, 'name': name, 'found': False})
        else:
            cur.execute(
                """update rs.afiliados
                set status = '3', filiaweb = true
                where user_id = %s::integer;""", (user[0],))
            cur.execute(
                """insert into rs.filiaweb_csv_logs
                (filiaweb_csv_id, name, email, found) VALUES
                (%s,%s,%s,%s);""", (id, name, email, True))
            result.append({'email': email, 'name': name, 'found': True})

    conn.commit()
    cur.close()

    return result
