# 🤖 Telegram Bot Template
**Python · Aiogram 3 · FastAPI · PostgreSQL · Redis · Docker**

قالب احترافي لبناء بوتات تيليغرام متكاملة في الإنتاج.

---

## 🗂️ هيكل المشروع

```
telegram-bot-template/
│
├── main.py                   # نقطة الدخول (polling أو webhook)
│
├── core/
│   ├── config.py             # إعدادات المشروع (pydantic-settings)
│   └── lifespan.py           # إدارة DB و Redis (startup/shutdown)
│
├── bot/
│   ├── handlers/             # معالجات الأوامر والرسائل
│   │   ├── __init__.py       # تسجيل جميع الـ routers
│   │   ├── start.py          # /start
│   │   ├── help.py           # /help
│   │   ├── echo.py           # ردود الفعل على الرسائل العادية
│   │   └── errors.py         # معالج الأخطاء العام
│   │
│   ├── middlewares/
│   │   ├── throttling.py     # حد معدل الطلبات عبر Redis
│   │   └── logging.py        # تسجيل كل طلب ووقت الاستجابة
│   │
│   ├── keyboards/
│   │   └── main_menu.py      # لوحات المفاتيح (Reply + Inline)
│   │
│   └── filters/
│       └── admin.py          # فلتر المشرفين
│
├── api/
│   ├── app.py                # FastAPI factory + webhook endpoint
│   └── routers/
│       ├── health.py         # GET /api/health
│       └── stats.py          # GET /api/stats
│
├── db/
│   ├── models/
│   │   └── user.py           # SQLAlchemy User model
│   └── repositories/
│       └── user_repo.py      # User CRUD operations
│
├── requirements.txt
├── .env.example
├── Dockerfile
├── docker-compose.yml
└── alembic.ini
```

---

## 🚀 البدء السريع

### 1. استنساخ وإعداد البيئة
```bash
git clone <your-repo>
cd telegram-bot-template
cp .env.example .env
# عدّل .env وأضف BOT_TOKEN الخاص بك
```

### 2. تشغيل محلي (Polling — للتطوير)
```bash
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
python main.py
```

### 3. تشغيل بـ Docker
```bash
docker compose up --build
```

### 4. تهجير قاعدة البيانات
```bash
alembic revision --autogenerate -m "initial"
alembic upgrade head
```

---

## ⚙️ متغيرات البيئة الرئيسية

| المتغير | الوصف | القيمة الافتراضية |
|---|---|---|
| `BOT_TOKEN` | توكن البوت من @BotFather | **مطلوب** |
| `USE_WEBHOOK` | webhook للإنتاج، polling للتطوير | `false` |
| `DATABASE_URL` | رابط PostgreSQL | `postgresql+asyncpg://...` |
| `REDIS_URL` | رابط Redis | `redis://localhost:6379/0` |
| `BOT_ADMIN_IDS` | قائمة Telegram IDs للمشرفين | `[]` |

---

## 🔌 نقاط API

| Method | Endpoint | الوصف |
|---|---|---|
| `POST` | `/webhook` | استقبال تحديثات تيليغرام |
| `GET` | `/api/health` | فحص حالة الخدمات |
| `GET` | `/api/stats` | إحصائيات المستخدمين |

---

## 🧩 إضافة Handler جديد

```python
# bot/handlers/myfeature.py
from aiogram import Router, F
from aiogram.types import Message

router = Router(name="myfeature")

@router.message(F.text == "🆕 ميزة جديدة")
async def my_feature(message: Message) -> None:
    await message.answer("هذه ميزة جديدة!")
```

ثم سجّله في `bot/handlers/__init__.py`:
```python
from bot.handlers.myfeature import router as myfeature_router

def setup_routers(dp):
    dp.include_router(myfeature_router)
    ...
```

---

## 📦 التقنيات المستخدمة

- **[Aiogram 3](https://docs.aiogram.dev/)** — أطار بوت تيليغرام غير متزامن
- **[FastAPI](https://fastapi.tiangolo.com/)** — API سريع للـ webhook والـ admin API
- **[SQLAlchemy 2 (async)](https://docs.sqlalchemy.org/)** — ORM لـ PostgreSQL
- **[Redis](https://redis.io/)** — التخزين المؤقت وحد معدل الطلبات
- **[Pydantic Settings](https://docs.pydantic.dev/)** — إدارة إعدادات آمنة
- **[Alembic](https://alembic.sqlalchemy.org/)** — تهجيرات قاعدة البيانات
- **[Docker](https://docs.docker.com/)** — حاويات للنشر

---

## 📄 License
MIT
