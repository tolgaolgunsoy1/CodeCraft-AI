# HealthTracker - Android Studio Import Rehberi

## APK Oluşturma Adımları

### 1. Android Studio'yu Açın
- Android Studio'yu başlatın
- "Open an existing Android Studio project" seçin
- Bu klasörü seçin: `c:\codecraftai\backend\..\generated_apps\86afc7b8-d8bf-4328-b6d6-740df6d5040f`

### 2. Gradle Sync
- Proje açıldıktan sonra Gradle sync otomatik başlar
- "Sync Now" butonuna tıklayın (gerekirse)
- Sync tamamlanana kadar bekleyin

### 3. APK Oluşturma
- Menüden **Build > Build Bundle(s) / APK(s) > Build APK(s)** seçin
- Build işlemi tamamlanana kadar bekleyin
- "locate" linkine tıklayarak APK'yı bulun

### 4. APK Konumu
```
app/build/outputs/apk/debug/app-debug.apk
```

## Alternatif Yöntemler

### Gradle Command Line (Eğer Gradle kuruluysa)
```bash
./gradlew assembleDebug
```

### Android Studio Terminal
```bash
cd c:\codecraftai\backend\..\generated_apps\86afc7b8-d8bf-4328-b6d6-740df6d5040f
./gradlew assembleDebug
```

## Sorun Giderme

### Gradle Sync Hatası
- **File > Invalidate Caches and Restart**
- **Build > Clean Project**
- **Build > Rebuild Project**

### SDK Hatası
- **File > Project Structure > SDK Location**
- Android SDK path'ini kontrol edin

### Build Hatası
- **Build > Clean Project**
- **Build > Rebuild Project**
- Gradle files'ları kontrol edin

---

**Not:** Bu proje Android Uygulama Üretici ile oluşturulmuştur.
APK oluşturmak için Android Studio kullanmanız önerilir.
