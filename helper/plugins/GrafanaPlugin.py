import os
import time
from datetime import datetime
from behave.model_core import Status
from helper.plugins import PluginSpec
from helper.services_class.connection_mysql import ConnectionMysql
from dotenv import load_dotenv

global conn
def conectar_Server_Grafana(context):
    """
    Realiza la conexion a la base de datos de grafana
    :param context:
    :return:
    """
    try:
        context.conn = ConnectionMysql(database_host=os.getenv("GRAFANA_DATABASE_HOST"),
                                       user=os.getenv("GRAFANA_DATABASE_USER"),
                                       password=os.getenv("GRAFANA_DATABASE_PASSWORD_USER"))
        context.conn.use_data_base(os.getenv("GRAFANA_DATABASE_NAME"))
        query = "SET SQL_SAFE_UPDATES = 0;"
        context.conn.execute_query2(query)
    except Exception as e:
        print("Error al conectar con la BD de grafana: ", e)


def crear_Ejecucion_Grafana(context):
    """Crea una nueva ejecución en grafana.
        Toma el tiempo de inicio, el tiempo de ejecucion y la ID de la celula
        Si no existe registro de la celula, toma el nombre y lo asocial al nombre del proyecto que viene desde las
        variables de entorno
    """
    try:
        global time_start_execution
        global datetime_execution
        global id_cell

        try:
            count_celula_by_name = "select COUNT(id_celula) from celula where nombre_celula = '" + os.getenv('CELULA') + "' and nombre_proyecto = '" + os.getenv('PROYECTO') + "';"
            exiteCell = context.conn.execute_query(count_celula_by_name)[0][0]
            get_id_by_name = "select id_celula from celula where nombre_celula = '" + os.getenv('CELULA') + "' and nombre_proyecto = '" + os.getenv('PROYECTO') + "';"
            """si existe la celula actualiza el nombre del automatizar que está ejecutando
                Si no existe lo crea
            """
            if exiteCell != 0:
                id_cell = context.conn.execute_query(get_id_by_name)[0][0]
                update_celula_by_id = "UPDATE celula SET nombre_qa = '" + os.getenv('AUTOMATIZADORQA') + "' WHERE id_celula =  {}  ;".format(str(id_cell))
                context.conn.execute_query(update_celula_by_id)
            else:
                insert_celula = "insert into celula (nombre_celula, nombre_proyecto, nombre_qa) values ('" + os.getenv('CELULA') + "', '" + os.getenv('PROYECTO') + "', '" + os.getenv('AUTOMATIZADORQA') + "')"
                context.conn.execute_query(insert_celula)
                id_cell = context.conn.execute_query(get_id_by_name)[0][0]
        except Exception as msg:
            print("Error al crear o actualizar la informacion de la celula:", msg)

        ##### Crea la nueva ejecucion ######
        datetime_execution = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        insert_executions = "insert into executions (id_celula, browser, start_datetime, producto, flujo, proyect_id ) values (" + str(id_cell) + ", '" + os.getenv('BROWSER') + "', '" + datetime_execution + "', '" + os.getenv('PRODUCTO') + "', '" + os.getenv('FLUJO') + "', {});".format(str(id_cell))
        context.conn.execute_query2(insert_executions)

        #### obtiene el ID de la ejecucion recien creada ####
        select_max_executions = "SELECT MAX(id) FROM executions;"
        id_executionTemp = context.conn.execute_query(select_max_executions)
        print("ID TEMPO=", id_executionTemp)
        context.id_execution = id_executionTemp[0][0]
        context.scenarios_passed = [0]
        context.scenarios_failed = [0]
        time_start_execution = time.time()
    except Exception as e:
        print("Error Al crear la nueva ejecución", e)


def finalizar_Ejecucion_Grafana(context):
    """
        finaliza la ejecucion completa
    :param context:
    :return:
    """
    tiempo_fin = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    update_datetime_execution_by_id = "UPDATE executions SET end_datetime = '" + tiempo_fin + "' WHERE id=" + str(context.id_execution) + ";"
    context.conn.execute_query2(update_datetime_execution_by_id)
    context.conn.close_connection()


def crear_Feature_Grafana(context, feature):
    """
        Almacena los datos de los features ejecutados
    :param context:
    :param feature:
    :return:
    """
    datetime_execution = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    tags = ''
    for t in feature.tags:
        tags = tags + "@" + t + ", "
    insert_features = "insert into features (id_execution, nombre_feature, tags_feature, t_inicio) values (" + str(context.id_execution) + ", '" + feature.name + "', '" + tags + "', '" + datetime_execution + "');"
    context.conn.execute_query2(insert_features)

    select_max_features = "SELECT MAX(idfeatures) FROM features;"
    id_state_issue = context.conn.execute_query(select_max_features)
    context.idFeature = id_state_issue[0][0]


