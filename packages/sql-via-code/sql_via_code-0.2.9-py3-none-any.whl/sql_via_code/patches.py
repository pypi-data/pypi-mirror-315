import weakref
from sqlalchemy.ext.asyncio import AsyncConnection

def patch_async_connection_init():
    original_init = AsyncConnection.__init__

    def connection_init_hook(connection_self, *args, **kwargs):
        weakref.finalize(connection_self, lambda: None)  # Finalize clean-up
        return original_init(connection_self, *args, **kwargs)

    AsyncConnection.__init__ = connection_init_hook
