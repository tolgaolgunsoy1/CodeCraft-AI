# CustomApp - Android Uygulaması

## 📱 Uygulama Hakkında

**Açıklama:** Özel uygulama: Eğitim platformu ve öğrenme yönetimi sistemi

**Kategori:** Genel

## ✨ Özellikler

- ✅ Görev oluşturma
- ✅ Kategori yönetimi
- ✅ Hatırlatıcılar
- ✅ İlerleme takibi
- ✅ Takvim entegrasyonu
- ✅ Veri yedekleme
- ✅ Karanlık tema

## 🏗️ Proje Yapısı

```
CustomApp/
├── app/
│   ├── src/main/
│   │   ├── java/com/example/customapp/
│   │   │   ├── MainActivity.java
│   │   │   ├── TaskActivity.java
│   │   │   ├── CategoryActivity.java
│   │   │   ├── CalendarActivity.java
│   │   │   ├── SettingsActivity.java

│   │   ├── res/
│   │   │   ├── layout/
│   │   │   ├── values/
│   │   │   └── drawable/
│   │   └── AndroidManifest.xml
│   └── build.gradle
├── gradle/wrapper/
├── build.gradle
├── gradlew.bat
└── build_apk.bat
```

## 🚀 Kurulum ve Çalıştırma

### 1. Android Studio ile Açma
1. Android Studio'yu açın
2. "Open an existing Android Studio project" seçin
3. Bu klasörü seçin
4. Gradle sync bekleyin
5. "Run" butonuna tıklayın

### 2. APK Oluşturma
```bash
# Otomatik APK oluşturma
build_apk.bat

# Manuel APK oluşturma
gradlew.bat assembleDebug
```

APK dosyası: `app/build/outputs/apk/debug/app-debug.apk`

## 📊 Teknik Detaylar

### Aktiviteler
- **MainActivity**: Ana ekran ve navigasyon
- **TaskActivity**: Görev yönetimi
- **CategoryActivity**: Kategori yönetimi
- **CalendarActivity**: Takvim görünümü
- **SettingsActivity**: Ayarlar menüsü


### İzinler
- **SET_ALARM**: Alarm kurma
- **RECEIVE_BOOT_COMPLETED**: Sistem başlatıldığında çalışma

### Kütüphaneler
- **room**: Veritabanı yönetimi
- **lifecycle-extensions**: Yaşam döngüsü yönetimi

## 🎨 Tasarım Rehberi

### Renk Paleti
- **Primary:** #6200EE (Mor)
- **Secondary:** #03DAC6 (Turkuaz)
- **Background:** #FFFFFF (Beyaz)
- **Surface:** #F5F5F5 (Açık Gri)

### Tipografi
- **Başlık:** 24sp, Bold
- **Alt Başlık:** 18sp, Medium
- **Gövde Metni:** 16sp, Regular
- **Küçük Metin:** 14sp, Regular

### UI Bileşenleri
- **Material Design 3** standartları
- **CardView** ile modern kartlar
- **RecyclerView** ile listeler
- **FloatingActionButton** ile hızlı aksiyonlar

## 🛠️ Geliştirme Rehberi

### Yeni Özellik Ekleme
1. **Activity Ekleme:**
   ```java
   public class NewActivity extends AppCompatActivity {
       @Override
       protected void onCreate(Bundle savedInstanceState) {
           super.onCreate(savedInstanceState);
           setContentView(R.layout.activity_new);
       }
   }
   ```

2. **Layout Oluşturma:**
   ```xml
   <?xml version="1.0" encoding="utf-8"?>
   <LinearLayout xmlns:android="http://schemas.android.com/apk/res/android"
       android:layout_width="match_parent"
       android:layout_height="match_parent"
       android:orientation="vertical">
       
       <!-- UI bileşenleri buraya -->
       
   </LinearLayout>
   ```

3. **Manifest'e Ekleme:**
   ```xml
   <activity android:name=".NewActivity" />
   ```

### Veritabanı Ekleme
```java
// Room Database kullanımı
@Entity
public class User {
    @PrimaryKey
    public int id;
    public String name;
    public String email;
}
```

### Network İşlemleri
```java
// Retrofit kullanımı
public interface ApiService {
    @GET("users")
    Call<List<User>> getUsers();
}
```

## 📝 Geliştirme Adımları

### Faz 1: Temel Yapı
- [x] Proje yapısı oluşturuldu
- [x] MainActivity hazırlandı
- [x] Temel layout'lar eklendi
- [x] Material Design tema uygulandı

### Faz 2: Özellik Geliştirme
- [ ] Görev oluşturma geliştirilecek
- [ ] Kategori yönetimi geliştirilecek
- [ ] Hatırlatıcılar geliştirilecek
- [ ] İlerleme takibi geliştirilecek
- [ ] Takvim entegrasyonu geliştirilecek


### Faz 3: Test ve Optimizasyon
- [ ] Unit testler yazılacak
- [ ] UI testleri eklenecek
- [ ] Performans optimizasyonu
- [ ] Memory leak kontrolü

### Faz 4: Yayınlama
- [ ] İkon ve splash screen
- [ ] Play Store açıklaması
- [ ] Screenshot'lar
- [ ] Release APK oluşturma

## 📊 Performans İpuçları

1. **RecyclerView Optimizasyonu:**
   - ViewHolder pattern kullan
   - setHasFixedSize(true) ekle
   - Gereksiz layout_weight kullanma

2. **Image Loading:**
   - Glide kütüphanesi kullan
   - Placeholder'lar ekle
   - Cache stratejisi belirle

3. **Memory Yönetimi:**
   - Static referanslardan kaçın
   - Context leak'lerini önle
   - onDestroy'da cleanup yap

## 🔍 Test Rehberi

### Unit Test Örneği
```java
@Test
public void testUserValidation() {
    User user = new User("test@example.com", "password");
    assertTrue(user.isValid());
}
```

### UI Test Örneği
```java
@Test
public void testLoginButton() {
    onView(withId(R.id.login_button))
        .perform(click())
        .check(matches(isDisplayed()));
}
```

## 📞 Destek

Sorularınız için:
- Android Developer Documentation
- Stack Overflow
- Material Design Guidelines

---

**Not:** Bu proje Android Uygulama Üretici ile otomatik oluşturulmuştur.
