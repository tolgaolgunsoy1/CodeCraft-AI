"""
Enterprise-Level Android App Generator
Gelişmiş özellikler ve profesyonel kod kalitesi
"""

ENHANCED_TEMPLATES = {
    'productivity': {
        'name': 'TaskMaster Pro',
        'description': 'Enterprise seviye görev yönetimi ve verimlilik platformu',
        'features': [
            'Akıllı görev önceliklendirme (AI destekli)',
            'Gerçek zamanlı ekip işbirliği',
            'Gelişmiş kategori ve etiket sistemi',
            'Akıllı hatırlatıcılar ve bildirimler',
            'Takvim ve zaman çizelgesi entegrasyonu',
            'Veri yedekleme ve senkronizasyon',
            'Karanlık tema ve özelleştirilebilir arayüz',
            'Offline çalışma modu',
            'Detaylı raporlama ve analitik',
            'Sesli komut desteği'
        ],
        'activities': [
            'MainActivity', 'TaskListActivity', 'TaskDetailActivity', 
            'CategoryActivity', 'CalendarActivity', 'SettingsActivity',
            'AnalyticsActivity', 'TeamActivity'
        ],
        'permissions': ['INTERNET', 'SET_ALARM', 'RECEIVE_BOOT_COMPLETED', 'RECORD_AUDIO'],
        'dependencies': ['room', 'retrofit2', 'workmanager', 'lifecycle', 'navigation']
    },
    'social_media': {
        'name': 'SocialHub Pro',
        'description': 'Yeni nesil sosyal medya ve topluluk platformu',
        'features': [
            'Gelişmiş kullanıcı profili ve özelleştirme',
            'Multimedya paylaşımı (fotoğraf, video, ses)',
            'Gerçek zamanlı mesajlaşma ve grup sohbetleri',
            'Hikaye ve canlı yayın özellikleri',
            'Akıllı içerik keşfi ve öneri sistemi',
            'Takip sistemi ve sosyal ağ',
            'Beğeni, yorum ve paylaşım sistemi',
            'Bildirim merkezi',
            'Gizlilik ve güvenlik ayarları',
            'İçerik moderasyonu'
        ],
        'activities': [
            'MainActivity', 'ProfileActivity', 'FeedActivity', 'PostActivity',
            'ChatActivity', 'StoryActivity', 'LiveActivity', 'SearchActivity',
            'NotificationActivity', 'SettingsActivity'
        ],
        'permissions': ['INTERNET', 'CAMERA', 'READ_EXTERNAL_STORAGE', 'WRITE_EXTERNAL_STORAGE', 'RECORD_AUDIO'],
        'dependencies': ['retrofit2', 'glide', 'room', 'firebase', 'exoplayer', 'camerax']
    },
    'ecommerce': {
        'name': 'ShopMaster Pro',
        'description': 'Kapsamlı e-ticaret ve satış platformu',
        'features': [
            'Gelişmiş ürün katalogu ve arama',
            'Akıllı filtreleme ve sıralama',
            'Sepet yönetimi ve kaydetme',
            'Çoklu ödeme yöntemi entegrasyonu',
            'Sipariş takibi ve geçmişi',
            'Favori ürünler ve istek listesi',
            'İndirim kuponu ve promosyon sistemi',
            'Ürün değerlendirme ve yorumlar',
            'Canlı destek ve chatbot',
            'AR ürün önizleme'
        ],
        'activities': [
            'MainActivity', 'ProductListActivity', 'ProductDetailActivity',
            'CartActivity', 'CheckoutActivity', 'OrderHistoryActivity',
            'WishlistActivity', 'ProfileActivity', 'SearchActivity', 'SupportActivity'
        ],
        'permissions': ['INTERNET', 'ACCESS_NETWORK_STATE', 'CAMERA'],
        'dependencies': ['retrofit2', 'room', 'stripe', 'glide', 'arcore']
    },
    'health': {
        'name': 'HealthTracker Pro',
        'description': 'Kapsamlı sağlık ve fitness takip platformu',
        'features': [
            'Gelişmiş adım sayacı ve GPS takibi',
            'Kalori ve besin değeri hesaplama',
            'Özelleştirilmiş egzersiz planları',
            'Su tüketimi ve uyku takibi',
            'Kilo ve vücut ölçümleri',
            'Detaylı istatistik ve grafikler',
            'Hedef belirleme ve motivasyon',
            'Sağlık cihazları entegrasyonu',
            'Sosyal paylaşım ve yarışmalar',
            'AI destekli sağlık önerileri'
        ],
        'activities': [
            'MainActivity', 'DashboardActivity', 'WorkoutActivity',
            'NutritionActivity', 'StatsActivity', 'GoalsActivity',
            'DevicesActivity', 'SocialActivity', 'ProfileActivity', 'SettingsActivity'
        ],
        'permissions': ['ACTIVITY_RECOGNITION', 'BODY_SENSORS', 'ACCESS_FINE_LOCATION', 'INTERNET'],
        'dependencies': ['fitness', 'charts', 'room', 'workmanager', 'mlkit']
    }
}

