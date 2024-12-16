import aiohttp
import asyncio
from ..scripts import Scripted
from .function01 import Shortner
#======================================================================================

class Shortners(Shortner):

    def __init__(self, **kwargs):
        self.seon = aiohttp.ClientSession
        self.timo = kwargs.get("timeout", 30)
        self.apis = kwargs.get("api", Scripted.DATA01)
        self.site = kwargs.get("domain", Scripted.DATA02)

#======================================================================================

    async def clinton(self, recived):
        try: recived = await self.shortlink(recived)
        except asyncio.TimeoutError: pass
        except Exception: pass
        return recived

#======================================================================================

    async def shorturl(self, recived):
        try: recived = await self.shortlink(recived)
        except asyncio.TimeoutError: pass
        except Exception: pass
        return recived

#======================================================================================
