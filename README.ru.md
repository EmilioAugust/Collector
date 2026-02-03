[![lang en](https://img.shields.io/badge/lang-en-red)](https://github.com/EmilioAugust/Collector/blob/main/README.md)
[![lang ru](https://img.shields.io/badge/lang-ru-blue)](https://github.com/EmilioAugust/Collector/blob/main/README.ru.md)

# Collector
**Collector** Это полнофункциональное приложение для управления вашей личной коллекцией фильмов, сериалов и книг.
Проект включает в себя аутентификацию пользователей, поиск, фильтры, статусы, пагинацию и темную/светлую тему оформления.

---

## Стек технологий
### Frontend
- React
- Vite
- JavaScript (ES6+)
- CSS
- Fetch API

### Backend
- Python
- FastAPI
- JWT Authentication
- REST API

---

## Features
- Регистрация и вход пользователя
- Аутентификация на основе JWT
- Поиск по названию
- Фильтры по категории и статусу
- Пагинация
- Изменение статуса элемента (просмотрено / прочитано / запланированный и т.д.)
- Удаление элементов
- Модальное окно с подробной информацией
- Темная/светлая тема

---

## Структура проекта
```bash
collector/
├── backend/ # FastAPI backend
├── frontend/ # React frontend
└── README.md

```
---

## Запуск через Docker (рекомендовано)

**1. Собрать образ**
```bash
docker compose up --build
```
**2. Открыть в браузере**
```bash
http://localhost:3000/
```

---

## Вклад

PR приветствуются!
Вы можете добавить новые источники, улучшить структуру или предложить новые функции.

---

## Лицензия

MIT — можно использовать в любом проекте.
