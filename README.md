# AutoService Pro 2026: Enterprise Edition

## Overview
AutoService Pro 2026 represents the pinnacle of automotive service management systems. Rebuilt from the ground up for the 2026 diploma defense, this project combines a futuristic "Solar 2026" visual identity with a robust, enterprise-grade Django backend.

## 🚀 Key Features
- **Solar 2026 Vision Design**: A cutting-edge UI featuring Deep Blue glassmorphism, Solar Orange highlights, and Bento-grid layouts.
- **Neural Price Engine (AI Calculator)**: Real-time cost estimation using HTMX with age and mileage-based smart multipliers.
- **Enterprise Booking Engine**: Interactive scheduling powered by FullCalendar 6 with automated mechanic assignment logic.
- **Multi-Role Ecosystem**: Tailored experiences for Clients (Garage & History), Managers (ApexCharts Analytics), and Mechanics (Real-time Terminal).
- **Pro Reporting**: High-precision print-ready invoices and analytics exports.
- **Zero-Error Architecture**: Strictly follows Django 5.1 best practices with a clean, modular structure.

## 🛠 Setup & Run
1. **Clone & Environment**:
   ```powershell
   cd c:\Users\Bosco\Desktop\диплом\auto_service
   ..\venv\Scripts\python.exe -m pip install -r ..\requirements.txt
   ```

2. **Database & Seeding**:
   ```powershell
   ..\venv\Scripts\python.exe manage.py migrate
   ..\venv\Scripts\python.exe seed_massive.py
   ```

3. **Start Server**:
   ```powershell
   ..\venv\Scripts\python.exe manage.py runserver
   ```

## 👥 Demo Credentials

| Role | Email | Password |
|------|-------|----------|
| Manager | manager@gmail.com | admin123 |
| Client | client@gmail.com | pass123 |

## 💎 Design Philosophy
- **Primary Color**: `#0A2540` (Deep Space Navy)
- **Accent Color**: `#FF6B00` (Solar Flare Orange)
- **Typography**: Orbitron (Headlines) & Plus Jakarta Sans (UI)
- **Frameworks**: Django 5.1, Tailwind CSS 4, DaisyUI 5, HTMX, Alpine.js.
