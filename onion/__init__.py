import json, asyncio, copy
from logger import error_log

class peer:
    # custom 
    async def init(self, db, cid):
        self.db = db
        await self.db.query('CREATE table if not exists "userbase" ("id" INTEGER, "mylang" TEXT DEFAULT "en", "tolang" TEXT DEFAULT "en", "sepa" TEXT DEFAULT "#")')
        js = await self.db.fetch("SELECT * from userbase where id={}".format(cid))
        if len(js) < 1:
            print("\033[91m{}\033[00m" .format(" creating new user"))
            # generate new secret hash
            if await self.db.query('INSERT into userbase (id, mylang, tolang, sepa) values (?,?,?,?)', (cid, 'en', 'en','#')):
                js = await self.db.fetch("select * from userbase where id={}".format(cid))
        # format peer js
        self.js = js[0]

    async def update(self):
        if await self.db.query("UPDATE userbase set mylang = ?, tolang = ?, sepa = ? where id = ?", [self.js['mylang'], self.js['tolang'], self.js['sepa'], self.js['id']]):
           return True
        else:
           return False
    
    async def mylang(self, lang = None):
        if lang:
            self.js['mylang'] = lang
            await self.update()
        return self.js['mylang']
    
    async def tolang(self, lang = None):
        if lang:
            self.js['tolang'] = lang
            await self.update()
        return self.js['tolang']
    
    async def sepa(self, symbol = None):
        if symbol:
            self.js['sepa'] = symbol
            await self.update()
        return self.js['sepa']