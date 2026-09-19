import os
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import PlainTextResponse

app = FastAPI()
CONNECTED_USERS = set()

# --- NEW PATH FOR THE CRON MONITOR ---
@app.get("/ping")
async def health_check():
    # Dedicated regular HTTP path that avoids the 426 WebSocket rule
    return PlainTextResponse("Server Alive")

# --- TURBOWARP MULTIPLAYER CONNECTIONS ---
@app.websocket("/")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    CONNECTED_USERS.add(websocket)
    print(f"A player connected! Total players: {len(CONNECTED_USERS)}")
    
    try:
        while True:
            message = await websocket.receive_text()
            for user in list(CONNECTED_USERS):
                if user != websocket:
                    try:
                        await user.send_text(message)
                    except Exception:
                        pass
    except WebSocketDisconnect:
        pass
    finally:
        if websocket in CONNECTED_USERS:
            CONNECTED_USERS.remove(websocket)
        print(f"A player left. Total players: {len(CONNECTED_USERS)}")

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 10000))
    uvicorn.run(app, host="0.0.0.0", port=port)
