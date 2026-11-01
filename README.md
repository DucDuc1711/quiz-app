# 🎯 Hệ Thống Quiz Trực Tuyến (Online Quiz System)

Dự án Quiz trực tuyến theo kiến trúc tách đôi:
- **Frontend**: Vue 3 (Composition API, `<script setup>`) + Vite + Vue Router + Pinia + Bootstrap 5
- **Backend**: Python 3.10+ + Flask + Flask-SQLAlchemy + Flask-Migrate + Flask-JWT-Extended + Flask-CORS + SQLite

---

## 📁 Cấu trúc thư mục

```text
quiz-app/
├── backend/
│   ├── app/
│   ├── instance/
│   ├── migrations/
│   ├── run.py
│   ├── requirements.txt
│   ├── .env
│   └── .env.example
├── frontend/
│   ├── src/
│   ├── index.html
│   ├── package.json
│   └── vite.config.js
├── .gitignore
└── README.md
```

## 🚀 Cách chạy dự án

### 1. Backend (cổng 5000)

```powershell
cd quiz-app/backend
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
copy .env.example .env
$env:FLASK_APP="run.py"
python -m flask seed
python run.py
```

Backend chạy tại: `http://localhost:5000`

**Tài khoản admin mặc định:** Username: `admin` / Password: `123456`

### 2. Frontend (cổng 5173)

```powershell
cd quiz-app/frontend
npm install
npm run dev
```

Frontend chạy tại: `http://localhost:5173`


---

## 🔌 Các API chính

### Auth
| Method | Endpoint | Mô tả |
|--------|----------|-------|
| POST | `/api/auth/register` | Đăng ký |
| POST | `/api/auth/login` | Đăng nhập |
| GET | `/api/auth/me` | Thông tin user hiện tại (cần JWT) |

### Quiz (Người chơi)
| Method | Endpoint | Mô tả |
|--------|----------|-------|
| GET | `/api/quizzes` | Danh sách quiz |
| GET | `/api/quizzes/<id>` | Chi tiết quiz + câu hỏi (không có đáp án đúng) |
| POST | `/api/quizzes/<id>/submit` | Nộp bài, chấm điểm |
| GET | `/api/quizzes/<id>/leaderboard` | Top 10 bảng xếp hạng |
| GET | `/api/me/attempts` | Lịch sử làm bài cá nhân |
| GET | `/api/attempts/<id>` | Chi tiết một lần làm bài |

### Admin (yêu cầu role admin)
| Method | Endpoint | Mô tả |
|--------|----------|-------|
| GET/POST | `/api/admin/quizzes` | Danh sách / Tạo quiz |
| GET/PUT/DELETE | `/api/admin/quizzes/<id>` | Chi tiết / Sửa / Xóa quiz |
| POST | `/api/admin/quizzes/<id>/questions` | Thêm câu hỏi |
| PUT/DELETE | `/api/admin/questions/<id>` | Sửa / Xóa câu hỏi |
| GET | `/api/admin/stats` | Thống kê tổng quan |
