import json
import aiohttp
from os import environ
from aiohttp import web

# fanpage token
PAGE_ACCESS_TOKEN = ''
# verify token
VERIFY_TOKEN = ''

class BotControl(web.View):

    async def get(self):
        query = self.request.rel_url.query
        if(query.get('hub.mode') == "subscribe" and query.get("hub.challenge")):
            if not query.get("hub.verify_token") == VERIFY_TOKEN:
                return web.Response(text='Verification token mismatch', status=403)
            return web.Response(text=query.get("hub.challenge"))
        return web.Response(text='Forbidden', status=403)

    async def post(self):
        data = await self.request.json()
        if data.get("object") == "page":
            await self.send_greeting("Chào bạn. Mình là bot demo của học python.")

            for entry in data.get("entry"):
                for messaging_event in entry.get("messaging"):
                    if messaging_event.get("message"):
                        sender_id = messaging_event["sender"]["id"]
                        message_text = messaging_event["message"]["text"]

                        if any(["chào" in message_text.lower(), "hi " in message_text.lower(),
                                "hello" in message_text.lower(), "có ai" in message_text.lower(),
                                "có ở đó" in message_text.lower(), "hi" == message_text.lower()]):
                            await self.send_message(sender_id, "chào đằng ấy :)")
                        elif any(["bạn tên" in message_text.lower(), "mày tên" in message_text.lower(),
                                "your name" in message_text.lower(), "cậu tên" in message_text.lower()]):
                            await self.send_message(sender_id, "mình tên là bot demo aiohttp nha")
                        elif any(["tác giả" in message_text.lower(), "người viết" in message_text.lower(),
                                "ai viết" in message_text.lower(), "ba mày" in message_text.lower(), "cha mày" in message_text.lower()
                                     , "bố mày" in message_text.lower(), "tía mày" in message_text.lower()]):
                            await self.send_message(sender_id, "ahihi bạn vào đây để xem ai là người tạo ra mình nha :3 https://www.hocpython.com")
                        else:
                            await self.send_message(sender_id, "Bạn dễ thương gì ấy ơi, ghé https://www.hocpython.com để ủng hộ ba mình nha :3 ")
                            await self.send_message(sender_id,
                                              "mình nghe ba mình nói nếu mình được 100 like sẽ chia sẻ với các bạn thêm tính năng mới của mình đó :3")

        return web.Response(text='ok', status=200)

    async def send_greeting(self, message_text):
        params = {
            "access_token": PAGE_ACCESS_TOKEN
        }
        headers = {
            "Content-Type": "application/json"
        }
        data = json.dumps({
            "setting_type": "greeting",
            "greeting": {
                "text": message_text
            }
        })
        async with aiohttp.ClientSession() as session:
            await session.post("https://graph.facebook.com/v3.0/me/thread_settings", params=params, headers=headers, data=data)

    async def send_message(self, sender_id, message_text):

        params = {
            "access_token": PAGE_ACCESS_TOKEN
        }
        headers = {
            "Content-Type": "application/json"
        }
        data = json.dumps({
            "recipient": {
                "id": sender_id
            },
            "message": {
                "text": message_text
            }
        })

        async with aiohttp.ClientSession() as session:
            await session.post("https://graph.facebook.com/v3.0/me/messages", params=params, headers=headers, data=data)



routes = [
    web.get('/', BotControl, name='verify'),
    web.post('/', BotControl, name='webhook'),
]

app = web.Application()
app.add_routes(routes)

if __name__ == '__main__':
    web.run_app(app, host='0.0.0.0', port=environ.get("PORT", 9090))
