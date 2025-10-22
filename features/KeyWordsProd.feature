@whatsapp @keywords
Feature: Validar respuestas del chatbot con diferentes palabras clave

  Background:
    Given ingreso a WhatsApp Web y abro el chat con "Abastible"
    When envío el mensaje "reset" para reiniciar el bot

  @validar_keywords
  Scenario Outline: Enviar palabra clave al bot y validar su respuesta
    When envío la palabra clave "<KeyWords>"
    Then valido la respuesta del chat bot

  Examples:
    | KeyWords                  |
    | hola                      |
    | ola                       |
    | ola k tal                 |
    | holi                      |
    | buenas                    |
    | wenas                     |
    | wenass                    |
    | quiero gas                |
    | kiero gas                 |
    | necesito gas              |
    | pedir gas                 |
    | pedir gaz                 |
    | comprar gas               |
    | pedir gaz con descuento   |
    | gaz                       |
    | gas                       |
    | pedir                     |
    | pedi gas                  |
    | pedi un cilindro          |
    | quiero pedir              |
    | necesito pedir            |
    | descuento                 |
    | descunto                  |
    | deskuento                 |
    | mi descuento              |
    | mi desc                   |
    | quiero mi descuento       |
    | tengo descuento           |
    | descuento wsp             |
    | cupón                     |
    | kupon                     |
    | promocion                 |
    | promo                     |
    | promocion gas             |
    | precios                   |
    | precio                    |
    | presio                    |
    | precio gas                |
    | cuanto vale el gas        |
    | cuanto cuesta el gas      |
    | precio gas hoy            |
    | precio en mi comuna       |
    | precio por formato        |
    | cuanto esta el gas        |
    | kiero saber el precio     |
    | qr                        |
    | descargar qr              |
    | cupon                     |
  