MODERN_DEPENDENCIES = {
    'core': [
        'androidx.core:core-ktx:1.12.0',
        'androidx.appcompat:appcompat:1.6.1',
        'com.google.android.material:material:1.11.0',
        'androidx.constraintlayout:constraintlayout:2.1.4'
    ],
    'architecture': [
        'androidx.lifecycle:lifecycle-viewmodel-ktx:2.7.0',
        'androidx.lifecycle:lifecycle-livedata-ktx:2.7.0',
        'androidx.lifecycle:lifecycle-runtime-ktx:2.7.0',
        'androidx.navigation:navigation-fragment-ktx:2.7.6',
        'androidx.navigation:navigation-ui-ktx:2.7.6'
    ],
    'database': [
        'androidx.room:room-runtime:2.6.1',
        'androidx.room:room-ktx:2.6.1'
    ],
    'network': [
        'com.squareup.retrofit2:retrofit:2.9.0',
        'com.squareup.retrofit2:converter-gson:2.9.0',
        'com.squareup.okhttp3:logging-interceptor:4.12.0'
    ],
    'image': [
        'com.github.bumptech.glide:glide:4.16.0',
        'androidx.palette:palette-ktx:1.0.0'
    ],
    'async': [
        'org.jetbrains.kotlinx:kotlinx-coroutines-android:1.7.3',
        'androidx.work:work-runtime-ktx:2.9.0'
    ],
    'ui': [
        'androidx.recyclerview:recyclerview:1.3.2',
        'androidx.cardview:cardview:1.0.0',
        'androidx.swiperefreshlayout:swiperefreshlayout:1.1.0',
        'com.google.android.material:material:1.11.0'
    ],
    'testing': [
        'junit:junit:4.13.2',
        'androidx.test.ext:junit:1.1.5',
        'androidx.test.espresso:espresso-core:3.5.1',
        'org.mockito:mockito-core:5.8.0',
        'androidx.arch.core:core-testing:2.2.0'
    ]
}

ENTERPRISE_FEATURES = {
    'security': [
        'Biometric authentication (parmak izi/yüz tanıma)',
        'Encrypted local storage',
        'Secure API communication (SSL pinning)',
        'Session management',
        'Data encryption at rest'
    ],
    'performance': [
        'Image caching and optimization',
        'Database indexing',
        'Lazy loading',
        'Memory leak prevention',
        'Background task optimization'
    ],
    'ux': [
        'Smooth animations',
        'Skeleton screens',
        'Pull-to-refresh',
        'Infinite scroll',
        'Empty states',
        'Error handling',
        'Loading indicators'
    ],
    'accessibility': [
        'Screen reader support',
        'High contrast mode',
        'Font scaling',
        'Touch target sizes',
        'Color blind friendly'
    ]
}
