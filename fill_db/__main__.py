import yaml
import bson
import asyncio
from funcy import post_processing
import skema
from motor.motor_asyncio import AsyncIOMotorClient
from motor.core import Collection
from mongoke.support import get_skema
import fire

custom_resolvers = {
    'ObjectId': lambda: bson.ObjectId()
}

async def main(config, url, custom_resolvers={}):
        db = AsyncIOMotorClient(url)
        db: AsyncIOMotorClient = db.get_database()
        schema = get_skema(config)
        for typename, config in config['types'].items():
            collection = config['collection']
            items = skema.fake_data(schema, ref=typename, amount=100, resolvers=custom_resolvers)
            # print(dir(db[collection]))
            collection: Collection = db[collection]
            print(f'persisting {len(items)} documents in {collection.name} in db {collection.database.name}')
            for i in range(len(items) // 20):
                j = i*20
                if j+20 < len(items):
                    await collection.insert_many(items[j: j+20])


def cli(config_path, db,):
    asyncio.run(main(
        yaml.safe_load(open(config_path)),
        url=db,
        custom_resolvers=custom_resolvers
    ))

fire.Fire(cli)