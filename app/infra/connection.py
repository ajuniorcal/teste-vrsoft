import aio_pika
from aio_pika import RobustConnection
from app.config import RABBITMQ_URL

_rabbitmq_connection: RobustConnection | None = None

async def get_rabbitmq_connection() -> RobustConnection:
    global _rabbitmq_connection
    if _rabbitmq_connection is None or _rabbitmq_connection.is_closed:
        _rabbitmq_connection = await aio_pika.connect_robust(RABBITMQ_URL)
    return _rabbitmq_connection