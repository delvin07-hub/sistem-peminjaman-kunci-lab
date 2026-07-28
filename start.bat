@echo off
title Sistem Peminjaman Kunci Laboratorium
cd /d "%~dp0"

echo ============================================
echo   SISTEM PEMINJAMAN KUNCI LABORATORIUM
echo ============================================
echo.

if not exist ".venv\Scripts\activate" (
    echo [!] Virtual environment tidak ditemukan.
    echo     Jalankan: python -m venv .venv
    pause
    exit /b 1
)

call .venv\Scripts\activate

echo [*] Mengaktifkan virtual environment... OK
echo [*] Menjalankan server di http://0.0.0.0:8000
echo.

:: Buka browser otomatis setelah 3 detik
timeout /t 3 /nobreak >nul
start http://localhost:8000

python manage.py runserver 0.0.0.0:8000
pause