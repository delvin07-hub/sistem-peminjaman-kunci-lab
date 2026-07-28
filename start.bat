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
echo [*] Buka http://localhost:8000 di browser
echo.
echo     Tekan Ctrl+C untuk menghentikan server
echo ============================================
echo.

python manage.py runserver 0.0.0.0:8000

pause