
from tartiflette import Resolver
from .support import strip_nones, zip_pluck
import mongodb_streams
from operator import setitem
from funcy import omit

pipeline: list = [
    {
        "$group": {
            "_id": {
                "$subtract": [
                    "$timestamp",
                    {
                        "$mod": [
                            "$timestamp",
                            60000
                        ]
                    }
                ]
            },
            "count": {
                "$sum": 1
            }
        }
    },
    {
        "$project": {
            "timestamp": "$_id",
            "count": 1
        }
    }
]

@Resolver('Query.eventWindow')
async def resolve_query_eventwindow(parent, args, ctx, info):
    where = strip_nones(args.get('where', {}))
    headers = ctx['req'].headers
    jwt = ctx['req'].jwt_payload
    fields = []
    
    collection = ctx['db']['events']
    x = await mongodb_streams.find_one(collection, match=where, pipeline=pipeline)
    
    
    if fields:
        x = omit(x or dict(), fields)
    return x
