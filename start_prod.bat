@echo off
title Sistem Peminjaman Kunci Laboratorium (PRODUKSI)
cd /d "%~dp0"

echo ============================================
echo   SISTEM PEMINJAMAN KUNCI LABORATORIUM
echo   MODE PRODUKSI (waitress)
echo ============================================
echo.

if not exist ".venv\Scripts\activate" (
    echo [!] Virtual environment tidak ditemukan.
    echo     Jalankan: python -m venv .venv
    pause
    exit /b 1
)

call .venv\Scripts\activate

echo [*] Migrasi database...
python manage.py migrate
if errorlevel 1 (
    echo [!] Migrasi gagal.
    pause
    exit /b 1
)

echo [*] Mengumpulkan static files...
python manage.py collectstatic --noinput

echo [*] Menjalankan server produksi di http://0.0.0.0:8000
echo     (static disajikan oleh WhiteNoise, WSGI oleh waitress)
echo.

:: Paksa mode produksi (DEBUG=False) untuk server ini.
set DEBUG=False

:: Buka browser otomatis setelah 3 detik
timeout /t 3 /nobreak >nul
start http://localhost:8000

:: Jalankan server produksi.
waitress-serve --listen=0.0.0.0:8000 --threads=8 config.wsgi:application
pause