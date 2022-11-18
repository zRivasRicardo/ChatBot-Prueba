# Proyecto <name_project>

_Arquetipo BDD y ATDD en lenguaje Python para automatización de pruebas funcionales_
_____________________________________________________________________________

Este repositorio fue desarrollado con el objetivo de abarcar las pruebas de calidad a proyectos de software de forma automátizada
abarcando la ejecución de pruebas funcionales web por medio de Selenium

__________________________________________________________________

### Pre-requisitos
1.- Solicitar a un mantenedor del repositorio bddpython que te agregue como usuario 'develop'

2.- Clonar rama master del repositorio

3.- Descomprimir archivo de 'helper/vendor/allure-2.13.6.7z' (o descargar desde sitio oficial de allure framework)

4.- Confirmar versión correcta webdriver en 'helper/selenium_class/web_driver' dependiendo del browser a ejecutar. O levantar servidor de Selenium Grid e indicar ip en variable de entorno "SELENIUM_HUB_IP".

5.- Instalar Python

6.- Ejecutar instalación de librerías que requiere el arquetipo con comando 'pip install -r requirements.txt'

7.- Configurar archivo .env que contiene las variables de entorno de la ejecución

```
########### EXECUTION SELENIUM VARIABLES ###########
EXECUTION_TYPE=hub
SELENIUM_HUB_IP = selenium__standalone-chrome
WIDTH_RESOLUTION=1300
HEIGHT_RESOLUTION=900
BROWSER=chrome
RELOADBROWSER=false
########### ALLURE VARIABLES ###########
EXECUTE_ALLURE=true
SAVE_REPORT_ALLURE=true
CLEAN_EXTRAS_REPORT_ALLURE=true
EXECUTION_PARALLEL=false
########### SAUCELABS VARIABLES ###########
USER_SAUCELAB=
TOKEN_SAUCELAB=
HOST_SAUCELAB=
BROWSER_VERSION_SELENIUM=
PLATFORM_NAME_SELENIUM=
####### Re-run variables ############
EXECUTE_RERUN=false
COUNT=0
REPEAT=2
FAILED_SCENARIO_ARRAY=[]

```
- _EXECUTION_TYPE = [localhost, hub, saucelabs]_
  - localhost: Si quieres ejecutar selenium con los webdriver debes seleccionar localhost. Debes guardar los webdriver en 'helper/selenium_class/webdriver/' para abrir el navegador en tu local.
  - hub: Si quieres ejecutar tus pruebas en un hub remoto ya sea selenium grid(especificar ip)o un pipeline (especificar imagen : selenium__standalone-chrome).
  - saucelabs: 

- _BROWSER = [chrome, firefox, opera, edge, safari]_
  - chrome-safari: Indica el tipo de browser que se quiere ejecutar la prueba de Selenium.


- _RELOADBROWSER = [true, false]_

   Activa o desactiva la opcion de reiniciar el navegador al terminar cada esenario o ejecutar todos los escenarios en el mismo navegador


- WIDTH_RESOLUTION:

  Indica la resolución de pantalla que se requiere ejecutar. Solo necesario para ejecución remota.


- HEIGHT_RESOLUTION:

  Indica la resolución de pantalla que se requiere ejecutar. Solo necesario para ejecución remota.


- SAUCELAB:

  Si se define USER_SAUCELAB_SELENIUM y TOKEN_SAUCELAB_SELENIUM, también es necesario definir BROWSER_VERSION_SELENIUM, PLATFORM_NAME_SELENIUM.

  Usar la siguiente página para obtener estos valores por cada dispositivo: https://wiki.saucelabs.com/display/DOCS/Platform+Configurator?src=sidebar#/

```
########### EXECUTION APPIUM VARIABLES ###########

EXECUTION_APPIUM_IP=localhost
BROWSER=chrome
USER_SAUCELAB_APPIUM=user_saucelab
TOKEN_SAUCELAB_APPIUM=token_saucelab
DEVICE_NAME_APPIUM=
VERSION_APPIUM=
PLATFORM_NAME_APPIUM=
PLATFORM_VERSION_APPIUM=
```

- EXECUTION_APPIUM_IP = [localhost, ip]_
  - localhost: Si quieres ejecutar Appium en tu local. Debes tener un dispositivo mobile o un emulador del dispositivo en la cual se quiere hacer la prueba.
  - ip: Ip en la que se levanto un servidor remoto para la ejecución de Appium


- BROWSER = [chrome, ]_
  - chrome: Indica el tipo de browser que se quiere ejecutar la prueba de Appium. El capabilities browserName is define with this variable


