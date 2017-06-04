import asyncio
import inspect


class TaskScheduler:
    def schedule_task(self, func, arg):
        asyncio.ensure_future(
            self.execute(
                func=func,
                arg=arg,
            )
        )

    async def execute(self, func, arg):
        if inspect.iscoroutinefunction(func):
            await func(arg)
        else:
            func(arg)
