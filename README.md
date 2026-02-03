[![lang ru](https://img.shields.io/badge/lang-ru-blue)]
[![lang en](https://img.shields.io/badge/lang-en-red)]

# Collector
**Collector** is a full-stack application for managing your personal collection of movies, TV series, and books.  
The project includes user authentication, search, filters, statuses, pagination, and a dark/light theme.

---

## Tech Stack
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
- User registration and login  
- JWT-based authentication  
- Search by title  
- Filters by category and status  
- Pagination  
- Change item status (watched / reading / planned, etc.)  
- Delete items  
- Modal with detailed information  
- Dark / Light theme

---

## Project Structure
```bash
collector/
├── backend/ # FastAPI backend
├── frontend/ # React + Vite frontend
└── README.md

```
---

## 🐳 Docker Usage (recommended)

**1. Build the image**
```bash
docker compose up --build
```
**2. Open in browser**
```bash
http://localhost:3000/
```

---

## 🤝 Contributing

PRs are welcome!
Feel free to add new sources or improve code structure.

---

## 📄 License

MIT — free for all use.