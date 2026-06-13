# MARUINO - 猫の給餌管理アプリ

<<<<<<< HEAD
これはyumaとnororiの共同プロジェクトです．
またの名をMARUINOといいます．
これは私の飼っている猫の頭文字から取得しました．
- MARU
- RUI
- NONO
=======
domaとnororiの共同プロジェクトです。\
3匹の猫の頭文字から **MARUINO** と名付けました。

- **MARU**
- **RUI**
- **NONO**
>>>>>>> d216c08 (README.md修正)

## Features

- 朝・昼・夜の給餌をワンクリックで記録
- 給餌時刻をリアルタイムで画面に表示
- 時間帯が来るまでボタンをグレーアウト（誤操作防止）
- 給餌記録をキャンセルする機能
- 家族全員でブラウザから給餌状況を共有

## Tech Stack

| カテゴリ | 技術 |
|--------|------|
| Backend | FastAPI / uvicorn |
| ORM | SQLAlchemy |
| DB | SQLite |
| Template | Jinja2 |

## Setup

```bash
git clone https://github.com/yuma-yuma-222/Cat-feeding-manager.git
cd Cat-feeding-manager
pip install -r requirements.txt
```

## Usage

```bash
cd src
uvicorn main:app --reload
```

ブラウザで `http://localhost:8000` にアクセス。

## API Endpoints

| Method | Path | 説明 |
|--------|------|------|
| GET | `/` | トップページ（給餌ボタン一覧） |
| POST | `/feed` | 給餌を記録する |
| POST | `/cancel_feed` | 今日の給餌記録を取り消す |
| GET | `/time` | 現在時刻を返す（リアルタイム表示用） |
| GET | `/feed-time` | 各時間帯の最新給餌時刻を返す |

## Project Structure

```
maruino/
├── src/
│   ├── main.py        # FastAPIアプリ本体
│   ├── models.py      # DBモデル (Logs, Schedule)
│   ├── database.py    # DB初期化・セッション管理
│   ├── app.db         # SQLiteデータベース
│   └── template/
│       └── index.html # フロントエンド
├── images/            # 猫の写真
├── movie/             # 動画ファイル
└── requirements.txt
```

## My Cats

↓ maru\
![maru](images/maru.jpg)

↓ rui\
![rui](images/rui.jpg)

↓ nono\
![nono](images/nono.jpg)
