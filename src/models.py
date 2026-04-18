# SQLAlchemyのインポート
from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String, Time, DateTime
from datetime import datetime

# テーブルを定義する時の設計図の土台を定義
Base = declarative_base()

class Schedule(Base):       # Baseを継承してテーブルを定義
    __tablename__ = "schedules"     # 実際のテーブル名
    id = Column(Integer, primary_key=True)
    time_of_day = Column(String)
    available_from = Column(Time)

class Logs(Base):
    __tablename__ = "logs"
    id = Column(Integer, primary_key=True)
    time_of_day = Column(String)
    time_given = Column(DateTime, default=datetime.now)
