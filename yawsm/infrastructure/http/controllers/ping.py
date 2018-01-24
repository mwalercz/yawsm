from aiohttp.web_response import Response


class PingController:
    async def handle(self, request):
        return Response(text='pong')
