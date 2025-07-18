from typing import Optional, Literal
from pydantic import BaseModel, Field
import uuid

class NotificationRequest(BaseModel):
    mensagemId: Optional[str] = Field(default=None, description="UUID opcional da mensagem. Será gerado se não fornecido.")
    conteudoMensagem: str = Field(..., min_length=1, description="Conteúdo da notificação a ser enviada")
    tipoNotificacao: Literal["EMAIL", "SMS", "PUSH"] = Field(..., description="Tipo da notificação: EMAIL, SMS ou PUSH")

    class Config:
        schema_extra = {
            "example": {
                "mensagemId": "a1b2c3d4-e5f6-7890-abcd-1234567890ab",
                "conteudoMensagem": "Mensagem de teste",
                "tipoNotificacao": "EMAIL"
            }
        }

class NotificationResponse(BaseModel):
    mensagemId: str = Field(..., description="UUID da mensagem")
    traceId: str = Field(..., description="UUID do rastreamento da requisição")
