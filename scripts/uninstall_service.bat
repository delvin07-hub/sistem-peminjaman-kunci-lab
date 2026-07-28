@echo off
cd /d "%~dp0.."
set SERVICE_NAME=SistemPeminjamanKunciLab
set NSSM=scripts\nssm.exe

echo ============================================
echo   UNINSTALL WINDOWS SERVICE
echo ============================================
echo.

if not exist "%NSSM%" (
    echo [!] nssm.exe tidak ditemukan di scripts\nssm.exe
    pause
    exit /b 1
)

echo [*] Menghentikan service...
"%NSSM%" stop "%SERVICE_NAME%"
if %errorlevel% neq 0 (
    echo [i] Service tidak berjalan atau sudah dihentikan.
)

echo [*] Menghapus service...
"%NSSM%" remove "%SERVICE_NAME%" confirm
if %errorlevel% equ 0 (
    echo [OK] Service berhasil dihapus.
) else (
    echo [!] Gagal menghapus service. Jalankan sebagai Administrator.
)

timeout /t 3