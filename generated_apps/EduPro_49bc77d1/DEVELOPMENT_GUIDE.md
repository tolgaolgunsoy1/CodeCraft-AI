# EduPro - Geliştirme Rehberi

## 📝 Proje Geliştirme Planı

### 1. Proje Kurulumu
- [x] Android Studio projesi oluşturuldu
- [x] Gradle yapılandırması tamamlandı
- [x] Material Design 3 tema eklendi
- [x] Temel kütüphaneler eklendi

### 2. UI/UX Tasarımı
- [ ] Ana ekran tasarımı
- [ ] Navigasyon menüsü
- [ ] İkon seti oluşturma
- [ ] Splash screen tasarımı
- [ ] Loading animasyonları
- [ ] Task ekran tasarımı
- [ ] Category ekran tasarımı


### 3. Özellik Geliştirme
- [ ] Görev oluşturma implementasyonu
- [ ] Kategori yönetimi implementasyonu
- [ ] Hatırlatıcılar implementasyonu
- [ ] İlerleme takibi implementasyonu
- [ ] Takvim entegrasyonu implementasyonu
- [ ] Veri yedekleme implementasyonu


### 4. Veri Yönetimi
- [ ] Veritabanı şeması tasarla
- [ ] Room Database entegrasyonu
- [ ] SharedPreferences ayarları
- [ ] Veri senkronizasyonu

### 5. Test ve Kalite
- [ ] Unit testler yaz
- [ ] Integration testler
- [ ] UI testleri
- [ ] Performance testleri

## 🎨 Tasarım Sistemi

### Renk Rehberi
```xml
<!-- colors.xml -->
<color name="primary">#6200EE</color>
<color name="primary_variant">#3700B3</color>
<color name="secondary">#03DAC6</color>
<color name="background">#FFFFFF</color>
<color name="surface">#F5F5F5</color>
<color name="error">#B00020</color>
```

### Tipografi
```xml
<!-- styles.xml -->
<style name="TextAppearance.App.Headline1">
    <item name="android:textSize">24sp</item>
    <item name="android:textStyle">bold</item>
</style>
```

### Spacing
```xml
<!-- dimens.xml -->
<dimen name="spacing_xs">4dp</dimen>
<dimen name="spacing_sm">8dp</dimen>
<dimen name="spacing_md">16dp</dimen>
<dimen name="spacing_lg">24dp</dimen>
<dimen name="spacing_xl">32dp</dimen>
```

## 🛠️ Kod Standartları

### Java Naming Conventions
```java
// Class names: PascalCase
public class UserManager {}

// Method names: camelCase
public void getUserData() {}

// Variable names: camelCase
private String userName;

// Constants: UPPER_SNAKE_CASE
public static final String API_BASE_URL = "https://api.example.com";
```

### Layout Naming
```
activity_main.xml       // Activity layouts
fragment_profile.xml    // Fragment layouts
item_user.xml          // RecyclerView items
dialog_confirm.xml     // Dialog layouts
```

### Resource Naming
```
ic_home.xml            // Icons
bg_gradient.xml        // Backgrounds
shape_rounded.xml      // Shapes
selector_button.xml    // Selectors
```

## 📊 Performans Optimizasyonu

### 1. Layout Optimizasyonu
- ConstraintLayout kullan
- Nested layout'lardan kaçın
- ViewStub ile lazy loading
- include tag'i ile layout yeniden kullanımı

### 2. Memory Yönetimi
- Bitmap'leri doğru boyutlandır
- WeakReference kullan
- onDestroy'da cleanup yap
- Memory leak'leri kontrol et

### 3. Network Optimizasyonu
- Retrofit ile efficient API calls
- Caching stratejisi
- Offline support
- Progress indicator'lar

## 🔍 Debug ve Test

### Logging
```java
private static final String TAG = "MainActivity";
Log.d(TAG, "Debug message");
Log.e(TAG, "Error message", exception);
```

### Unit Test Örneği
```java
@RunWith(JUnit4.class)
public class UserValidatorTest {
    @Test
    public void testEmailValidation() {
        assertTrue(UserValidator.isValidEmail("test@example.com"));
        assertFalse(UserValidator.isValidEmail("invalid-email"));
    }
}
```

### Espresso UI Test
```java
@RunWith(AndroidJUnit4.class)
public class MainActivityTest {
    @Test
    public void testButtonClick() {
        onView(withId(R.id.button))
            .perform(click())
            .check(matches(isDisplayed()));
    }
}
```

## 🚀 Deployment

### Debug APK
```bash
./gradlew assembleDebug
```

### Release APK
```bash
./gradlew assembleRelease
```

### Play Store Hazırlık
1. App signing key oluştur
2. ProGuard/R8 yapılandır
3. Version code/name güncelle
4. Store listing hazırla
5. Screenshot'lar çek

---

**İyi kodlamalar! 🚀**
