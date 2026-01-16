@echo off
echo WellnessApp APK Building...
echo.

cd /d "C:\codecraftai\backend\..\generated_apps\WellnessApp_16cb1f8c"

echo Building APK automatically...
call gradlew.bat assembleDebug

if exist "app\build\outputs\apk\debug\app-debug.apk" (
    echo.
    echo SUCCESS! APK created at:
    echo app\build\outputs\apk\debug\app-debug.apk
    echo.
) else (
    echo.
    echo Build failed. Please check Java installation.
    echo.
)
