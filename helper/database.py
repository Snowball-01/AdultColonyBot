import datetime
import motor.motor_asyncio
from config import Config
from .utils import send_log
from dateutil.relativedelta import relativedelta


class Database:

    def __init__(self, uri, database_name):
        self._client = motor.motor_asyncio.AsyncIOMotorClient(uri)
        self.db = self._client[database_name]
        self.col = self.db.users
        self.bot = self.db.bots
        self.dumpfiles = self.db.dumpfiles
        self.tokens = self.db.tokens

    def new_user(self, id):
        return dict(
            id=int(id),
            join_date=datetime.date.today().isoformat(),
            user_type=dict(is_premium=False, plan="free", plan_expire_on=None),
            ban_status=dict(
                is_banned=False,
                ban_duration=0,
                banned_on=datetime.date.max.isoformat(),
                ban_reason="",
            ),
        )

    async def add_files(
        self, link, msg_id, file_id, file_name, file_size, file_type, mime_type, caption
    ):
        dumpfileinfo = {
            "link": link,
            'msg_id': msg_id,
            "file_id": file_id,
            "file_name": file_name,
            "file_size": file_size,
            "file_type": file_type,
            "mime_type": mime_type,
            "caption": caption
        }
        await self.dumpfiles.insert_one(dumpfileinfo)
        
    
    async def add_token(self, token, username):
        checkToken = await self.tokens.find_one({"token": token})
        if checkToken:
            return
        await self.tokens.insert_one({"token": token, "username": username})
    
    async def get_token(self, token):
        token = await self.tokens.find_one({"token": token})
        return token
        
    async def get_all_tokens(self):
        cursor = self.tokens.find({})
        tokens = []
        async for document in cursor:
            tokens.append(document)
        return tokens
    
    async def get_files(self, link):
        cursor = self.dumpfiles.find({"link": link})
        dumpfile = []

        async for document in cursor:
            dumpfile.append(document)
        return dumpfile if dumpfile else None

    async def add_user_bot(self, user_datas):
        if not await self.is_user_bot_exist(user_datas["user_id"]):
            await self.bot.insert_one(user_datas)

    async def remove_user_bot(self, user_id):
        await self.bot.delete_many({"user_id": int(user_id), "is_bot": False})

    async def is_user_bot_exist(self, user_id):
        user = await self.bot.find_one({"user_id": user_id, "is_bot": False})
        return bool(user)

    async def get_user_bot(self, user_id: int):
        user = await self.bot.find_one({"user_id": user_id, "is_bot": False})
        return user if user else None

    async def remove_user_bot(self, user_id):
        await self.bot.delete_many({"user_id": int(user_id), "is_bot": False})

    async def add_user(self, b, m):
        u = m.from_user
        if not await self.is_user_exist(u.id):
            user = self.new_user(u.id)
            await self.col.insert_one(user)
            await send_log(b, u)

    async def is_user_exist(self, id):
        user = await self.col.find_one({"id": int(id)})
        return True if user else False

    async def total_users_count(self):
        count = await self.col.count_documents({})
        return count

    async def get_all_users(self):
        all_users = self.col.find({})
        return all_users

    async def delete_user(self, user_id):
        await self.col.delete_many({"id": int(user_id)})

    async def remove_ban(self, id):
        ban_status = dict(
            is_banned=False,
            ban_duration=0,
            banned_on=datetime.date.max.isoformat(),
            ban_reason="",
        )
        await self.col.update_one({"id": id}, {"$set": {"ban_status": ban_status}})

    async def ban_user(self, user_id, ban_duration, ban_reason):
        ban_status = dict(
            is_banned=True,
            ban_duration=ban_duration,
            banned_on=datetime.date.today().isoformat(),
            ban_reason=ban_reason,
        )
        await self.col.update_one({"id": user_id}, {"$set": {"ban_status": ban_status}})

    async def get_ban_status(self, id):
        default = dict(
            is_banned=False,
            ban_duration=0,
            banned_on=datetime.date.max.isoformat(),
            ban_reason="",
        )
        user = await self.col.find_one({"id": int(id)})
        return user.get("ban_status", default)

    async def get_all_banned_users(self):
        banned_users = self.col.find({"ban_status.is_banned": True})
        return banned_users

    async def add_premium(self, user_id, plan):
        # Get today's date
        today = datetime.date.today()

        # Calculate the date after one month
        next_month = today + relativedelta(months=1)

        user_type = dict(
            is_premium=True,
            plan=plan,
            plan_expire_on=str(next_month),
        )
        await self.col.update_one(
            {"id": int(user_id)}, {"$set": {"user_type": user_type}}
        )

    async def remove_premium(self, id):
        user_type = dict(
            is_premium=False,
            plan="free",
            plan_expire_on=None,
        )
        await self.col.update_one({"id": int(id)}, {"$set": {"user_type": user_type}})

    async def get_user_status(self, id):
        default = dict(
            is_premium=False,
            plan="free",
            plan_expire_on=None,
        )
        user = await self.col.find_one({"id": int(id)})
        return user.get("user_type", default)

    async def get_all_premium_users(self):
        all_premium_users = self.col.find({"user_type.is_premium": True})
        return all_premium_users


db = Database(Config.DB_URL, Config.BOT_USERNAME)
