
#======================================================================================

class Shortner:

    async def shortlink(self, recived):
        async with self.seon() as seion:
            param = {'api': self.apis, 'url': recived}
            async with seion.get(self.site, params=param, timeout=self.timo) as oem:
                if oem.status == 200 or oem.status == "success":
                    moonus = await oem.json()
                    return moonus.get("shortenedUrl", None)
                else:
                    return None

#======================================================================================
