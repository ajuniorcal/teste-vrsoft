import asyncio
import json
import random
from aio_pika import IncomingMessage
from app.infra.connection import get_rabbitmq_connection
from app.infra.store import NotificationStore
from app.infra.publisher import publish_message

store = NotificationStore()
QUEUE_NAME = "fila.notificacao.validacao.antonio"

async def processar_validacao(msg: IncomingMessage):
    async with msg.process():
        try:
            payload = json.loads(msg.body)
            trace_id = payload.get("traceId")
            tipo = payload.get("tipoNotificacao")

            await asyncio.sleep(random.uniform(0.5, 1))

            if random.random() < 0.05:
                store.update_status(trace_id, "FALHA_ENVIO_FINAL")
                await publish_message("fila.notificacao.dlq.antonio", payload)
                return

            store.update_status(trace_id, "ENVIADO_SUCESSO")

        except Exception as e:
            print(f"Erro no processamento de validacao/envio: {e}")


async def start_validacao_consumer():
    connection = await get_rabbitmq_connection()
    channel = await connection.channel()
    await channel.set_qos(prefetch_count=1)

    queue = await channel.declare_queue(QUEUE_NAME, durable=True)
    await queue.consume(processar_validacao)
    print(f" [*] Consumidor de validacao escutando: {QUEUE_NAME}")
