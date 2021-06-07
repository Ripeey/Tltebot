#!/usr/bin/python3
import aiosqlite as sqlite3
import asyncio, copy
from sqlite3 import Error as sql_error
from logger import error_log

class litedb:
    # basics
    async def connect(self, db_name, assoc = True):
        try:
            con = await sqlite3.connect(db_name)
            self.assoc = assoc
            if self.assoc : con.row_factory = sqlite3.Row
            self.con = con
            print("\033[91m{}\033[00m" .format(db_name + " connection established"))   
        except sql_error as err:
            error_log(err)
            print("\033[91m{}\033[00m" .format(db_name + " connection falied"))

    async def close(self):
            await self.con.close()
            print("\033[91m{}\033[00m" .format(db_name + " connection closed"))

    async def query(self, sql, entities = False):
        cursorObj = await self.con.cursor()
        if entities:
            # commit as insert or update
            try:
                await cursorObj.execute(sql, entities)
                await self.con.commit()
                return True
            except Exception as err:
                error_log(err)
                return False
        else:
            try:
                # commit as update, use fetch() for select
                await cursorObj.execute(sql)
                await self.con.commit()
                return True
            except Exception as err:
                error_log(err)
                return False


    async def fetch(self, sql):
        # select and fetch
        cursorObj = await self.con.cursor()
        try:
            await cursorObj.execute(sql)
            rows = await cursorObj.fetchall()
            if self.assoc:
                result = []
                for row in rows:
                    result.append(dict(row).copy())
                return result
            else:
                return rows
        except Exception as err:
            return False
