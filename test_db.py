import pathlib
import sqlite3

from helper.plugins.DBPlugin import BDPlugin
db_file = str(pathlib.Path().absolute()) + "/helper/database/haka_auto.db"
try:
    _conn = sqlite3.connect(db_file)
    print("_CONN :", _conn)
    cur = _conn.cursor()
    cur.execute("SELECT * FROM Features")
    rows = cur.fetchall()
    print(len(rows))
    for row in rows:
        print(row)
    _conn.close()
except Exception as e:
    print(">> Error al conectar con la BD: ", e)
