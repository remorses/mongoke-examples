
from tartiflette import Resolver
from .support import strip_nones, connection_resolver, zip_pluck, select_keys, get_pagination
from operator import setitem
from funcy import omit

def filter_nodes_by_guard(nodes, fields):
    for x in nodes:
        try:
            
            yield omit(x or dict(), fields)
        except Exception:
            pass


map_fields_to_types = {
        "timestamp": "Float",
        "count": "Float"
    }

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

@Resolver('Query.eventWindows')
async def resolve_query_eventwindows(parent, args, ctx, info):
    where = strip_nones(args.get('where', {}))
    cursorField = args.get('cursorField',) or ('_id' if '_id' in map_fields_to_types else list(map_fields_to_types.keys())[0])
    headers = ctx['req'].headers
    jwt = ctx['req'].jwt_payload
    fields = []
    
    pagination = get_pagination(args,)
    data = await connection_resolver(
        collection=ctx['db']['events'], 
        where=where,
        cursorField=cursorField,
        pagination=pagination,
        scalar_name=map_fields_to_types[cursorField],
        pipeline=pipeline,
    )
    data['nodes'] = list(filter_nodes_by_guard(data['nodes'], fields))
    
    return data

