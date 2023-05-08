import asyncio
from push_sender import cli as push_cli
from request_handler import cli as client_cli

async def main():
    try:
        await asyncio.gather(
            client_cli(),
            # push_cli(),
        )
    except (KeyboardInterrupt, SystemExit):
        print('Bot stopped')

if __name__ == '__main__':
    asyncio.run(main())

