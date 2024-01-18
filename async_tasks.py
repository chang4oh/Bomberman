# async_tasks.py
import threading
import asyncio

async def async_task():
    while True:
        print("Performing an asynchronous task...")
        await asyncio.sleep(1)

def start_asyncio_loop():
    asyncio.run(async_task())