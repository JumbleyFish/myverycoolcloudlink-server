import os
import asyncio
import json
import websockets

# Keep track of active connections
CONNECTED_USERS = set()

async def handler(websocket):
    # Register new user
    CONNECTED_USERS.add(websocket)
    print(f"A player connected! Total players: {len(CONNECTED_USERS)}")
    
    try:
        async for message in websocket:
            # Parse Cloudlink text protocol packets safely
            try:
                data = json.loads(message)
            except json.JSONDecodeError:
                data = message
                
            # Broadcast the game state packet to every other connected player
            for user in CONNECTED_USERS:
                if user != websocket:
                    try:
                        await user.send(message)
                    except websockets.exceptions.ConnectionClosed:
                        pass
    except websockets.exceptions.ConnectionClosedError:
        pass
    finally:
        # Clean up on player disconnect
        CONNECTED_USERS.remove(websocket)
        print(f"A player left. Total players: {len(CONNECTED_USERS)}")

async def main():
    port = int(os.environ.get("PORT", 10000))
    print(f"🚀 Custom TurboWarp Server running on port {port}...")
    async with websockets.serve(handler, "0.0.0.0", port):
        await asyncio.Future()  # run forever

if __name__ == "__main__":
    asyncio.run(main())

