from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(80), unique=True, index=True, nullable=False)
    email = Column(String(255), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    xp = Column(Integer, default=0, nullable=False)
    rank = Column(String(50), default="Novice", nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    attempts = relationship("Attempt", back_populates="user", cascade="all, delete-orphan")
    friends = relationship("Friend", back_populates="user", cascade="all, delete-orphan")
    downloads = relationship("Download", back_populates="user", cascade="all, delete-orphan")
    leaderboard_entry = relationship(
        "Leaderboard", back_populates="user", uselist=False, cascade="all, delete-orphan"
    )
    analytics_events = relationship(
        "Analytics", back_populates="user", cascade="all, delete-orphan"
    )

class Lab(Base):
    __tablename__ = "labs"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(120), index=True, nullable=False)
    difficulty = Column(String(20), nullable=False)
    status = Column(String(20), nullable=False)
    icon = Column(String(255), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    attempts = relationship("Attempt", back_populates="lab", cascade="all, delete-orphan")

class Attempt(Base):
    __tablename__ = "attempts"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    lab_id = Column(Integer, ForeignKey("labs.id"), nullable=False, index=True)
    attempt_result = Column(String(30), nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow, nullable=False)

    user = relationship("User", back_populates="attempts")
    lab = relationship("Lab", back_populates="attempts")

class Friend(Base):
    __tablename__ = "friends"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    friend_username = Column(String(80), nullable=False)
    status = Column(String(20), default="offline", nullable=False)
    last_seen = Column(DateTime, default=datetime.utcnow, nullable=False)

    user = relationship("User", back_populates="friends")

class Download(Base):
    __tablename__ = "downloads"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    file_name = Column(String(255), nullable=False)
    progress = Column(Integer, default=0, nullable=False)
    time_remaining = Column(String(40), nullable=False)

    user = relationship("User", back_populates="downloads")

class Leaderboard(Base):
    __tablename__ = "leaderboard"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, unique=True, index=True)
    xp = Column(Integer, default=0, nullable=False)
    rank_position = Column(Integer, default=0, nullable=False)

    user = relationship("User", back_populates="leaderboard_entry")

class Analytics(Base):
    __tablename__ = "analytics"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    xp_gained = Column(Integer, default=0, nullable=False)
    missions_completed = Column(Integer, default=0, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow, nullable=False)

    user = relationship("User", back_populates="analytics_events")
