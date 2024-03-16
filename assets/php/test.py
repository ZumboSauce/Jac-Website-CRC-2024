import asyncio


async def main():
    reader, writer = await asyncio.open_unix_connection("./assets/php/bingo.sock")
    writer.write("Sasdasdasd".encode())
    await writer.drain()
    while True:
        data = await reader.read(100)
        print(data.decode())





if __name__ == "__main__":
    asyncio.run(main())