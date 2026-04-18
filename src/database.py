import time
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, Schedule
from datetime import time

# app.dbをSQLiteファイルに接続するエンジンを作成
engine = create_engine("sqlite:///./app.db")    # ///はこのディレクトリに作成

# さっきのengineを使ってDBとやり取りするセッションを作成
SessionLocal = sessionmaker(bind=engine)


def init_db():
    Base.metadata.create_all(bind=engine)   # どのエンジンを使うかを指定
    db = SessionLocal()     # DBのセッションを開く
    try:
        if db.query(Schedule).count() == 0:  # Scheduleテーブルにデータがなければ
            schedule =  Schedule(time_of_day="morning", available_from=time(6, 0))  # Scheduleクラスのインスタンスを作る
            db.add(schedule)       # DBに追加
            schedule2 = Schedule(time_of_day="afternoon", available_from=time(12, 0))
            db.add(schedule2)
            schedule3 = Schedule(time_of_day="evening", available_from=time(18, 0))
            db.add(schedule3)
            db.commit()           # DBに変更を保存
            db.close()            # DBのセッションを閉じる
    finally:
        db.close()            # DBのセッションを閉じる
