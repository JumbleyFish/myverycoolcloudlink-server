import os
import json
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import PlainTextResponse

app = FastAPI()
CONNECTED_USERS = set()

# --- HEALTH CHECK FOR CRON-JOB.ORG ---
@app.get("/")
async def health_check():
    # Returns a valid HTTP 200 response that satisfies the pinger
    return PlainTextResponse("Server Alive")

# --- TURBOWARP MULTIPLAYER CONNECTIONS ---
@app.websocket("/")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    CONNECTED_USERS.add(websocket)
    print(f"A player connected! Total players: {len(CONNECTED_USERS)}")
    
    try:
        while True:
            # Listen for continuous TurboWarp data messages
            message = await websocket.receive_text()
            
            # Broadcast incoming data to all other online players
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
    print(f"🚀 Custom TurboWarp Server running on port {port}...")
    uvicorn.run(app, host="0.0.0.0", port=port)
