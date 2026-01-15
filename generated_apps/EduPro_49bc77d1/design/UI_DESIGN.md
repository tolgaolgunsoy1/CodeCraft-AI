# EduPro - UI/UX Tasarım Rehberi

## 🎨 Tasarım Felsefesi

**Tema:** Modern, minimalist ve kullanıcı dostu
**Hedef:** Özel uygulama: Eğitim platformu ve öğrenme yönetimi sistemi
**Platform:** Android (Material Design 3)

## 🌈 Renk Paleti

### Ana Renkler
```
Primary Color:    #6200EE (🟣 Mor)
Secondary Color:  #03DAC6 (🟢 Turkuaz)
Background:       #FFFFFF (⚪ Beyaz)
Surface:          #F5F5F5 (🔘 Açık Gri)
Error:            #B00020 (🔴 Kırmızı)
```

### Renk Kullanımı
- **Primary:** Ana butonlar, başlıklar, vurgular
- **Secondary:** Yardımcı butonlar, linkler, ikonlar
- **Background:** Ana arka plan
- **Surface:** Kartlar, dialog'lar, bottom sheet'ler
- **Error:** Hata mesajları, uyarılar

## 🔤 Tipografi

### Font Ailesi
**Roboto** (Android varsayılan)

### Metin Boyutları
```
Headline 1:  32sp (Ana başlıklar)
Headline 2:  24sp (Bölüm başlıkları)
Subtitle 1:  18sp (Alt başlıklar)
Body 1:      16sp (Ana metin)
Body 2:      14sp (Yardımcı metin)
Caption:     12sp (Küçük açıklamalar)
Button:      14sp (Buton metinleri)
```

## 📏 Layout Sistemi

### Spacing (Boşluk)
```
XS:  4dp  (Küçük boşluklar)
SM:  8dp  (Orta boşluklar)
MD:  16dp (Standart boşluklar)
LG:  24dp (Büyük boşluklar)
XL:  32dp (Çok büyük boşluklar)
```

## 📱 Ekran Tasarımları

### Ana Ekran
- AppBar ile başlık
- CardView'lar ile özellik listesi
- FloatingActionButton ile hızlı erişim
- Bottom Navigation (gerekirse)

### Liste Ekranları
- RecyclerView ile performanslı listeleme
- SwipeRefreshLayout ile yenileme
- Empty state görünümü
- Loading indicator

## 🎯 UI Bileşenleri

### Butonlar
```xml
<com.google.android.material.button.MaterialButton
    style="@style/Widget.Material3.Button"
    android:layout_width="match_parent"
    android:layout_height="56dp"
    android:text="Ana Buton"
    app:cornerRadius="28dp" />
```

### Kartlar
```xml
<com.google.android.material.card.MaterialCardView
    android:layout_width="match_parent"
    android:layout_height="wrap_content"
    app:cardCornerRadius="12dp"
    app:cardElevation="4dp">
    
    <!-- Kart içeriği -->
    
</com.google.android.material.card.MaterialCardView>
```

---

**Tasarım her zaman kullanıcı deneyimini öncelemeli! 🎨**
