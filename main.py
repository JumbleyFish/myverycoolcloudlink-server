import os
import json
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import PlainTextResponse

app = FastAPI()
CONNECTED_USERS = set()

@app.get("/ping")
async def health_check():
    return PlainTextResponse("Server Alive")

@app.websocket("/")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    CONNECTED_USERS.add(websocket)
    
    # EXACT CloudLink v4 protocol initialization handshake frame
    handshake_packet = {
        "cmd": "server_version",
        "val": "0.2.0.1",
        "listener": "setup"
    }
    await websocket.send_text(json.dumps(handshake_packet))
    
    # Send a secondary frame to clear the connection queue checks
    status_packet = {
        "cmd": "statuscode",
        "val": "I am alive",
        "listener": "setup"
    }
    await websocket.send_text(json.dumps(status_packet))
    
    print(f"Handshake frame dispatched. Active terminals: {len(CONNECTED_USERS)}")
    
    try:
        while True:
            raw_message = await websocket.receive_text()
            
            # Simple global broadcast mirror for all engine packets
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
        print(f"Terminal severed. Active terminals: {len(CONNECTED_USERS)}")

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 10000))
    uvicorn.run(app, host="0.0.0.0", port=port)
