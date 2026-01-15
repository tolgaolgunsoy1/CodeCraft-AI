@echo off
echo WellnessApp APK Olusturuluyor...
echo.

cd /d "c:\codecraftai\backend\..\generated_apps\WellnessApp_dd77b972"

echo Android Studio ile acmak icin ENTER basin...
echo (APK olusturmak icin Android Studio gereklidir)
echo.
echo Adimlar:
echo 1. Android Studio'yu ac
echo 2. "Open an existing project" sec
echo 3. Bu klasoru sec: c:\codecraftai\backend\..\generated_apps\WellnessApp_dd77b972
echo 4. Gradle sync bekle
echo 5. Build > Make Project
echo 6. Build > Build Bundle(s) / APK(s) > Build APK(s)
echo.
echo APK konumu: app\build\outputs\apk\debug\app-debug.apk
echo.
pause

echo Android Studio aciliyor...
start "" "c:\codecraftai\backend\..\generated_apps\WellnessApp_dd77b972"
