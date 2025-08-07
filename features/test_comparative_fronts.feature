Feature: POC comparativa entre fronts

  @front-vs-front
  Scenario: Valido que la pagina de formularios no tenga cambios
    Given ingreso a hakatools
    When selecciono la lista "Formularios"
    Then valido que la vista "Hakalab/Formularios" no haya sufrido cambios