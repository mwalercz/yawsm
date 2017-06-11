import aioodbc
import aiopg
import asyncio
import peewee
from peewee_async import AsyncDatabase, AsyncPostgresqlConnection


class SqliteDatabase(AsyncDatabase, peewee.SqliteDatabase):
    def init(self, database, **kwargs):
        self.min_connections = 1
        self.max_connections = 1
        super().init(database, **kwargs)
        self.init_async()

    if aiopg:
        import psycopg2
        Error = psycopg2.Error

    def init_async(self):
        if not aiopg:
            raise Exception("Error, aiopg is not installed!")
        self._async_conn_cls = AsyncPostgresqlConnection

    @property
    def connect_kwargs_async(self):
        """Connection parameters for `aiopg.Connection`
        """
        kwargs = self.connect_kwargs.copy()
        return kwargs


class AsyncSqliteConnection:
    """Asynchronous database connection pool.
    """
    def __init__(self, *, database=None, loop=None, timeout=None, **kwargs):
        self.conn = None
        self.loop = loop
        self.database = database
        self.timeout = timeout
        self.connect_kwargs = kwargs

    @asyncio.coroutine
    def acquire(self):
        """Acquire connection from pool.
        """
        return (yield from self.pool.acquire())

    def release(self, conn):
        """Release connection to pool.
        """
        self.pool.release(conn)

    async def connect(self):
        """Create connection pool asynchronously.
        """
        self.conn = await aioodbc.connect(
            loop=self.loop,
            timeout=self.timeout,
            dsn=self.database,
            **self.connect_kwargs)

    @asyncio.coroutine
    def close(self):
        """Terminate all pool connections.
        """
        del self.conn

    async def cursor(self, conn=None, *args, **kwargs):
        """Get a cursor for the specified transaction connection
        or acquire from the pool.
        """
        return await self.conn.cursor()

    @asyncio.coroutine
    def release_cursor(self, cursor, in_transaction=False):
        """Release cursor coroutine. Unless in transaction,
        the connection is also released back to the pool.
        """
        cursor.close()
