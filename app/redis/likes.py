from typing import  List
from redis import Redis


class PostLikes:

    likes_amount: int
    dislikes_amount: int
    likes: List[int]
    dislikes: List[int]

    def __init__(self, post_likes: dict):
        self.likes = []
        self.dislikes = []
        
        for user_id, like in post_likes.items():
            if like == "True".encode():
                self.likes.append(user_id)
            else:
                self.dislikes.append(user_id)
        
        self.likes_amount = len(self.likes)
        self.dislikes_amount = len(self.dislikes)


class Likes:

    @staticmethod
    async def new_like(post_id: int, user_id: int, like: bool, db:Redis):
        post_id = str(post_id).encode()
        user_id = str(user_id).encode()
        like = str(like).encode()
        
        post_likes= await db.hgetall(name=post_id)

        if post_likes.get(user_id) == like:
            await db.hdel(post_id, user_id)
        else:
            await db.hset(post_id, user_id, like)


    @staticmethod
    async def get_post_likes(post_id: str, db:Redis):
        post_likes = await db.hgetall(name=post_id)
        return PostLikes(post_likes=post_likes)


    @staticmethod
    async def delete_post_likes(post_id: str, db:Redis):
        await db.delete(post_id)
