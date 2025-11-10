# 🚀 Smart Test Automation Dashboard

A full-stack web application for automated UI testing with real-time reporting and CI/CD pipeline.

![CI/CD Status](https://github.com/YOUR_USERNAME/smart-test-automation-dashboard/actions/workflows/ci-cd.yml/badge.svg)

## ✨ Features

- **🔍 Automated Testing**: Browser automation with Playwright
- **📊 Real-time Dashboard**: Live test results with interactive charts
- **🔄 CI/CD Pipeline**: Automated testing on every commit
- **💾 Data Persistence**: SQL database for test history
- **🎯 Multi-Website Testing**: Google, Wikipedia, E-commerce demo
- **🐳 Docker Ready**: Containerized deployment

## 🛠️ Tech Stack

- **Backend**: Python, Flask, SQLAlchemy
- **Frontend**: HTML5, CSS3, JavaScript, Chart.js
- **Testing**: Playwright, Pytest
- **Database**: SQLite/PostgreSQL
- **CI/CD**: GitHub Actions
- **Container**: Docker

## 🚀 Quick Start

### Local Development
```bash
# 1. Clone repository
git clone https://github.com/YOUR_USERNAME/smart-test-automation-dashboard.git
cd smart-test-automation-dashboard

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt
playwright install chromium

# 4. Initialize database
python -c "from app import create_app, db; app = create_app(); app.app_context().push(); db.create_all()"

# 5. Run application
python run.py

# 6. Open http://localhost:5000
