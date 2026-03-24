# 🚀 ResolveIT AI — Smart IT Helpdesk Platform

🚧 Status: MVP (Startup-Grade Prototype)

An AI-powered IT Service Management (ITSM) platform designed to automate IT support operations inside companies.

Inspired by tools like HaloITSM, Zendesk, and Jira Service Management.

---

## ✨ Key Features

### 🤖 AI Ticket Classification
- Automatically detects issue category
- Predicts priority (Low / Medium / High)
- Provides confidence score

### ⚙️ Event-Driven Architecture
- Queue-based processing system
- Background worker execution
- Scalable backend design

### 📊 Admin Dashboard
- Live ticket monitoring
- Queue size tracking
- Worker status
- Priority distribution charts
- Real-time updates

### 👨‍💻 Client Portal
- Submit IT issues
- Instant AI classification
- Auto priority detection
- Success confirmation UI

---

## 🧠 Tech Stack

| Layer        | Technology |
|-------------|------------|
| Backend     | Python |
| Server      | HTTPServer |
| Database    | SQLite |
| Queue       | Python Queue |
| AI Model    | Rule-based (ML-ready) |
| Frontend    | HTML, CSS, Chart.js |

---

## 🏗 System Architecture


Client Portal
↓
API Layer
↓
AI Classification
↓
Queue System
↓
Worker Processing
↓
Database
↓
Admin Dashboard


---

## 🚀 How to Run

```bash
git clone https://github.com/thakursahab2580-lgtm/ai-helpdesk-system.git
cd ai-helpdesk-system
python ticket_system.py
🌐 Access
Client Portal

http://127.0.0.1:8000/portal

Admin Panel

http://127.0.0.1:8000/admin

🔐 Admin Credentials

ID: admin
Password: admin123

📸 Screenshots

Make sure you have this folder structure:

assets/
├── dashboard.png
├── portal.png
Dashboard

Client Portal

🔮 Future Improvements
FastAPI backend
React frontend (modern SaaS UI)
PostgreSQL database
Redis queue (Celery workers)
Machine Learning model (TF-IDF + Naive Bayes)
Authentication system (JWT)
Ticket assignment system
SLA tracking
Notification system (Email / Slack)
💡 Why This Project?

This project demonstrates:

Real-world system architecture
Event-driven backend design
AI integration in IT operations
Scalable helpdesk system design
👨‍💻 Author

Yuvraj Singh
MSC in AI | AI + SaaS Builder