- SAUCELAB:

  Si se define USER_SAUCELAB_APPIUM y TOKEN_SAUCELAB_APPIUM, también es necesario definir DEVICE_NAME_APPIUM, VERSION_APPIUM, PLATFORM_NAME_APPIUM, PLATFORM_VERSION_APPIUM.

  Usar la siguiente página para obtener estos valores por cada dispositivo: https://wiki.saucelabs.com/display/DOCS/Platform+Configurator?src=sidebar#/

```

########### ALLURE VARIABLES ############

EXECUTE_ALLURE=true
SAVE_REPORT_ALLURE=true
```
- EXECUTE_ALLURE = [true, false]

  Activa o desactiva la opcion de generar reportes en Allure


- SAVE_REPORT_ALLURE = [true, false]

  Activa o desactiva guardar información de reportes pasados en Allure

```
########### Grafana variables ################

SAVE_GRAFANA=true
GRAFANA_DATABASE_HOST=192.168.99.100
GRAFANA_DATABASE_USER=root
GRAFANA_DATABASE_PASSWORD_USER=myRootPassword123
GRAFANA_DATABASE_NAME=myDb

ID_TEST_CYCLE=4
CELL_KEY_JIRA=IS
UPDATE_JIRA=true
SERVER_JIRA=https://server.atlassian.net
USER_EMAIL_JIRA=email_jira
TOKEN_JIRA=token_generado_en_jira
```

- SAVE_GRAFANA = [true, false]

  Activa o desactiva guardado de información de la ejecución en Grafana

- GRAFANA_DATABASE:

  Variables de configuración para host, usuarios, password y db

- ID_TEST_CYCLE:

  Define id de la db para Grafana

- UPDATE_JIRA = [true, false]

  Define si se actualizarán las issues en cada ejecución

- Jira:

  Variables configure api Jira

```
########### Sonar variables ################

ANALIZE_SONAR=false
SONAR_HOST=ip
```
- ANALIZE_SONAR = [true, false]

  Activa o desactiva el analisis de código estático con Sonarqube

- SONAR_HOST = [ip, ]

  Agrega IP para levantar Sonarqube

```
########### Re - run variables  ###########


EXECUTE_RERUN=true
COUNT=0
REPEAT=2
FAILED_SCENARIO_ARRAY=[]
TOTAL_SCENARIOS=[]
FLAG_BREAK=true
```
-  EXECUTE_RERUN = [true, false]

   Activa o desactiva los reintentos de los pasos que fallaron

-  COUNT = 0 

   Contador de reintentos hasta llegar a la cantidad de repeticiones (valor inicial : 0)

-  REPEAT :

   Cantidad de veces que hará el reintento de los pasos que fallaron (valor entero)

-  FAILED_SCENARIO_ARRAY = []

   Array de string de tags de los escenarios que contienen los pasos que fallaron (ej ["@escenario1", "@escenario2", ...]) 


   
## Pasos y definiciones para ejecución de extensiones 
__________________________________________________________

### Re-Run 

#### Variables globales usadas
- scenarios en el archivo environment.py, es usada para guardar los escenarios fallidos y luego sincronizarlo con el de la variable de entorno (FAILED_SCENARIO_ARRAY)
#### Definición 
- Esta extensión se ejecuta a nivel de entorno, su programación está escrita en el archivo environment.py haciendo uso de los metodos after_feature y after_all
  no requiere intervención de código, ya que se ejecuta al momento de realizar las pruebas por detrás.
- En after_feature es donde se almacenarán los escenarios que fallaron en la prueba
- En after_all es donde ejecutará n veces los escenarios que fallaron captados en after_feature haciendo uso de:

  - Un contador para contabilizar las ejecuciones 
  - Un comando en formato string con los tags de los escenarios fallidos por la ejecucion anterior




## Pipeline
__________________________________________________________
Para ejecutar el arquetipo en un Pipeline, se debe:

- Configurar stage en archivo gitlab-ci.yml
- Definir las variables de entorno en la plataforma de gitlab (deben ser las mismas que se usan en el archivo .env para el stage de pruebas funcionales + variables de entorno necesarias para otros stages)

## Comandos para ejecución de pruebas ⚙️
_______________________________________________________________________________________
Existe tres ejemplos de ejecuciones

- Ejecuta regresión de todas las pruebas
```
behave features -------> _No genera reporte_

behave -f allure_behave.formatter:AllureFormatter -o reporte ./features ------> _Genera reporte_
```

- Ejecuta feature en específico
```
behave features/name.feature -------> No genera reporte

behave -f allure_behave.formatter:AllureFormatter -o reporte features/name.feature ---> Genera reporte
```
- Ejecuta un tag específico para ayudar al proceso de construcción de una prueba o escenario

```
behave -t'@tag_especifico_a_ejecutar' -------> No genera reporte
behave --tags=tag_especifico_a_ejecutar1,tag_especifico_a_ejecutar2 -------> No genera reporte
```

