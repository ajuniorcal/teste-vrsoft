import pytest
from unittest.mock import AsyncMock, patch
from app.infra.publisher import publish_message

@pytest.mark.asyncio
@patch("app.infra.publisher.get_rabbitmq_connection")
async def test_publish_message_success(mock_get_connection):
    print("Iniciando o teste de publicação...")

    # Mock setup
    mock_channel = AsyncMock()
    mock_connection = AsyncMock()
    mock_connection.channel.return_value = mock_channel
    mock_get_connection.return_value = mock_connection

    message = {
        "traceId": "1234",
        "mensagemId": "abcd",
        "conteudoMensagem": "Teste",
        "tipoNotificacao": "EMAIL"
    }

    await publish_message("fila.test.mock", message)

    print("Mensagem publicada (mock). Validando chamadas...")

    # Verificações
    mock_channel.declare_queue.assert_awaited_once_with("fila.test.mock", durable=True)
    mock_channel.default_exchange.publish.assert_awaited()

    args, kwargs = mock_channel.default_exchange.publish.call_args
    published_message = args[0]
    print("Payload publicado:", published_message.body.decode())

    assert published_message.body.decode() == '{"traceId": "1234", "mensagemId": "abcd", "conteudoMensagem": "Teste", "tipoNotificacao": "EMAIL"}'

    print("Teste finalizado com sucesso.")
