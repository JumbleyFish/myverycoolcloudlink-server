import os
import asyncio
import json
import websockets

CONNECTED_USERS = set()

async def handler(websocket, path):
    # --- HEALTH CHECK FOR UPTIME MONITORS ---
    if path == "/" and "Upgrade" not in websocket.request_headers:
        # If a monitor like UptimeRobot sends a regular web ping, say "I am alive!"
        response = "HTTP/1.1 200 OK\r\nContent-Length: 11\r\n\r\nServer Alive"
        websocket.transport.write(response.encode())
        websocket.transport.close()
        return

    # --- TURBOWARP MULTIPLAYER CONNECTIONS ---
    CONNECTED_USERS.add(websocket)
    print(f"A player connected! Total players: {len(CONNECTED_USERS)}")
    
    try:
        async_message_stream = websocket
        async for message in async_message_stream:
            try:
                data = json.loads(message)
            except json.JSONDecodeError:
                data = message
                
            for user in CONNECTED_USERS:
                if user != websocket:
                    try:
                        await user.send(message)
                    except websockets.exceptions.ConnectionClosed:
                        pass
    except websockets.exceptions.ConnectionClosedError:
        pass
    finally:
        if websocket in CONNECTED_USERS:
            CONNECTED_USERS.remove(websocket)
        print(f"A player left. Total players: {len(CONNECTED_USERS)}")

async def main():
    port = int(os.environ.get("PORT", 10000))
    print(f"🚀 Custom TurboWarp Server running on port {port}...")
    async with websockets.serve(handler, "0.0.0.0", port):
        await asyncio.Future()

if __name__ == "__main__":
    asyncio.run(main())

