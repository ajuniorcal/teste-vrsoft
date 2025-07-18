import asyncio
import json
import random
from aio_pika import IncomingMessage
from app.infra.connection import get_rabbitmq_connection
from app.infra.store import NotificationStore
from app.infra.publisher import publish_message

store = NotificationStore()
QUEUE_NAME = "fila.notificacao.retry.antonio"

async def processar_retry(msg: IncomingMessage):
    async with msg.process():
        try:
            payload = json.loads(msg.body)
            trace_id = payload.get("traceId")

            await asyncio.sleep(3)

            if random.random() < 0.2:
                store.update_status(trace_id, "FALHA_FINAL_REPROCESSAMENTO")
                await publish_message("fila.notificacao.dlq.antonio", payload)
                return

            store.update_status(trace_id, "REPROCESSADO_COM_SUCESSO")
            await publish_message("fila.notificacao.validacao.antonio", payload)

        except Exception as e:
            print(f"Erro no processamento de retry: {e}")


async def start_retry_consumer():
    connection = await get_rabbitmq_connection()
    channel = await connection.channel()
    await channel.set_qos(prefetch_count=1)

    queue = await channel.declare_queue(QUEUE_NAME, durable=True)
    await queue.consume(processar_retry)
    print(f" [*] Consumidor de retry escutando: {QUEUE_NAME}")
