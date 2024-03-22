@Regresion
@allure.label.epic:formulario_basico
Feature: historia hu-3
  Validar funcionalidad de formularios en hakatools

  @allure.label.story:Story3
  @hakatools @formulario_basico3
  Scenario Outline: Valido formulario basico en hakatools 2
    Given ingreso a hakatools
    When selecciono la lista "Formularios"
    And ingreso nombre de usuario <usuario>
    And ingreso correo <correo>
    And ingreso direccion <direccion>
    And ingreso direccion permanente <direccion_permanente>
    And selecciono opcion enviar
    Then valido resultados de formulario <usuario><correo><direccion><direccion_permanente>
  @HU-21
  Examples: ejecucion combinatoria 21
    | usuario   | correo                | direccion           | direccion_permanente            |
    | "Hakito"  | "hakito@hakalab.com"  | "calle prueba 123"  | "calle permanente prueba 123 "  |

  @HU-22
  Examples: ejecucion combinatoria 22
    | usuario   | correo                | direccion           | direccion_permanente            |
    | "Hakito"  | "hakito@hakalab.com"  | "calle prueba 123"  | "calle permanente prueba 123 "  |

  @HU-23
  Examples: ejecucion combinatoria 23
    | usuario   | correo                | direccion           | direccion_permanente            |
    | "Hakito"  | "hakito@hakalab.com"  | "calle prueba 123"  | "calle permanente prueba 123 "  |

