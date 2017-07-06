import asyncio


class StrictEventLoopPolicy(asyncio.DefaultEventLoopPolicy):
    def new_event_loop(self):
        if self._local._set_called:
            raise RuntimeError('An event loop has already been set')
        return super().new_event_loop()


