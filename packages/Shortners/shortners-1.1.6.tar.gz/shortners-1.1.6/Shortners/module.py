import aiohttp
import asyncio
from .scripts import Scripted
#======================================================================================

class Shortner:

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

    async def shortlink(self, recived):
        async with self.seon() as seion:
            param = {'api': self.apis, 'url': recived}
            async with seion.get(self.site, params=param, timeout=self.timo) as res:
                if res.status == "success" or res.status == 200:
                    dataes = await res.json()
                    reurns = dataes["shortenedUrl"]
                    moonus = reurns if reurns else None
                    return moonus
                else:
                    return None

#======================================================================================
