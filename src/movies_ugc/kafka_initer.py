import asyncio

from movies_ugc.initers.kafka.base import init

if __name__ == "__main__":
    asyncio.run(init())
