from datetime import datetime
from fastapi import FastAPI, Request, Form
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
# SessionLocal はDBとのやり取りする窓口
from database import init_db, SessionLocal
from sqlalchemy import func, and_
# Logsはlogsテーブルのクラス
from models import Logs, Schedule
from fastapi.templating import Jinja2Templates
import os

BASE_DIR=os.path.dirname(os.path.abspath(__file__))

app = FastAPI()

app.mount("/movie", StaticFiles(directory=os.path.join(BASE_DIR, "..", "movie")), name="movie")  # /staticというURLでstaticフォルダを公開する

# templatesフォルダを使います
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "template"))

@app.get("/")
def index(request: Request):

    now = datetime.now().time()  # 今の時間を取ってくる
    now_str = now.strftime("%H:%M:%S")  # 今の時間を文字列に変換

    today = datetime.now().date()  # 今日の日付を取ってくる
    today_str = today.strftime("%Y年%m月%d日")  # 今日の日付を文字列に変換



    db = SessionLocal()

    try:
        logs = db.query(Logs).filter(
            func.date(Logs.time_given) == today
        )  # Logsテーブルから今日のログを取ってくる
    # サブクエリ：各time_of_dayの最新時刻
        subq = (
            db.query(
                Logs.time_of_day,
                # Logsテーブルからtime_of_dayとtime_givenの最大値(最新時刻)を取ってくる
                func.max(Logs.time_given).label("max_time")
            )
            # Logsテーブルからmorning, afternoon, eveningのログを取ってくる
            .filter(Logs.time_of_day.in_(["morning", "afternoon", "evening"]))
            # 区分ごとにまとめる
            .group_by(Logs.time_of_day)
            # サブクエリとして使うためにsubqという名前をつける
            .subquery()
        )

        # メインクエリ：一致するログを取得
        latest_logs = (
            db.query(Logs)
            # JoinでサブクエリとLogsテーブルを結合する
            .join(
                subq,
                and_(
                    Logs.time_of_day == subq.c.time_of_day,
                    Logs.time_given == subq.c.max_time
                )
            )
            # 結果をリストで受け取る
            .all()
        )

        schedule = db.query(Schedule).all()  # Scheduleテーブルから全ての行を取ってくる

        fed_log = db.query(Logs).filter(
            func.date(Logs.time_given) == today
        ).all()

        fed = [fed_log.time_of_day for fed_log in fed_log]  # fed_logからtime_of_dayだけを抜き取る

        # 第一引数はテンプレートファイルの名前、第二引数はテンプレートに渡す変数を辞書形式で指定
        return templates.TemplateResponse(
            # index.htmlに返す
            "index.html", {
                "request": request, "schedule": schedule, "now": now, "logs": logs, "fed": fed,
                "today_str": today_str, "now_str": now_str, "latest_logs": latest_logs
                }
            )  # index.htmlにrequestとscheduleを渡す
    finally:
        db.close()  # DBのセッションを閉じる

# 初期化
@app.on_event("startup")
def startup():
    init_db()

@app.post("/feed")
def feed(time_of_day: str = Form()):
    db = SessionLocal()     # DBのセッションを開く
    log = Logs(time_of_day=time_of_day)  # Logsクラスのインスタンスを作る
    db.add(log)           # DBに追加
    db.commit()           # DBに変更を保存
    db.close()            # DBのセッションを閉じる
    return RedirectResponse(url="/", status_code=303)

@app.get("/time")
async def get_time():
    now = datetime.now().time()  # 今の時間を取ってくる
    now_countinue = now.strftime("%H:%M:%S")  # 今の時間を文字列に変換
    return {"time": now_countinue}

# 各時間帯の最新の給餌時刻を返す（フロントのリアルタイム表示用）
@app.get("/feed-time")
def get_feed_time():
    db = SessionLocal()
    try:
        # サブクエリ：各time_of_dayの最新時刻を取得
        subq = (
            db.query(
                Logs.time_of_day,
                func.max(Logs.time_given).label("max_time")
            )
            .filter(Logs.time_of_day.in_(["morning", "afternoon", "evening"]))
            .group_by(Logs.time_of_day)
            .subquery()
        )

        # メインクエリ：最新時刻と一致するログを取得
        latest_logs = (
            db.query(Logs)
            .join(
                subq,
                and_(
                    Logs.time_of_day == subq.c.time_of_day,
                    Logs.time_given == subq.c.max_time
                )
            )
            .all()
        )

        return {
            "logs": [
                {
                    "time_of_day": log.time_of_day,
                    "time": log.time_given.strftime("%H:%M")
                }
                for log in latest_logs
            ]
        }
    finally:
        db.close()

# 指定した時間帯の今日の給餌ログをすべて削除する（キャンセル機能）
@app.post("/cancel_feed")
def cancel_feed(time_of_day: str = Form(...)):
    db = SessionLocal()
    today = datetime.now().date()

    # 今日の、指定された時間帯（morningなど）のログをすべて削除する
    db.query(Logs).filter(
        func.date(Logs.time_given) == today,
        Logs.time_of_day == time_of_day
    ).delete(synchronize_session=False)

    db.commit()
    db.close()

    # 削除が終わったらトップページに戻る
    return RedirectResponse(url="/", status_code=303)
