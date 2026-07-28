@echo off
cd /d "%~dp0.."
set SERVICE_NAME=SistemPeminjamanKunciLab
set NSSM=scripts\nssm.exe

echo ============================================
echo   INSTALL WINDOWS SERVICE
echo ============================================
echo.

if not exist "%NSSM%" (
    echo [!] nssm.exe tidak ditemukan di scripts\nssm.exe
    echo.
    echo     Download dari: https://nssm.cc/download
    echo     Letakkan nssm.exe di folder scripts/
    pause
    exit /b 1
)

echo [*] Menghentikan service jika sudah berjalan...
"%NSSM%" stop "%SERVICE_NAME%" >nul 2>&1

echo [*] Menghapus service lama jika ada...
"%NSSM%" remove "%SERVICE_NAME%" confirm >nul 2>&1

echo [*] Membuat service baru...
"%NSSM%" install "%SERVICE_NAME%" "%~dp0..\start.bat"

echo [*] Mengatur service agar auto-start...
"%NSSM%" set "%SERVICE_NAME%" Start SERVICE_AUTO_START

echo [*] Mengatur directory kerja...
"%NSSM%" set "%SERVICE_NAME%" AppDirectory "%~dp0.."

echo [*] Mengatur restart otomatis jika crash...
"%NSSM%" set "%SERVICE_NAME%" AppThrottle 0
"%NSSM%" set "%SERVICE_NAME%" AppExit Default Exit

echo [*] Menyalakan service...
"%NSSM%" start "%SERVICE_NAME%"

echo.
echo ============================================
echo   Service berhasil diinstall dan dijalankan!
echo   Nama Service : %SERVICE_NAME%
echo   URL          : http://localhost:8000
echo ============================================
timeout /t 5