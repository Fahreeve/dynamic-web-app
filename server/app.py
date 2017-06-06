from aiohttp import web
import aioredis

from server.routes import routes

app = web.Application()

for route in routes:
    app.router.add_route(route[0], route[1], route[2], name=route[3])

async def init_redis(app):
    #redis = await aioredis.create_redis(('localhost', 6379))
    redis = await aioredis.create_pool(('localhost', 6379))
    # redis = None
    app['db'] = redis

app.on_startup.append(init_redis)

async def close_redis(app):
    app['db'].close()
    await app['db'].wait_closed()

app.on_cleanup.append(close_redis)

if __name__ == "__main__":
    web.run_app(app, port=8080)
