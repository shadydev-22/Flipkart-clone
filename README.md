# Flipkart Clone

A full-stack e-commerce application inspired by Flipkart, featuring a React frontend and a FastAPI backend.

## 🚀 Live Deployment
- **Frontend**: [Netlify (astounding-ganache-26c4c5)](https://astounding-ganache-26c4c5.netlify.app)
- **Backend/API**: [Render (flipkart-clone-tk4m)](https://flipkart-clone-tk4m.onrender.com)

## 🛠 Tech Stack
- **Frontend**: React (Vite), Axios, React Router
- **Backend**: FastAPI (Python), SQLAlchemy ORM
- **Database**: PostgreSQL (Managed by Render)
- **Deployment**: Netlify (Frontend) & Render (Backend + Database)

## 🌍 Cloud Architecture
This project is architected for seamless cross-platform communication:
1.  **Frontend (Netlify)**: Deployed as a Single Page Application (SPA). Uses `_redirects` for clean routing and the `VITE_API_URL` environment variable to securely connect to the backend.
2.  **Backend (Render)**: FastAPI server with automatic CORS configuration to allow secure requests from the Netlify domain.
3.  **Database**: Hosted on Render PostgreSQL, connected via a secure `DATABASE_URL`.

### **Self-Healing Mechanism**
To bridge the gap between local development and cloud deployment, I implemented a custom "Self-Healing" logic:
- **Auto-Schema Generation**: On every server startup, the backend automatically detects and creates any missing database tables.
- **Remote Seeding**: A specialized `POST /api/admin/seed` endpoint allows you to populate the cloud database with initial product and category data via a simple `curl` command, without needing manual database access.

## 💻 Local Setup
1. **Clone & Install**: `npm install` (Root) and `pip install -r requirements.txt` (Backend folder).
2. **Environment**: Setup `.env` with your `DATABASE_URL` and `VITE_API_URL`.
3. **Launch**:
   - **Backend**: `python backend/main.py` (Default: port 8000)
   - **Frontend**: `npm run dev` (Default: port 3000)

## 📡 Essential API
- `GET /api/products` - Search and list products
- `GET /api/categories` - Fetch all categories
- `POST /api/admin/seed` - Populate production database

---
*Created for educational purposes.*