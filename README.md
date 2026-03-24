# 🚀 ResolveIT AI — Smart IT Helpdesk Platform

🚧 **Status:** MVP (Startup-Grade Prototype)

ResolveIT AI is an AI-powered IT Service Management (ITSM) platform designed to automate internal IT support operations.

Inspired by tools like **HaloITSM, Zendesk, and Jira Service Management**.

---

## ✨ Key Features

### 🤖 AI Ticket Classification

* Automatic issue categorization
* Priority prediction (Low / Medium / High)
* Confidence scoring system

### ⚙️ Event-Driven Architecture

* Queue-based processing
* Background worker execution
* Async-ready scalable design

### 📊 Admin Dashboard

* Live ticket monitoring
* Queue size tracking
* Worker status visibility
* Priority distribution charts

### 👨‍💻 Client Portal

* Submit IT issues
* Instant AI classification
* Auto-priority detection
* Ticket confirmation with ID

---

## 🧠 Tech Stack

| Layer    | Technology            |
| -------- | --------------------- |
| Backend  | Python                |
| Server   | HTTPServer            |
| Database | SQLite                |
| Queue    | Python Queue          |
| AI Model | Rule-based (ML-ready) |
| Frontend | HTML, CSS, Chart.js   |

---

## 🏗 System Architecture

```text
Client Portal
     ↓
API Layer
     ↓
AI Classification
     ↓
Queue System
     ↓
Worker Engine
     ↓
Database
     ↓
Admin Dashboard
```

---

## 🚀 How to Run

```bash
git clone https://github.com/thakursahab2580-lgtm/ai-helpdesk-system.git
cd ai-helpdesk-system
python main.py
```

---

## 📸 Screenshots

### 📊 Dashboard

![Dashboard](./assets/dashboard.png)

### 👨‍💻 Client Portal

![Client Portal](./assets/portal.png)

---

## 🔥 Roadmap

* [ ] FastAPI migration
* [ ] PostgreSQL integration
* [ ] Authentication system (Admin / Agent / User)
* [ ] Ticket lifecycle management
* [ ] ML-based classification model
* [ ] SaaS-grade UI (React + Tailwind)
* [ ] Notifications & SLA tracking

---

## 💡 Vision

To build a **production-ready AI Helpdesk platform** that reduces manual IT workload and improves response efficiency using intelligent automation.

---

## 👨‍💻 Author

**Yuvraj Singh**
BCA Graduate | AI + SaaS Builder

---

## ⭐ Support

If you like this project, consider giving it a ⭐ on GitHub!
