from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
import uuid
import asyncio
import logging
from app.infra.publisher import publish_message
from app.infra.store import NotificationStore
from app.models import NotificationRequest, NotificationResponse

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Sistema de Notificações Assíncronas")

store = NotificationStore()

@app.post("/api/notificar", response_model=NotificationResponse, status_code=202)
async def notificar(payload: NotificationRequest):
    """Recebe uma solicitação de notificação e a envia para processamento assíncrono."""
    try:
        trace_id = str(uuid.uuid4())
        mensagem_id = payload.mensagemId or str(uuid.uuid4())

        store.save(trace_id, {
            "mensagemId": mensagem_id,
            "conteudoMensagem": payload.conteudoMensagem,
            "tipoNotificacao": payload.tipoNotificacao,
            "status": "RECEBIDO"
        })

        logger.info(f"[RECEBIDO] traceId={trace_id}, mensagemId={mensagem_id}")

        await publish_message(
            queue=f"fila.notificacao.entrada.antonio",
            message={
                "traceId": trace_id,
                "mensagemId": mensagem_id,
                "conteudoMensagem": payload.conteudoMensagem,
                "tipoNotificacao": payload.tipoNotificacao
            }
        )

        return NotificationResponse(mensagemId=mensagem_id, traceId=trace_id)

    except Exception as e:
        logger.exception("Erro ao processar notificação")
        raise HTTPException(status_code=500, detail=f"Erro ao processar notificação: {str(e)}")

@app.get("/api/notificacao/status/{trace_id}")
async def consultar_status(trace_id: str):
    """Consulta o status atual de uma notificação via traceId."""
    notificacao = store.get(trace_id)
    if notificacao is None:
        raise HTTPException(status_code=404, detail="traceId não encontrado")
    return {"traceId": trace_id, **notificacao}