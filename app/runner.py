import asyncio
from app.consumers.entrada import start_entrada_consumer
from app.consumers.retry import start_retry_consumer
from app.consumers.validacao import start_validacao_consumer
from app.consumers.dlq import start_dlq_consumer

async def main():
    await asyncio.gather(
        start_entrada_consumer(),
        start_retry_consumer(),
        start_validacao_consumer(),
        start_dlq_consumer()
    )

if __name__ == "__main__":
    asyncio.run(main())
