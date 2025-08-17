from fastapi import APIRouter, WebSocket, WebSocketDisconnect

router = APIRouter(prefix="/collab", tags=["Collaboration"])

class ConnectionManager:
    def __init__(self):
        self.active_connections: dict = {}

    async def connect(self, session_id: str, websocket: WebSocket):
        await websocket.accept()
        if session_id not in self.active_connections:
            self.active_connections[session_id] = []
        self.active_connections[session_id].append(websocket)

    def disconnect(self, session_id: str, websocket: WebSocket):
        self.active_connections[session_id].remove(websocket)
        if not self.active_connections[session_id]:
            del self.active_connections[session_id]

    async def broadcast(self, session_id: str, message: dict):
        for connection in self.active_connections.get(session_id, []):
            await connection.send_json(message)

manager = ConnectionManager()

@router.websocket("/ws/session/{session_id}")
async def websocket_endpoint(websocket: WebSocket, session_id: str):
    await manager.connect(session_id, websocket)
    try:
        while True:
            data = await websocket.receive_json()
            await manager.broadcast(session_id, data)
    except WebSocketDisconnect:
        manager.disconnect(session_id, websocket)
