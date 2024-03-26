import os
import pathlib
import sqlite3
from dotenv import load_dotenv
from helper.plugins import PluginSpec

def get_connection(self):
    """
    get conection of DB SQLite3
    :return _conn: the Connection object
    :return _cur: the Cursor object
    """
    try:
        if self._conn is None:
            self._conn = sqlite3.connect(self._db_file)
            self._cur = self._conn.cursor()
            print(">> INICIO CONEXION A LA BD SQLITE")
            return self._conn
        else:
            return self._conn
    except Exception as e:
        print(">> ERROR AL CONECTAR CON LA BD : ", e)


def close_connection(self):
    """
   close instance conection of DB SQLite3
   """
    try:
        if self._conn is not None:
            self._conn.close()
            print(">> CIERRO CONEXION A LA BD SQLITE")
            self._conn = None
    except Exception as e:
        print("ERROR AL CERRAR CONEXION CON LA DB: ", e)


def insert_data(self, tabla, datos):
    """
    get query data for multiple object for validation exist object,
    if object not found insert object in BD SQLite3
    :param tabla: Name table for manipulation
    :param datos: list[key:value] for insert query
    :return object query: Object found for select or insert
    """
    try:
        self._cur.execute("SELECT * FROM "+tabla+" WHERE nombre = ?", (datos['nombre'],))
        data = self._cur.fetchone()
        if data is not None:
            print(">> Ya existe un registro en la tabla "+tabla+" con la descripción proporcionada.", datos['nombre'])
            return data
        else:
            print(">> NO existe un registro en la tabla "+tabla+" con la descripción proporcionada.", datos['nombre'])
            columnas = ', '.join(datos.keys())
            valores = ', '.join('?' * len(datos))
            query_insert = f"INSERT INTO "+tabla+f" ({columnas}) VALUES ({valores})"
            print(query_insert)
            self._cur.execute(query_insert, tuple(datos.values()))
            print(">> Nuevo registro insertado correctamente.")
            self._conn.commit()
            return self._cur.execute("SELECT * FROM "+tabla+" WHERE nombre = ?", (datos['nombre'],))
    except Exception as e:
        print(">> ERROR EN LA QUERY ", e)


class BDPlugin:
    _db_file = str(pathlib.Path().absolute()) + "/helper/database/haka_auto.db"
    _conn = None
    _cur = None

    @PluginSpec.hookimpl
    def before_all(self, context):
        load_dotenv(dotenv_path='.env')
        if os.getenv('SAVE_DATA_DB') == 'true':
            get_connection(self)

    @PluginSpec.hookimpl
    def before_feature(self, context, feature):
        if os.getenv('SAVE_DATA_DB') == 'true':
            str_description_feature = ' '.join(map(str, feature.description))
            datos_feature = {'nombre': feature.name, 'descripcion': str_description_feature}
            feature_aux = insert_data(self, "Features", datos_feature)
            for scenario in feature.scenarios:
                datos_scenario = {'nombre': scenario.name, 'id_feature': feature_aux[0]}
                scenario_aux = insert_data(self, "Scenarios", datos_scenario)
                for step in scenario.steps:
                    datos_step = {'nombre': step.name, 'id_scenario': scenario_aux[0]}
                    insert_data(self, "Steps", datos_step)
                    #for row in step_aux:
                    #    print(">> RESULTADO STEPS", row)

    @PluginSpec.hookimpl
    def before_scenario(self, context, scenario):
        """My special little hook that you can customize."""

    @PluginSpec.hookimpl
    def before_step(self, context, step):
        """My special little hook that you can customize."""

    @PluginSpec.hookimpl
    def before_tag(self, context, tag):
        """My special little hook that you can customize."""

    @PluginSpec.hookimpl
    def after_tag(self, context, tag):
        """My special little hook that you can customize."""

    @PluginSpec.hookimpl
    def after_step(self, context, step):
        """My special little hook that you can customize."""

    @PluginSpec.hookimpl
    def after_scenario(self, context, scenario):
        """My special little hook that you can customize."""

    @PluginSpec.hookimpl
    def after_feature(self, context, feature):
        """My special little hook that you can customize."""

    @PluginSpec.hookimpl
    def after_all(self, context):
        close_connection(self)

