@codigo_HU
@allure.label.epic:Hakatools
Feature: formulario basico
  Validar funcionalidad de formularios en hakatools

  @critical
  @allure.label.owner:JohnDoe
  @allure.link:https://dev.example.com/
  @allure.issue:UI-123
  @allure.tms:TMS-456
  @test
  @allure.label.story:Story124
  Scenario: Crear caso Banco tipo solicitud
  Ejemplo de descripcion de escenario
     Given ingreso a hakatools

  @blocker
  @allure.label.owner:William_Navarrete
  @allure.link:https://www.hakalab.com/
  @allure.issue:UI-123
  #@allure.tms:TMS-456
  @allure.label.story:HU-1
  @hakatools @formulario_basico1
  Scenario Outline: Valido formulario basico en hakatools con datos correcto
    Given ingreso a hakatools
    When selecciono la lista "Formularios"
    And ingreso nombre de usuario <usuario>
    And ingreso correo <correo>
    And ingreso direccion <direccion>
    And ingreso direccion permanente <direccion_permanente>
    And selecciono opcion enviar
    Then valido resultados de formulario <usuario><correo><direccion><direccion_permanente>

  @test
  Examples: ejecucion combinatoria 1
    | usuario   | correo                | direccion           | direccion_permanente            |
    | "Hakito"  | "hakito@hakalab.com"  | "calle prueba 123"  | "calle permanente prueba 123 "  |

  @HU-2
  Examples: ejecucion combinatoria 2
    | usuario   | correo                | direccion           | direccion_permanente            |
    | "Hakito"  | "hakito@hakalab.com"  | "calle prueba 123"  | "calle permanente prueba 123 "  |

  @HU-3
  Examples: ejecucion combinatoria 3
    | usuario   | correo                | direccion           | direccion_permanente            |
    | "Hakito"  | "hakito@hakalab.com"  | "calle prueba 123"  | "calle permanente prueba 123 "  |



