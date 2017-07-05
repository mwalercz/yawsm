import asyncio
import inspect


class Executor:
    def execute(self, func, arg):
        return asyncio.ensure_future(
            self._execute(
                func=func,
                arg=arg,
            )
        )

    async def _execute(self, func, arg):
        if inspect.iscoroutinefunction(func):
            return await func(arg)
        else:
            return func(arg)
