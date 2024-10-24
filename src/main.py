import asyncio
import websockets

connected_clients = set()  # Keep track of connected clients

async def handler(websocket, path):
    connected_clients.add(websocket)
    try:
        async for message in websocket:
            print(f"Received message: {message}")
            await broadcast(message)  # Send the message to all clients
    finally:
        connected_clients.remove(websocket)

async def broadcast(message):
    if connected_clients:  # Check if there are any clients
        # Use gather instead of wait to handle broadcasting to all clients
        await asyncio.gather(*(client.send(message) for client in connected_clients))

async def main():
    # Change "localhost" to "0.0.0.0" if needed to allow connections from any IP address
    async with websockets.serve(handler, "localhost", 6789):
        print("Server started at ws://localhost:6789")
        await asyncio.Future()  # Run forever

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nServer shut down.")