def crear_Escenario_Grafana(context):
    """
        Crear en la bd el escenario que se está ejecutando y obtiene el ID del mismo
    :param context:
    :return:
    """
    if context.grafana:
        global id_escenario_executions
        datetime_scenario = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        insert_escenario = "insert into scenario_executions (id, start_datetime, id_feature, id_execution) values (DEFAULT, '" + datetime_scenario + "', " + str(context.idFeature) + ", " + str(context.id_execution) + ");"
        context.conn.execute_query2(insert_escenario)
        query = "SELECT MAX(id) FROM scenario_executions;"
        id_escenario_executions = context.conn.execute_query(query)
        context.id_escenario_executions = id_escenario_executions[0][0]
        context.steps_passed = [0]
        context.steps_failed = [0]


def actualizar_Escenario_Grafana(context, step):
    if context.grafana:
        tiempo_end = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        estado = 'failed'
        if step.status == Status.passed:
            estado = 'passed'

        update_scenario_executions_by_id = "UPDATE scenario_executions SET scenario_status = '" + estado + "', end_datetime = '" + tiempo_end + "' WHERE id_feature = " + str(
            context.idFeature) + " and id = " + str(id_escenario_executions[0][0]) + ";"
        context.conn.execute_query2(update_scenario_executions_by_id)


def finalizar_Escenario_Grafana(context, scenario):
    """
        Finaliza la ejecucion del escenario y actualiza el estado del mismo y del feature.
        El feature se marca como Failed al existir 1 o más escenarios Failed
    :param context:
    :param scenario:
    :return:
    """
    if context.grafana:
        time_scenario = int(scenario.duration)
        tags = str(scenario.tags).replace("'", "@")

        count_scenario_executions_by_scenario = "SELECT COUNT(id) FROM scenario_executions where scenario_status = 'failed' and id_feature =" + str(context.idFeature) + ";"
        numFails = context.conn.execute_query(count_scenario_executions_by_scenario)
        if numFails[0][0] > 0:
            update_features_by_feature = "UPDATE features SET status = 'failed' where idfeatures =" + str(context.idFeature) + ";"
            context.conn.execute_query(update_features_by_feature)
        else:
            update_features_by_id = "UPDATE features SET status = 'passed', t_fin = '" + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "' where idfeatures =" + str(context.idFeature) + ";"
            context.conn.execute_query(update_features_by_id)

        """Actualiza el estado del escenario"""

        update_scenario_executions = "UPDATE scenario_executions SET type_execution='" + context.type_execution + "', execution_timeEE=" + str(time_scenario) + ", name_scenario='" + scenario.name + "', tags_scenario='" + tags + "' WHERE id=" + str(context.id_escenario_executions) + ";"
        context.conn.execute_query2(update_scenario_executions)
        status = scenario.status
        if status == Status.passed:
            context.scenarios_passed[0] = context.scenarios_passed[0] + 1
        elif status == Status.failed:
            context.scenarios_failed[0] = context.scenarios_failed[0] + 1
        update_executions_by_id = "UPDATE executions SET features_passed=" + str(context.scenarios_passed[0]) + ",  features_failed=" + str(context.scenarios_failed[0]) + " WHERE id=" + str(context.id_execution) + ";"
        context.conn.execute_query2(update_executions_by_id)


class GrafanaPlugin:
    scenarios = []
    id_escenario_steps = 0
    time_start_execution = 0.0
    id_cell = 0
    id_escenario_executions = 0
    id_execution = 0
    type_execution = ''
    global datetime_execution
    global idFeature
    global conn

    def __init__(self):
        self.scenarios_passed = None
        self.datetime_execution = None
        self.idFeature = None

    @PluginSpec.hookimpl
    def before_all(self, context):
        if os.getenv('SAVE_GRAFANA') is None:
            load_dotenv(dotenv_path='.env')
        if os.getenv('SAVE_GRAFANA') == 'true':
            print("*************************ingreso a before_all grafana")
            conectar_Server_Grafana(context)
            crear_Ejecucion_Grafana(context)

    @PluginSpec.hookimpl
    def after_all(self, context):
        if os.getenv('SAVE_GRAFANA') == 'true':
            finalizar_Ejecucion_Grafana(context)

    @PluginSpec.hookimpl
    def before_feature(self, context, feature):
        if os.getenv('SAVE_GRAFANA') == 'true':
            crear_Feature_Grafana(context, feature)

    @PluginSpec.hookimpl
    def after_feature(self, context, feature):
        pass

    @PluginSpec.hookimpl
    def before_scenario(self, context, scenario):
        if os.getenv('SAVE_GRAFANA') == 'true':
            crear_Escenario_Grafana(context)

    @PluginSpec.hookimpl
    def after_scenario(self, context, scenario):
        if os.getenv('SAVE_GRAFANA') == 'true':
            finalizar_Escenario_Grafana(context, scenario)

    @PluginSpec.hookimpl
    def after_step(self,context, step):
        if os.getenv('SAVE_GRAFANA') == 'true':
            actualizar_Escenario_Grafana(context, step)
