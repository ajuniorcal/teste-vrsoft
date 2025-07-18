import json
from aio_pika import IncomingMessage
from app.infra.connection import get_rabbitmq_connection

QUEUE_NAME = "fila.notificacao.dlq.antonio"

async def processar_dlq(msg: IncomingMessage):
    async with msg.process():
        try:
            payload = json.loads(msg.body)
            trace_id = payload.get("traceId")
            print(f" [DLQ] Mensagem enviada para DLQ. TraceID: {trace_id} - Payload: {payload}")
        except Exception as e:
            print(f"Erro no processamento da DLQ: {e}")


async def start_dlq_consumer():
    connection = await get_rabbitmq_connection()
    channel = await connection.channel()
    await channel.set_qos(prefetch_count=1)

    queue = await channel.declare_queue(QUEUE_NAME, durable=True)
    await queue.consume(processar_dlq)
    print(f" [*] Consumidor da DLQ escutando: {QUEUE_NAME}")