### _Ejecución de pruebas paralelas_

Al comenzar cada escenario se debe definir con @tag que tipo de ejecución que va a correr la prueba, debido a que para cada feature abarcamos todas las posibilidades de comportamiento para una funcionalidad tanto en web como en mobile. </p>

- Web:
    @Selenium

- Mobile:
    @Appium

- Desktop:
    @artificial_vision
```
@sprint1
Feature: Is4
  Test_example1

    @selenium
    Scenario: test example for web
      Given
      When
      Then

    @appium
    Scenario: test example for mobile
      Given
      When
      Then

    @artificial_vision
    Scenario: test example for artificial_vision
      Given
      When
      Then

```

El siguiente comando genera diferentes instancias para ejecutar todos los escenarios tageados previamente en  las categoria "@selenium", "@appium" y "@artificial_vision" de manera paralela uno del otro lo cual facilita el proceso de regresion y ahorra tiempo en la ejecución

```
python executions.py
```
### _Ejecución de pruebas desde un ejecutor_
- Ejecuta tags específicos desde un ejecutor. Al ejecutor se le deben agregar los tags requeridos.
- Para que el reporte conserve los reintentos se debe dejar la variable de entorno SAVE_REPORT_ALLURE=true.
- Para que el reporte no muestre los escenarios no requeridos, se debe quitar el comentario a la variable show_skipped=False en el archivo behave.ini en el directorio raíz

```
python executions/unit_test_execution.py -------> Genera reporte
```

## Levantar servidores con docker
__________________________________________________________
### Requerimientos
- Windows:
  - Descargar docker toolbox (v18.03.0-ce versión sugerida):
  ```
  https://github.com/docker/toolbox/releases
  ```
  - Iniciar docker toolbox
- Ubuntu:
  - Instalar docker:
  ```
  sudo apt install docker.io
  ```
  - Iniciar docker:
  ```
  sudo systemctl start docker
  ```
  - Habilitar docker:
  ```
  sudo systemctl enable docker
  ```
  - Indicar usuario para usar docker:
  ```
  sudo usermod -aG docker <nombre_entregado_whoami>
  ```
  - Instalar docker-compose:
  ```
  sudo curl -L "https://github.com/docker/compose/releases/download/1.25.4/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
  ```
  - Dar privilegios a docker-compose:
  ```
  sudo chmod +x /usr/local/bin/docker-compose
  ```

### Comandos utiles docker
Para desplegar las pruebas en los diferentes servidores, ya que en docker podemos levantas los servicios que deseemos con los siguientes comandos:
- Levantar maquina virtual
```
docker-machine start default
```
- Visualizar la dirección IP
```
docker-machine ip
```
- Ver los contenedores abiertos
```
docker ps
```
- Abrir la consola en el navegador
```
IP+:4444
```

### Levantar Selenium Grid Server
- Ir a ruta 'helper/services_docker' y ejecutar el siguiente comando:
```
docker-compose -f selenium_server.yml up -d
```

### Levantar Grafana server
- Ir a ruta 'helper/services_docker' y ejecutar el siguiente comando:
```
docker-compose -f grafana_server.yml up -d
```

### Levantar Sonarqube server
- Ir a ruta 'helper/services_docker' y ejecutar el siguiente comando:
```
docker-compose -f sonarqube_server.yml up -d
```
```
En Ubuntu:
sudo sysctl -w vm.max_map_count=262144

En windows:
docker-machine ssh
sudo sysctl -w vm.max_map_count=262144
```

## _Visualización de reportes_
__________________________________________________________
Al finalizar las ejecuciones los resultados de las pruebas estaran disponibles en la carpeta /report la cual contiene los .html de cada flujo y una carpeta /img con los screenshots correspondientes.

Para la visualización de reportes usamos el siguiente comando

```
.\helper\vendor\allure-2.13.6\bin\allure open report
```

## _Generar documentación_
__________________________________________________________
Para la generar la documentación configurada en las pruebas a traves de la libreria Mkdocs ejecutamos

```
mkdocs build
```


Si queremos levantar un servidor con la documentación de las pruebas localmente en el puerto 8000

```
mkdocs serve
```

## Autores ✒️
__________________________________________________________
Este repositorio es un esfuerzo de **Haka Lab** para que todos
los colaboradores cuenten con un arquetipo base para todas las
actividades de sus servicios dentro de la organización.

El objetivo es estandarizar y generar una forma de trabajo
común entre Servicios y Proyectos.

Por lo que todo este repositorio y su contenido es de uso interno de la organización y está estrictamente prohibido compartir fuera de la misma o para
utilización en proyectos personales.

**Haka Lab**
