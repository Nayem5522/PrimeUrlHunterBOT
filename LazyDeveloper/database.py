

import datetime
import motor.motor_asyncio
from configs import Config


class Database:

    def __init__(self, uri, database_name):
        self._client = motor.motor_asyncio.AsyncIOMotorClient(uri)
        self.db = self._client[database_name]
        self.col = self.db.users

    def new_user(self, user_id):
        return dict(
            id=user_id,
            join_date=datetime.date.today().isoformat(),
            ban_status=dict(
                is_banned=False,
                ban_duration=0,
                banned_on=datetime.date.max.isoformat(),
                ban_reason=""
            )
        )

    async def add_user(self, user_id):
        user = self.new_user(user_id)
        await self.col.insert_one(user)

    async def is_user_exist(self, user_id):
        user = await self.col.find_one({"id": int(user_id)})
        return True if user else False

    async def total_users_count(self):
        return await self.col.count_documents({})

    async def get_all_users(self):
        users = await self.col.find({}, {"id": 1}).to_list(None)
        return [user["id"] for user in users]

    async def delete_user(self, user_id):
        await self.col.delete_one({"id": int(user_id)})

    async def remove_ban(self, user_id):
        await self.col.update_one(
            {"id": int(user_id)}, {"$set": {"ban_status.is_banned": False}}
        )

    async def ban_user(self, user_id, ban_duration, ban_reason):
        ban_status = dict(
            is_banned=True,
            ban_duration=ban_duration,
            banned_on=datetime.date.today().isoformat(),
            ban_reason=ban_reason,
        )
        await self.col.update_one({"id": user_id}, {"$set": {"ban_status": ban_status}})

    async def get_ban_status(self, user_id):
        user = await self.col.find_one({"id": int(user_id)})
        return user.get("ban_status", {}) if user else {}

    async def get_all_banned_users(self):
        return self.col.find({"ban_status.is_banned": True})


db = Database(Config.DATABASE_URL, Config.BOT_USERNAME)
