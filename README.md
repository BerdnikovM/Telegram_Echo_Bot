# ⚡ Echo-Bot (aiogram 3 + Docker)

> **Telegram-бот “Эхо”**: принимает текст, фото, файлы ≤ 10 МБ — и мгновенно отправляет их обратно.  
> Проект демонстрирует чистую асинхронную архитектуру, работу с множеством типов сообщений и грамотный DevOps-пайплайн.

<p align="center">
  <img src="docs/example1.gif" width="720">
  <img src="docs/example2.gif" width="720">
</p>

[![Docker Pulls](https://img.shields.io/docker/pulls/mihailberd/telegram_echo_bot)](https://hub.docker.com/r/mihailberd/telegram_echo_bot)
[![Deploy to Render](https://img.shields.io/badge/Render-Deploy-blue?logo=render)](https://render.com/deploy?repo=https://github.com/BerdnikovM/Telegram_Echo_Bot)
[![License](https://img.shields.io/github/license/BerdnikovM/Telegram_Echo_Bot)](LICENSE)

---

## ✨ Ключевые фичи

| Фича | Что показывает |
|------|----------------|
| **aiogram 3 + Router** | Современная асинхронная обработка апдейтов |
| **Поддержка 8 типов сообщений** | Текст, фото, стикер, видео, GIF, документ, аудио, голос |
| **Ролевое ограничение /users** | Базовая RBAC-проверка (админы только из `config.py`) |
| **Persist пользователей** | Автоматически логирует `user_id` в файл |
| **Ограничение размера 10 МБ** | Пример middle-layer валидации входящих файлов |
| **Dockerfile 9 строк** | Сборка лёгкого образа (Python 3.12-slim) |
| **ENV-секреты (BOT_TOKEN)** | Безопасное управление токенами / CI-секретами |

---

## 🚀 Быстрый старт

> Требования: Docker 20.10+, токен Telegram-бота.

```bash
# 1. Забираем образ
docker pull mihailberd/telegram_echo_bot:latest

# 2. Запускаем
docker run --rm -e BOT_TOKEN=YOUR_TOKEN mihailberd/telegram_echo_bot:latest
```
## Локальная сборка
```
git clone https://github.com/BerdnikovM/Telegram_Echo_Bot.git
cd echo-bot
pip install -r requirements.txt   # aiogram 3.21+
export BOT_TOKEN=
python bot.py
```

---

## 🛠️ Стек и техники

| Слой               | Технологии                                                          |
| ------------------ | ------------------------------------------------------------------- |
| 🐍 Язык            | **Python 3.12**                                                     |
| 🤖 Telegram SDK    | **aiogram 3** (Router, Filters, FSM)                                |
| 🐋 Контейнеризация | **Docker** + официальный образ `python:3.12-slim`                   |
| 🔐 Secrets         | ENV-переменные (`BOT_TOKEN`), поддержка `.env` |
| 📈 Логирование     | `logging.basicConfig(level=INFO)`                                   |
| 🧪 Тесты (roadmap) | `pytest-asyncio`, GitHub Actions CI                                 |
| ☁️ Деплой          | Render (free tier) / Docker Hub image                               |

---
## 🤝 Связаться

|            | Контакт                                                                  |
| ---------- |--------------------------------------------------------------------------|
| ✉ Telegram | [@MihailBerd](https://t.me/MihailBerd)                                 |
| 💼 Kwork   | [https://kwork.ru/user/berdnikovmiha) |
| 📧 Email   | [MihailBerdWork@ya.ru](mailto:MihailBerdWork@ya.ru)                                |

