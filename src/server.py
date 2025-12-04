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
        
        print(f"+ {usernames[ws]} joined.")
        for c in clients:
            await c.send(f"+ {usernames[ws]} joined.")
                
        async for msg in ws:
            if msg.startswith("/set name "):
                newName = msg[10:].strip()
                oldName = usernames[ws]
                usernames[ws] = newName
                
                broadcast_msg = f"* {oldName} is now known as {newName}"
                print(broadcast_msg)
                for c in clients:
                    await c.send(broadcast_msg)
                continue

            for c in clients:
                full_msg = f"<{usernames[ws]}> {msg}"
                await c.send(full_msg)
            print (full_msg)
    finally:
        clients.remove(ws)
        print(f"- {usernames[ws]} leave.")
        for c in clients:
            await c.send(f"- {usernames[ws]} leave.")

        del usernames[ws]

async def server_chat():
    loop = asyncio.get_event_loop()

    while True:
        msg = await loop.run_in_executor(None, input, "> ")

        # if (msg.startswith("/say"))
        #     msg = msg[4].strip()

        broadcast_msg = f"[Server] {msg}"
        print(f"> {broadcast_msg}")

        for c in clients:
            try:
                await c.send(broadcast_msg)
            except:
                pass

async def main():
    async with websockets.serve(handle, "0.0.0.0", 8765):
        print("Server running on ws://0.0.0.0:8765")
        
        await asyncio.gather(
            asyncio.Future(),# Run forever
            server_chat()
        )

asyncio.run(main())