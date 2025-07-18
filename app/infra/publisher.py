import aio_pika
import logging
import json
from app.infra.connection import get_rabbitmq_connection

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def publish_message(queue: str, message: dict) -> None:
    try:
        connection = await get_rabbitmq_connection()
        channel = await connection.channel()

        await channel.declare_queue(queue, durable=True)

        body = json.dumps(message).encode()
        await channel.default_exchange.publish(
            aio_pika.Message(body=body),
            routing_key=queue
        )
    except Exception as e:
        logger.error(f"Erro ao publicar mensagem na fila {queue}: {e}")

