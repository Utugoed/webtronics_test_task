from sqlalchemy import (
    Column, DateTime, ForeignKey, Integer, String, Text, Table
)

from app.db import metadata


users = Table(
    "users",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("username", String, unique=True),
    Column("hashed_password", String)
)

posts = Table(
    "posts",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("title", String),
    Column("content", Text),
    Column("created_at", DateTime),
    Column("owner_id", ForeignKey("users.id"))
)
