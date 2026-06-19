# TOS (Django) — Project scaffold

This directory contains a minimal Django project named TOS.

Quick start (PowerShell on Windows):

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

Replace the `SECRET_KEY` in `TOS/settings.py` before deploying to production.
