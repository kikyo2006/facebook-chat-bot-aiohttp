import json
import aiohttp
from os import environ
from aiohttp import web

# fanpage token
PAGE_ACCESS_TOKEN = ''
# verify token
VERIFY_TOKEN = 'a'

class BotControl(web.View):

    async def get(self):
        print('test')
        return web.Response(text='Forbidden', status=200)

    async def post(self):
        return web.Response(text='ok', status=200)


routes = [
    web.get('/', BotControl, name='verify'),
    web.post('/', BotControl, name='webhook'),
]

app = web.Application()
app.add_routes(routes)

if __name__ == '__main__':
    web.run_app(app, host='0.0.0.0', port=environ.get("PORT", 9090))
