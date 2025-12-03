import asyncio
import websockets
import random
from datetime import datetime

clients = set()
usernames = {}

async def handle(ws):
    clients.add(ws)
    try:
        username = await ws.recv()
        
        if not username.strip():
            username = f"Player_{random.randint(1,99)}"
        usernames[ws] = username
        
        for c in clients:
            await c.send(f"+ {usernames[ws]} joined.")
                
        async for msg in ws:
            if msg.startswith("/set name "):
                newName = msg[10:].strip()
                oldName = usernames[ws]
                usernames[ws] = newName

                broadcast_msg = f"* {oldName} is now known as {newName}"
            
                for c in clients:
                    await c.send(broadcast_msg)
                continue

            for c in clients:
                full_msg = f"<{usernames[ws]}> {msg}"
                await c.send(full_msg)
    finally:
        clients.remove(ws)
        
        for c in clients:
            await c.send(f"- {usernames[ws]} leave.")

        del usernames[ws]

async def main():
    async with websockets.serve(handle, "0.0.0.0", 8765):
        print("Server running on ws://0.0.0.0:8765")
        await asyncio.Future()  # Run forever

asyncio.run(main())