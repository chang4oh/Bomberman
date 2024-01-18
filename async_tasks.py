# async_tasks.py
import asyncio
import threading

async def async_task():
    while True:
        print("Performing an asynchronous task...")
        await asyncio.sleep(1)

def start_asyncio_loop():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(async_task())

def run_async_tasks():
    asyncio_thread = threading.Thread(target=start_asyncio_loop, daemon=True)
    asyncio_thread.start()