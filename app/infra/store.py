from typing import Dict, Any
from threading import Lock
from copy import deepcopy

class NotificationStore:
    def __init__(self):
        self._data: Dict[str, Dict[str, Any]] = {}
        self._lock = Lock()

    def save(self, trace_id: str, payload: Dict[str, Any]) -> None:
        with self._lock:
            payload["status_history"] = [payload["status"]]
            self._data[trace_id] = payload

    def update_status(self, trace_id: str, status: str) -> None:
        with self._lock:
            if trace_id in self._data:
                self._data[trace_id]["status"] = status
                self._data[trace_id].setdefault("status_history", []).append(status)

    def get(self, trace_id: str) -> Dict[str, Any] | None:
        with self._lock:
            item = self._data.get(trace_id)
            return deepcopy({"mensagemId": item["mensagemId"],
                             "conteudoMensagem": item["conteudoMensagem"],
                             "tipoNotificacao": item["tipoNotificacao"],
                             "status": item["status"],
                             "status_history": item.get("status_history", [])}) if item else None

    def all(self) -> Dict[str, Dict[str, Any]]:
        with self._lock:
            return deepcopy(self._data)
