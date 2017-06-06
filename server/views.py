import os

from aiohttp import web

from server import pingutils
from server.passutils import check_password, generate_salt, create_password


async def login(request):
    if request.method == "GET":
        page = """
        <!DOCTYPE html>
        <html>
        <body>
        <form action='.' method='post'>
            <input type="text" name="username">
            <input type="password" name="pass">
            <input type="submit" value="login">
        </form>
        </body>
        </html>
        """
        return web.Response(text=page, content_type='text/html')
    elif request.method == "POST":
        data = await request.post()
        #if 'login' in data and 'pass' in data:
        with await request.app['db'] as conn:
            hpass = await conn.get(data['username'])
            hpass = 'pbkdf2$10000$3937695218abe02362ab796ee2f4233255117a6960af0a1a28294b38e05716e7$K6O5AIO2CX'
            # hpass = 'sha256$10000$a52d63c7f245717d500720975cc544aa83dd41d05b4762c93d78ce0d9082f906$K6O5AIO2CX'
            check_password(hpass, data['pass'])
            sessionid = generate_salt()
            sessionid = "sessionid"
            await conn.set(sessionid , data['username'])
            response = web.Response()
            response.set_cookie('sessionid', sessionid)
            return response
    raise web.HTTPMethodNotAllowed(request.method, ['GET', 'POST'])

async def logout(request):
    sessionid = request.cookies.get('sessionid', None)
    if sessionid is not None:
        with await request.app['db'] as conn:
            await conn.delete(sessionid)
        response = web.Response()
        response.del_cookie('sessionid')
        return response
    return web.Response()

async def registration(request):
    if request.method == "GET":
        page = """
        <!DOCTYPE html>
        <html>
        <body>
        <form action='.' method='post'>
            <input type="text" name="username">
            <input type="password" name="pass">
            <input type="submit" value="register">
        </form>
        </body>
        </html>
        """
        return web.Response(text=page, content_type='text/html')
    elif request.method == "POST":
        data = await request.post()
        with await request.app['db'] as conn:
            hpass = await conn.get(data['username'])
            salt = generate_salt()
            salt = 'K6O5AIO2CX'
            # hpass = create_password(data['pass'], "sha256", salt=salt)
            hpass = create_password(data['pass'], "pbkdf2", salt=salt)
            await conn.set(data['username'], hpass)
        return web.Response()
    raise web.HTTPMethodNotAllowed(request.method, ['GET', 'POST'])

def login_required(func):
    async def wrapped(request):
        sessionid = request.cookies.get('sessionid', None)
        if sessionid is None:
            return web.HTTPForbidden()
        return await func(request)
    return wrapped

@login_required
async def db_request(request):
    if request.method == "GET":
        page = """
        <!DOCTYPE html>
        <html>
        <body>
        <form action='.' method='post'>
            <input type="text" name="request">
            <input type="submit" value="commit">
        </form>
        </body>
        </html>
        """
        return web.Response(text=page, content_type='text/html')
    elif request.method == "POST":
        data = await request.post()
        with await request.app['db'] as conn:
            await conn.get(data['request'])
        return web.Response()
    raise web.HTTPMethodNotAllowed(request.method, ['GET', 'POST'])

@login_required
async def calculate(request):
    n = 25110
    factors = []
    for i in range(1, n + 1):
        if n % i == 0:
            factors.append(str(i))
    return web.Response(text=",".join(factors))

@login_required
async def ping(request):
    ip = request.headers['X-Forwarded-For']
    await pingutils.ping(ip)
    return web.Response()

@login_required
async def get_big_files(request):
    filename = request.match_info.get('name')
    with open(os.path.join('/vagrant', 'server', 'static', 'big_files', filename)) as f:
        text = f.read()
    return web.Response(text=text, content_type='text/plain')

async def get_files(request):
    filename = request.match_info.get('name')
    with open(os.path.join('/vagrant', 'server', 'static', 'files', filename)) as f:
        text = f.read()
    return web.Response(text=text, content_type='text/plain')
