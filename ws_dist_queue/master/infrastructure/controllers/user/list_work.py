class ListWorkController:
    def __init__(self, user_auth, usecase, user_client):
        self.user_auth = user_auth
        self.usecase = usecase
        self.user_client = user_client

    async def handle(self, req):
        credentials = self.user_auth.get_credentials(req.sender.peer)
        result = await self.usecase.perform(credentials.username)
        self.user_client.send(
            recipient=req.sender,
            message=result,
        )
