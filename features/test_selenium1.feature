@Regresion
Feature: historia hu-2
  Validar funcionalidad de formularios en hakatools

  @hakatools @formulario_basico
  Scenario Outline: Valido formulario basico en hakatools 1
    Given ingreso a hakatools
    When selecciono la lista "Formularios"
    And ingreso nombre de usuario <usuario>
    And ingreso correo <correo>
    And ingreso direccion <direccion>
    And ingreso direccion permanente <direccion_permanente>
    And selecciono opcion enviar
    Then valido resultados de formulario <usuario><correo><direccion><direccion_permanente>
  @HU-11
  Examples: ejecucion combinatoria 11
    | usuario   | correo                | direccion           | direccion_permanente            |
    | "Hakito"  | "hakito@hakalab.com"  | "calle prueba 123"  | "calle permanente prueba 123 "  |

  @HU-12
  Examples: ejecucion combinatoria 12
    | usuario   | correo                | direccion           | direccion_permanente            |
    | "Hakito"  | "hakito@hakalab.com"  | "calle prueba 123"  | "calle permanente prueba 123 "  |

  @HU-13
  Examples: ejecucion combinatoria 13
    | usuario   | correo                | direccion           | direccion_permanente            |
    | "Hakito"  | "hakito@hakalab.com"  | "calle prueba 123"  | "calle permanente prueba 123 "  |

