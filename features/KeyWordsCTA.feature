@whatsapp @keywordsCTA
Feature: Validar respuesta CTA del chatbot con diferentes palabras clave

  Background:
    Given ingreso a WhatsApp y abro el chat "Abastible SIT"
    When envío el mensaje "reset" para resetear el bot

  @validar_keywords
  Scenario Outline: Enviar palabra clave al bot y validar respuesta CTA
    When envío la palabra clave CTA "<KeyWordsCTA>"
    Then valido la respuesta que entrega el chat bot

  Examples:
    | KeyWordsCTA                |
    | sos                        |
    | sale gas                   |  
    | olor a gas                 |
    | fuga                       |