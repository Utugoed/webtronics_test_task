from databases import Database

from app.db.models import posts


class Posts:
    
    @staticmethod
    async def create_post(post_data: dict, db: Database):
        new_post = {
            "title": post_data["title"],
            "content": post_data["content"],
            "created_at": post_data["created_at"],
            "owner_id": post_data["owner_id"]
        }
        
        query = posts.insert()
        await db.execute(query=query, values=new_post)


    @staticmethod
    async def get_user_posts(owner_id: int, db: Database):
        query = posts.select().where(posts.c.owner_id == owner_id)
        posts_list = await db.fetch_all(query=query)
        return posts_list


    @staticmethod
    async def get_post(post_id: int, db: Database):
        query = posts.select().where(posts.c.id == post_id)
        post = await db.fetch_one(query=query)
        return post


    @staticmethod
    async def update_post(post_id: int, new_data: dict, db: Database):
        query = posts.update().where(posts.c.id == post_id).values(**new_data)
        await db.execute(query=query)


    @staticmethod
    async def delete_post(post_id: int, db: Database):
        query = posts.delete().where(posts.c.id == post_id)
        await db.execute(query=query)
