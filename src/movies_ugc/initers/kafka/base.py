from movies_ugc.initers.kafka.create_schemas import create_schemas
from movies_ugc.initers.kafka.create_topics import create_topics


async def init():
    await create_topics()
    await create_schemas()
