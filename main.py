import os
import json
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import PlainTextResponse

app = FastAPI()
CONNECTED_USERS = set()

# --- HEALTH CHECK FOR CRON-JOB.ORG ---
@app.get("/ping")
async def health_check():
    return PlainTextResponse("Server Alive")

# --- OFFICIAL CLOUDLINK V4 PROTOCOL TRANSLATOR ---
@app.websocket("/")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    CONNECTED_USERS.add(websocket)
    
    # Cloudlink V4 extension expects a "handshake" packet to successfully connect
    handshake_packet = {
        "cmd": "handshake",
        "val": {
            "version": "0.2.0.1",
            "motd": "Custom Cloudlink Server Live!"
        },
        "listener": "setup"
    }
    await websocket.send_text(json.dumps(handshake_packet))
    print(f"Player handshaked successfully! Total online: {len(CONNECTED_USERS)}")
    
    try:
        while True:
            # Listen for continuous game data streams from TurboWarp
            raw_message = await websocket.receive_text()
            
            # Broadcast the data packet to every other player in the room
            for user in list(CONNECTED_USERS):
                if user != websocket:
                    try:
                        await user.send_text(raw_message)
                    except Exception:
                        pass
                        
    except WebSocketDisconnect:
        pass
    finally:
        if websocket in CONNECTED_USERS:
            CONNECTED_USERS.remove(websocket)
        print(f"Player left. Total online: {len(CONNECTED_USERS)}")

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 10000))
    # Binds to 0.0.0.0 so Render can instantly detect the port mapping
    uvicorn.run(app, host="0.0.0.0", port=port)
