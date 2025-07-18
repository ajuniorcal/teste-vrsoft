import asyncio
import json
import random
from aio_pika import IncomingMessage
from app.infra.connection import get_rabbitmq_connection
from app.infra.store import NotificationStore
from app.infra.publisher import publish_message

store = NotificationStore()
QUEUE_NAME = "fila.notificacao.entrada.antonio"

async def processar_entrada(msg: IncomingMessage):
    async with msg.process():
        try:
            print("Mensagem recebida da fila:", msg.body)

            payload = json.loads(msg.body)
            trace_id = payload.get("traceId")
            print(f"traceId extraído: {trace_id}")

            # Cria o registro na store ao receber a mensagem
            store.create(trace_id, {
                "conteudoMensagem": payload.get("conteudoMensagem"),
                "tipoNotificacao": payload.get("tipoNotificacao"),
                "status": "RECEBIDO"
            })

            if random.random() < 0.15:
                print("Simulando falha inicial, enviando para retry")
                store.update_status(trace_id, "FALHA_PROCESSAMENTO_INICIAL")
                await publish_message("fila.notificacao.retry.antonio", payload)
                return

            await asyncio.sleep(random.uniform(1, 1.5))

            print("Atualizando status para 'PROCESSADO_INTERMEDIARIO'")
            store.update_status(trace_id, "PROCESSADO_INTERMEDIARIO")

            print("Enviando mensagem para fila de validação")
            await publish_message("fila.notificacao.validacao.antonio", payload)

        except Exception as e:
            print(f"Erro no processamento de entrada: {e}")


async def start_entrada_consumer():
    connection = await get_rabbitmq_connection()
    channel = await connection.channel()
    await channel.set_qos(prefetch_count=1)

    queue = await channel.declare_queue(QUEUE_NAME, durable=True)
    await queue.consume(processar_entrada)
    print(f" [*] Consumidor de entrada escutando: {QUEUE_NAME}")
