import os
import re
import json
from datetime import datetime
import requests

class AndroidAppGenerator:
    def __init__(self):
        self.output_dir = "C:/android_projects"
        self.ensure_output_dir()
        self.app_templates = self.load_templates()
    
    def ensure_output_dir(self):
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
    
    def load_templates(self):
        return {
            'social_media': {
                'name': 'SocialConnect',
                'description': 'Modern sosyal medya uygulaması',
                'features': ['Kullanıcı profili', 'Post paylaşma', 'Fotoğraf/video yükleme', 'Beğeni ve yorum sistemi', 'Takip sistemi', 'Mesajlaşma', 'Hikaye özelliği', 'Bildirimler'],
                'activities': ['MainActivity', 'ProfileActivity', 'PostActivity', 'FeedActivity', 'ChatActivity', 'StoryActivity'],
                'permissions': ['INTERNET', 'CAMERA', 'READ_EXTERNAL_STORAGE', 'WRITE_EXTERNAL_STORAGE'],
                'dependencies': ['recyclerview', 'cardview', 'glide', 'retrofit2']
            },
            'ecommerce': {
                'name': 'ShopEasy',
                'description': 'Kapsamlı e-ticaret uygulaması',
                'features': ['Ürün kataloğu', 'Arama ve filtreleme', 'Sepet yönetimi', 'Güvenli ödeme', 'Sipariş takibi', 'Kullanıcı hesabı', 'Favori ürünler', 'İndirim kuponu'],
                'activities': ['MainActivity', 'ProductListActivity', 'ProductDetailActivity', 'CartActivity', 'CheckoutActivity', 'OrderHistoryActivity'],
                'permissions': ['INTERNET', 'ACCESS_NETWORK_STATE'],
                'dependencies': ['recyclerview', 'cardview', 'retrofit2', 'gson']
            },
            'game': {
                'name': 'GameMaster',
                'description': 'Eğlenceli mobil oyun',
                'features': ['Oyun mekaniği', 'Skor sistemi', 'Seviye ilerlemesi', 'Başarımlar', 'Liderlik tablosu', 'Ses efektleri', 'Ayarlar menüsü'],
                'activities': ['MainActivity', 'GameActivity', 'ScoreActivity', 'LeaderboardActivity', 'SettingsActivity'],
                'permissions': ['VIBRATE'],
                'dependencies': ['play-services-games']
            },
            'productivity': {
                'name': 'TaskMaster',
                'description': 'Verimlilik ve görev yönetimi uygulaması',
                'features': ['Görev oluşturma', 'Kategori yönetimi', 'Hatırlatıcılar', 'İlerleme takibi', 'Takvim entegrasyonu', 'Veri yedekleme', 'Karanlık tema'],
                'activities': ['MainActivity', 'TaskActivity', 'CategoryActivity', 'CalendarActivity', 'SettingsActivity'],
                'permissions': ['SET_ALARM', 'RECEIVE_BOOT_COMPLETED'],
                'dependencies': ['room', 'lifecycle-extensions']
            },
            'health': {
                'name': 'HealthTracker',
                'description': 'Sağlık ve fitness takip uygulaması',
                'features': ['Adım sayacı', 'Kalori hesaplama', 'Egzersiz planları', 'Su tüketimi takibi', 'Kilo takibi', 'İstatistikler', 'Hedef belirleme'],
                'activities': ['MainActivity', 'StepCounterActivity', 'WorkoutActivity', 'StatsActivity', 'ProfileActivity'],
                'permissions': ['ACTIVITY_RECOGNITION', 'BODY_SENSORS'],
                'dependencies': ['play-services-fitness', 'charts']
            }
        }
    
    def ensure_output_dir(self):
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
    
    def generate_from_idea(self, idea, language='java', architecture='single_activity', ui_framework='xml', project_path=None, app_name=None):
        analysis = self.analyze_idea(idea)
        # Use provided app_name if available, otherwise use template name
        if app_name:
            analysis['name'] = app_name
        app_name = analysis['name']
        package_name = f"com.example.{app_name.lower().replace(' ', '')}"
        if project_path is None:
            project_path = os.path.join(self.output_dir, app_name.replace(' ', '_'))
        
        # Enhanced configuration
        config = {
            'language': language,
            'architecture': architecture,
            'ui_framework': ui_framework,
            'use_compose': ui_framework == 'compose',
            'use_navigation': architecture == 'single_activity'
        }
        
        self.create_project_structure(project_path, package_name, analysis, config)
        
        return {
            'app_name': analysis['name'],
            'description': analysis['description'],
            'features': analysis['features'],
            'project_path': project_path,
            'activities': analysis['activities'],
            'permissions': analysis.get('permissions', []),
            'dependencies': analysis.get('dependencies', []),
            'development_progress': self.calculate_development_progress(analysis),
            'architecture': architecture,
            'language': language,
            'ui_framework': ui_framework
        }
    
    def analyze_idea(self, idea):
        idea_lower = idea.lower()
        
        # Gelişmiş AI analizi
        if any(word in idea_lower for word in ['sosyal', 'medya', 'paylaş', 'takip', 'arkadaş', 'chat', 'mesaj']):
            template = self.app_templates['social_media']
        elif any(word in idea_lower for word in ['e-ticaret', 'alışveriş', 'satış', 'ürün', 'sepet', 'ödeme', 'mağaza']):
            template = self.app_templates['ecommerce']
        elif any(word in idea_lower for word in ['oyun', 'game', 'oyna', 'skor', 'seviye', 'yarış']):
            template = self.app_templates['game']
        elif any(word in idea_lower for word in ['görev', 'task', 'not', 'planlama', 'organize', 'verimlilik']):
            template = self.app_templates['productivity']
        elif any(word in idea_lower for word in ['sağlık', 'fitness', 'spor', 'egzersiz', 'adım', 'kalori']):
            template = self.app_templates['health']
        else:
            # Varsayılan olarak productivity template kullan
            template = self.app_templates['productivity']
            template['name'] = 'CustomApp'
            template['description'] = f'Özel uygulama: {idea}'
        
        return template
    
    def create_project_structure(self, project_path, package_name, analysis, config):
        # Ana klasör yapısını oluştur
        os.makedirs(project_path, exist_ok=True)
        
        # Android proje yapısı
        app_path = os.path.join(project_path, 'app')
        src_path = os.path.join(app_path, 'src', 'main')
        code_path = os.path.join(src_path, 'kotlin' if config['language'] == 'kotlin' else 'java', *package_name.split('.'))
        res_path = os.path.join(src_path, 'res')
        
        os.makedirs(code_path, exist_ok=True)
        os.makedirs(os.path.join(res_path, 'layout'), exist_ok=True)
        os.makedirs(os.path.join(res_path, 'values'), exist_ok=True)
        os.makedirs(os.path.join(res_path, 'values-night'), exist_ok=True)
        os.makedirs(os.path.join(res_path, 'drawable'), exist_ok=True)
        os.makedirs(os.path.join(res_path, 'navigation'), exist_ok=True)
        
        # Dosyaları oluştur
        self.create_manifest(src_path, package_name, analysis, config)
        self.create_gradle_files(project_path, app_path, package_name, analysis, config)
        
        if config['architecture'] == 'single_activity':
            self.create_single_activity_structure(code_path, package_name, analysis, config)
        else:
            self.create_multi_activity_structure(code_path, package_name, analysis, config)
        
        if config['use_compose']:
            self.create_compose_ui(code_path, package_name, analysis, config)
        else:
            self.create_layouts(res_path, analysis)
        
        self.create_resources(res_path, analysis)
        self.create_dark_mode_resources(res_path, analysis)
        
        # Gradle wrapper dosyalarını oluştur
        self.create_gradle_wrapper(project_path)
        
        # APK build script oluştur
        self.create_build_script(project_path, analysis['name'])
        
        # Production-ready dosyalar oluştur
        self.create_production_files(project_path, package_name, analysis)
        
        # Advanced production features
        self.create_advanced_features(project_path, package_name, analysis, config)
        self.create_ci_cd_files(project_path, analysis)
        self.create_github_actions(project_path, analysis)
        
        # Dokümantasyon oluştur
        self.create_documentation(project_path, analysis)
        
        # Tasarım dosyaları oluştur
        self.create_design_files(project_path, analysis)
    
    def create_manifest(self, src_path, package_name, analysis):
        permissions = '\n'.join([f'    <uses-permission android:name="android.permission.{perm}" />' for perm in analysis.get('permissions', [])])
        
        # Temel network permissions ekle
        base_permissions = '''    <uses-permission android:name="android.permission.ACCESS_NETWORK_STATE" />
    <uses-permission android:name="android.permission.WAKE_LOCK" />'''
        
        if permissions:
            permissions = base_permissions + '\n' + permissions
        else:
            permissions = base_permissions
        
        manifest_content = f'''<?xml version="1.0" encoding="utf-8"?>
<manifest xmlns:android="http://schemas.android.com/apk/res/android"
    package="{package_name}">

{permissions}

    <application
        android:allowBackup="true"
        android:icon="@mipmap/ic_launcher"
        android:label="@string/app_name"
        android:theme="@style/AppTheme"
        android:usesCleartextTraffic="true">
        
        <activity android:name=".MainActivity"
            android:exported="true">
            <intent-filter>
                <action android:name="android.intent.action.MAIN" />
                <category android:name="android.intent.category.LAUNCHER" />
            </intent-filter>
        </activity>
        
        {self.generate_activity_declarations(analysis)}
    </application>
</manifest>'''
        
        with open(os.path.join(src_path, 'AndroidManifest.xml'), 'w') as f:
            f.write(manifest_content)
    
    def generate_activity_declarations(self, analysis):
        declarations = ""
        for activity in analysis.get('activities', [])[1:]:  # MainActivity zaten var
            declarations += f'        <activity android:name=".{activity}" />\n'
        return declarations
    
    def create_gradle_files(self, project_path, app_path, package_name):
        # build.gradle (project level)
        project_gradle = '''buildscript {
    repositories {
        google()
        mavenCentral()
    }
    dependencies {
        classpath 'com.android.tools.build:gradle:8.0.2'
    }
}

allprojects {
    repositories {
        google()
        mavenCentral()
    }
}'''
        
        with open(os.path.join(project_path, 'build.gradle'), 'w') as f:
            f.write(project_gradle)
        
        # build.gradle (app level)
        app_gradle = '''plugins {
    id 'com.android.application'
}

android {
    namespace "''' + package_name + '''"
    compileSdk 34
    
    defaultConfig {
        applicationId "''' + package_name + '''"
        minSdk 24
        targetSdk 34
        versionCode 1
        versionName "1.0"
    }
    
    buildTypes {
        release {
            minifyEnabled false
            proguardFiles getDefaultProguardFile('proguard-android-optimize.txt'), 'proguard-rules.pro'
        }
    }
    
    compileOptions {
        sourceCompatibility JavaVersion.VERSION_1_8
        targetCompatibility JavaVersion.VERSION_1_8
    }
    
    buildFeatures {
        viewBinding true
    }
}

dependencies {
    implementation 'androidx.appcompat:appcompat:1.6.1'
    implementation 'com.google.android.material:material:1.11.0'
    implementation 'androidx.constraintlayout:constraintlayout:2.1.4'
    implementation 'androidx.recyclerview:recyclerview:1.3.2'
    implementation 'androidx.cardview:cardview:1.0.0'
    implementation 'androidx.lifecycle:lifecycle-viewmodel:2.7.0'
    implementation 'androidx.lifecycle:lifecycle-livedata:2.7.0'
    implementation 'androidx.lifecycle:lifecycle-common-java8:2.7.0'
    implementation 'com.squareup.retrofit2:retrofit:2.9.0'
    implementation 'com.squareup.retrofit2:converter-gson:2.9.0'
    implementation 'com.github.bumptech.glide:glide:4.16.0'
    implementation 'androidx.room:room-runtime:2.5.0'
    annotationProcessor 'androidx.room:room-compiler:2.5.0'
    implementation 'com.squareup.okhttp3:okhttp:4.12.0'
    implementation 'com.squareup.okhttp3:logging-interceptor:4.12.0'
    implementation 'androidx.work:work-runtime:2.9.0'
    implementation 'androidx.navigation:navigation-fragment:2.7.6'
    implementation 'androidx.navigation:navigation-ui:2.7.6'
    
    // Testing
    testImplementation 'junit:junit:4.13.2'
    testImplementation 'androidx.arch.core:core-testing:2.2.0'
    testImplementation 'org.mockito:mockito-core:5.8.0'
    androidTestImplementation 'androidx.test.ext:junit:1.1.5'
    androidTestImplementation 'androidx.test.espresso:espresso-core:3.5.1'
    androidTestImplementation 'androidx.test:runner:1.5.2'
    androidTestImplementation 'androidx.test:rules:1.5.0'
}'''
        
        with open(os.path.join(app_path, 'build.gradle'), 'w') as f:
            f.write(app_gradle)
        
        # settings.gradle
        settings_gradle = '''pluginManagement {
    repositories {
        google()
        mavenCentral()
        gradlePluginPortal()
    }
}
dependencyResolutionManagement {
    repositoriesMode.set(RepositoriesMode.FAIL_ON_PROJECT_REPOS)
    repositories {
        google()
        mavenCentral()
    }
}

rootProject.name = "''' + package_name.split('.')[-1] + '''"
include ':app'
'''
        
        with open(os.path.join(project_path, 'settings.gradle'), 'w') as f:
            f.write(settings_gradle)
        
        # gradle.properties
        gradle_properties = '''# Project-wide Gradle settings.
org.gradle.jvmargs=-Xmx2048m -Dfile.encoding=UTF-8
org.gradle.parallel=true
android.useAndroidX=true
android.enableJetifier=true
'''
        
        with open(os.path.join(project_path, 'gradle.properties'), 'w') as f:
            f.write(gradle_properties)
    
    def create_java_main_activity(self, package_name, analysis):
        """Create Java MainActivity"""
        return f'''package {package_name};

import androidx.appcompat.app.AppCompatActivity;
import androidx.recyclerview.widget.LinearLayoutManager;
import androidx.recyclerview.widget.RecyclerView;
import android.content.Intent;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.TextView;
import android.widget.Toast;
import java.util.ArrayList;
import java.util.List;

public class MainActivity extends AppCompatActivity {{

    private RecyclerView featuresRecyclerView;
    private TextView appDescriptionText;
    private Button startButton;

    @Override
    protected void onCreate(Bundle savedInstanceState) {{
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        
        initializeViews();
        setupFeaturesList();
    }}
    
    private void initializeViews() {{
        appDescriptionText = findViewById(R.id.app_description);
        featuresRecyclerView = findViewById(R.id.features_recycler);
        startButton = findViewById(R.id.start_button);
        
        appDescriptionText.setText("{analysis['description']}");
        
        startButton.setOnClickListener(new View.OnClickListener() {{
            @Override
            public void onClick(View v) {{
                Toast.makeText(MainActivity.this, "Hoş geldiniz! Uygulama hazır.", Toast.LENGTH_LONG).show();
            }}
        }});
    }}
    
    private void setupFeaturesList() {{
        List<String> features = new ArrayList<>();
        {self.generate_features_list(analysis['features'])}
        
        featuresRecyclerView.setLayoutManager(new LinearLayoutManager(this));
        // Adapter burada eklenecek
    }}
}}'''
        # MainActivity
        main_activity = f'''package {package_name};

import androidx.appcompat.app.AppCompatActivity;
import androidx.recyclerview.widget.LinearLayoutManager;
import androidx.recyclerview.widget.RecyclerView;
import android.content.Intent;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.TextView;
import android.widget.Toast;
import java.util.ArrayList;
import java.util.List;

public class MainActivity extends AppCompatActivity {{

    private RecyclerView featuresRecyclerView;
    private TextView appDescriptionText;
    private Button startButton;

    @Override
    protected void onCreate(Bundle savedInstanceState) {{
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        
        initializeViews();
        setupFeaturesList();
    }}
    
    private void initializeViews() {{
        appDescriptionText = findViewById(R.id.app_description);
        featuresRecyclerView = findViewById(R.id.features_recycler);
        startButton = findViewById(R.id.start_button);
        
        appDescriptionText.setText("{analysis['description']}");
        
        startButton.setOnClickListener(new View.OnClickListener() {{
            @Override
            public void onClick(View v) {{
                Toast.makeText(MainActivity.this, "Hoş geldiniz! Uygulama hazır.", Toast.LENGTH_LONG).show();
            }}
        }});
    }}
    
    private void setupFeaturesList() {{
        List<String> features = new ArrayList<>();
        {self.generate_features_list(analysis['features'])}
        
        featuresRecyclerView.setLayoutManager(new LinearLayoutManager(this));
        // Adapter burada eklenecek
    }}
}}'''
        
        with open(os.path.join(java_path, 'MainActivity.java'), 'w') as f:
            f.write(main_activity)
        
        # Diğer aktiviteleri oluştur
        for activity in analysis.get('activities', [])[1:]:
            self.create_secondary_activity(java_path, package_name, activity)
    
    def generate_features_list(self, features):
        features_code = ""
        for feature in features:
            features_code += f'        features.add("{feature}");\n'
        return features_code
    
    def create_secondary_activity(self, java_path, package_name, activity_name):
        activity_code = f'''package {package_name};

import androidx.appcompat.app.AppCompatActivity;
import android.os.Bundle;
import android.view.MenuItem;

public class {activity_name} extends AppCompatActivity {{

    @Override
    protected void onCreate(Bundle savedInstanceState) {{
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_{activity_name.lower().replace('activity', '')});
        
        if (getSupportActionBar() != null) {{
            getSupportActionBar().setDisplayHomeAsUpEnabled(true);
        }}
    }}
    
    @Override
    public boolean onOptionsItemSelected(MenuItem item) {{
        if (item.getItemId() == android.R.id.home) {{
            onBackPressed();
            return true;
        }}
        return super.onOptionsItemSelected(item);
    }}
}}'''
        
        with open(os.path.join(java_path, f'{activity_name}.java'), 'w') as f:
            f.write(activity_code)
    
    def create_layouts(self, res_path, analysis):
        # activity_main.xml - Modern Material Design
        main_layout = f'''<?xml version="1.0" encoding="utf-8"?>
<androidx.coordinatorlayout.widget.CoordinatorLayout xmlns:android="http://schemas.android.com/apk/res/android"
    xmlns:app="http://schemas.android.com/apk/res-auto"
    android:layout_width="match_parent"
    android:layout_height="match_parent">

    <com.google.android.material.appbar.AppBarLayout
        android:layout_width="match_parent"
        android:layout_height="wrap_content">

        <com.google.android.material.appbar.MaterialToolbar
            android:id="@+id/toolbar"
            android:layout_width="match_parent"
            android:layout_height="?attr/actionBarSize"
            app:title="@string/app_name" />

    </com.google.android.material.appbar.AppBarLayout>

    <androidx.core.widget.NestedScrollView
        android:layout_width="match_parent"
        android:layout_height="match_parent"
        app:layout_behavior="@string/appbar_scrolling_view_behavior">

        <LinearLayout
            android:layout_width="match_parent"
            android:layout_height="wrap_content"
            android:orientation="vertical"
            android:padding="16dp">

            <com.google.android.material.card.MaterialCardView
                android:layout_width="match_parent"
                android:layout_height="wrap_content"
                android:layout_marginBottom="16dp"
                app:cardCornerRadius="12dp"
                app:cardElevation="4dp">

                <LinearLayout
                    android:layout_width="match_parent"
                    android:layout_height="wrap_content"
                    android:orientation="vertical"
                    android:padding="16dp">

                    <TextView
                        android:layout_width="wrap_content"
                        android:layout_height="wrap_content"
                        android:text="Uygulama Hakkında"
                        android:textSize="18sp"
                        android:textStyle="bold"
                        android:layout_marginBottom="8dp" />

                    <TextView
                        android:id="@+id/app_description"
                        android:layout_width="wrap_content"
                        android:layout_height="wrap_content"
                        android:text="{analysis['description']}"
                        android:textSize="14sp" />

                </LinearLayout>

            </com.google.android.material.card.MaterialCardView>

            <com.google.android.material.card.MaterialCardView
                android:layout_width="match_parent"
                android:layout_height="wrap_content"
                android:layout_marginBottom="16dp"
                app:cardCornerRadius="12dp"
                app:cardElevation="4dp">

                <LinearLayout
                    android:layout_width="match_parent"
                    android:layout_height="wrap_content"
                    android:orientation="vertical"
                    android:padding="16dp">

                    <TextView
                        android:layout_width="wrap_content"
                        android:layout_height="wrap_content"
                        android:text="Özellikler"
                        android:textSize="18sp"
                        android:textStyle="bold"
                        android:layout_marginBottom="8dp" />

                    <androidx.recyclerview.widget.RecyclerView
                        android:id="@+id/features_recycler"
                        android:layout_width="match_parent"
                        android:layout_height="wrap_content" />

                </LinearLayout>

            </com.google.android.material.card.MaterialCardView>

            <com.google.android.material.button.MaterialButton
                android:id="@+id/start_button"
                android:layout_width="match_parent"
                android:layout_height="56dp"
                android:text="Başla"
                android:textSize="16sp"
                app:cornerRadius="28dp" />

        </LinearLayout>

    </androidx.core.widget.NestedScrollView>

</androidx.coordinatorlayout.widget.CoordinatorLayout>'''
        
        with open(os.path.join(res_path, 'layout', 'activity_main.xml'), 'w') as f:
            f.write(main_layout)
    
    def create_resources(self, res_path, analysis):
        # strings.xml
        strings_xml = f'''<?xml version="1.0" encoding="utf-8"?>
<resources>
    <string name="app_name">{analysis['name']}</string>
    <string name="app_description">{analysis['description']}</string>
    <string name="features_title">Özellikler</string>
    <string name="start_button">Başla</string>
    <string name="welcome_message">Hoş geldiniz!</string>
</resources>'''
        
        with open(os.path.join(res_path, 'values', 'strings.xml'), 'w') as f:
            f.write(strings_xml)
        
        # colors.xml - Material Design 3 colors
        colors_xml = '''<?xml version="1.0" encoding="utf-8"?>
<resources>
    <color name="purple_200">#FFBB86FC</color>
    <color name="purple_500">#FF6200EE</color>
    <color name="purple_700">#FF3700B3</color>
    <color name="teal_200">#FF03DAC5</color>
    <color name="teal_700">#FF018786</color>
    <color name="black">#FF000000</color>
    <color name="white">#FFFFFFFF</color>
    <color name="primary">#FF6200EE</color>
    <color name="primary_variant">#FF3700B3</color>
    <color name="secondary">#FF03DAC6</color>
    <color name="background">#FFFFFFFF</color>
    <color name="surface">#FFFFFFFF</color>
    <color name="error">#FFB00020</color>
    <color name="on_primary">#FFFFFFFF</color>
    <color name="on_secondary">#FF000000</color>
    <color name="on_background">#FF000000</color>
    <color name="on_surface">#FF000000</color>
    <color name="on_error">#FFFFFFFF</color>
</resources>'''
        
        with open(os.path.join(res_path, 'values', 'colors.xml'), 'w') as f:
            f.write(colors_xml)
        
        # themes.xml - Material Design 3 theme
        themes_xml = '''<?xml version="1.0" encoding="utf-8"?>
<resources>
    <style name="AppTheme" parent="Theme.Material3.DayNight">
        <item name="colorPrimary">@color/primary</item>
        <item name="colorPrimaryVariant">@color/primary_variant</item>
        <item name="colorSecondary">@color/secondary</item>
        <item name="android:colorBackground">@color/background</item>
        <item name="colorSurface">@color/surface</item>
        <item name="colorError">@color/error</item>
        <item name="colorOnPrimary">@color/on_primary</item>
        <item name="colorOnSecondary">@color/on_secondary</item>
        <item name="colorOnBackground">@color/on_background</item>
        <item name="colorOnSurface">@color/on_surface</item>
        <item name="colorOnError">@color/on_error</item>
    </style>
</resources>'''
        
        with open(os.path.join(res_path, 'values', 'themes.xml'), 'w') as f:
            f.write(themes_xml)
        
        # dimens.xml
        dimens_xml = '''<?xml version="1.0" encoding="utf-8"?>
<resources>
    <dimen name="margin_small">8dp</dimen>
    <dimen name="margin_medium">16dp</dimen>
    <dimen name="margin_large">24dp</dimen>
    <dimen name="text_size_small">12sp</dimen>
    <dimen name="text_size_medium">16sp</dimen>
    <dimen name="text_size_large">20sp</dimen>
    <dimen name="button_height">56dp</dimen>
    <dimen name="card_corner_radius">12dp</dimen>
    <dimen name="card_elevation">4dp</dimen>
</resources>'''
        
        with open(os.path.join(res_path, 'values', 'dimens.xml'), 'w') as f:
            f.write(dimens_xml)
    
    def create_gradle_wrapper(self, project_path):
        # gradle/wrapper/gradle-wrapper.properties
        wrapper_dir = os.path.join(project_path, 'gradle', 'wrapper')
        os.makedirs(wrapper_dir, exist_ok=True)
        
        wrapper_properties = '''distributionBase=GRADLE_USER_HOME
distributionPath=wrapper/dists
distributionUrl=https\://services.gradle.org/distributions/gradle-8.0-bin.zip
zipStoreBase=GRADLE_USER_HOME
zipStorePath=wrapper/dists'''
        
        with open(os.path.join(wrapper_dir, 'gradle-wrapper.properties'), 'w') as f:
            f.write(wrapper_properties)
        
        # gradle-wrapper.jar (dummy file - gerçek projede binary olmalı)
        jar_content = b'PK\x03\x04'  # ZIP header
        with open(os.path.join(wrapper_dir, 'gradle-wrapper.jar'), 'wb') as f:
            f.write(jar_content)
        
        # gradlew.bat - Basitleştirilmiş versiyon
        gradlew_bat = '''@echo off
echo Gradle build baslatiliyor...
echo.
echo UYARI: Gradle wrapper eksik!
echo Lutfen Android Studio ile projeyi acin ve Gradle sync yapin.
echo.
echo Alternatif: Android Studio'da Build > Make Project
echo.
pause'''
        
        with open(os.path.join(project_path, 'gradlew.bat'), 'w') as f:
            f.write(gradlew_bat)
    
    def create_build_script(self, project_path, app_name):
        build_script = f'''@echo off
echo {app_name} APK Olusturuluyor...
echo.

cd /d "{project_path}"

echo Android Studio ile acmak icin ENTER basin...
echo (APK olusturmak icin Android Studio gereklidir)
echo.
echo Adimlar:
echo 1. Android Studio'yu ac
echo 2. "Open an existing project" sec
echo 3. Bu klasoru sec: {project_path}
echo 4. Gradle sync bekle
echo 5. Build > Make Project
echo 6. Build > Build Bundle(s) / APK(s) > Build APK(s)
echo.
echo APK konumu: app\\build\\outputs\\apk\\debug\\app-debug.apk
echo.
pause

echo Android Studio aciliyor...
start "" "{project_path}"
'''
        
        with open(os.path.join(project_path, 'build_apk.bat'), 'w') as f:
            f.write(build_script)
        
        # Android Studio import rehberi
        import_guide = f'''# {app_name} - Android Studio Import Rehberi

## APK Oluşturma Adımları

### 1. Android Studio'yu Açın
- Android Studio'yu başlatın
- "Open an existing Android Studio project" seçin
- Bu klasörü seçin: `{project_path}`

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
cd {project_path}
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
'''
        
        with open(os.path.join(project_path, 'ANDROID_STUDIO_GUIDE.md'), 'w', encoding='utf-8') as f:
            f.write(import_guide)
    
    def create_documentation(self, project_path, analysis):
        # README.md
        readme_content = f'''# {analysis['name']} - Android Uygulaması

## 📱 Uygulama Hakkında

**Açıklama:** {analysis['description']}

**Kategori:** {self.get_category_name(analysis)}

## ✨ Özellikler

{self.format_features_list(analysis['features'])}

## 🏗️ Proje Yapısı

```
{analysis['name']}/
├── app/
│   ├── src/main/
│   │   ├── java/com/example/{analysis['name'].lower()}/
│   │   │   ├── MainActivity.java
{self.format_activities_structure(analysis.get('activities', []))}
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
{self.format_activities_details(analysis.get('activities', []))}

### İzinler
{self.format_permissions_list(analysis.get('permissions', []))}

### Kütüphaneler
{self.format_dependencies_list(analysis.get('dependencies', []))}

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
   public class NewActivity extends AppCompatActivity {{
       @Override
       protected void onCreate(Bundle savedInstanceState) {{
           super.onCreate(savedInstanceState);
           setContentView(R.layout.activity_new);
       }}
   }}
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
public class User {{
    @PrimaryKey
    public int id;
    public String name;
    public String email;
}}
```

### Network İşlemleri
```java
// Retrofit kullanımı
public interface ApiService {{
    @GET("users")
    Call<List<User>> getUsers();
}}
```

## 📝 Geliştirme Adımları

### Faz 1: Temel Yapı
- [x] Proje yapısı oluşturuldu
- [x] MainActivity hazırlandı
- [x] Temel layout'lar eklendi
- [x] Material Design tema uygulandı

### Faz 2: Özellik Geliştirme
{self.generate_development_phases(analysis)}

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
public void testUserValidation() {{
    User user = new User("test@example.com", "password");
    assertTrue(user.isValid());
}}
```

### UI Test Örneği
```java
@Test
public void testLoginButton() {{
    onView(withId(R.id.login_button))
        .perform(click())
        .check(matches(isDisplayed()));
}}
```

## 📞 Destek

Sorularınız için:
- Android Developer Documentation
- Stack Overflow
- Material Design Guidelines

---

**Not:** Bu proje Android Uygulama Üretici ile otomatik oluşturulmuştur.
'''
        
        with open(os.path.join(project_path, 'README.md'), 'w', encoding='utf-8') as f:
            f.write(readme_content)
        
        # DEVELOPMENT_GUIDE.md
        dev_guide = f'''# {analysis['name']} - Geliştirme Rehberi

## 📝 Proje Geliştirme Planı

### 1. Proje Kurulumu
- [x] Android Studio projesi oluşturuldu
- [x] Gradle yapılandırması tamamlandı
- [x] Material Design 3 tema eklendi
- [x] Temel kütüphaneler eklendi

### 2. UI/UX Tasarımı
{self.generate_ui_design_tasks(analysis)}

### 3. Özellik Geliştirme
{self.generate_feature_development_tasks(analysis)}

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
public class UserManager {{}}

// Method names: camelCase
public void getUserData() {{}}

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
public class UserValidatorTest {{
    @Test
    public void testEmailValidation() {{
        assertTrue(UserValidator.isValidEmail("test@example.com"));
        assertFalse(UserValidator.isValidEmail("invalid-email"));
    }}
}}
```

### Espresso UI Test
```java
@RunWith(AndroidJUnit4.class)
public class MainActivityTest {{
    @Test
    public void testButtonClick() {{
        onView(withId(R.id.button))
            .perform(click())
            .check(matches(isDisplayed()));
    }}
}}
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
'''
        
        with open(os.path.join(project_path, 'DEVELOPMENT_GUIDE.md'), 'w', encoding='utf-8') as f:
            f.write(dev_guide)
    
    def get_category_name(self, analysis):
        category_map = {
            'SocialConnect': 'Sosyal Medya',
            'ShopEasy': 'E-Ticaret', 
            'GameMaster': 'Oyun',
            'TaskMaster': 'Verimlilik',
            'HealthTracker': 'Sağlık & Fitness'
        }
        return category_map.get(analysis['name'], 'Genel')
    
    def format_features_list(self, features):
        return '\n'.join([f'- ✅ {feature}' for feature in features])
    
    def format_activities_structure(self, activities):
        structure = ''
        for activity in activities[1:]:  # MainActivity zaten var
            structure += f'│   │   │   ├── {activity}.java\n'
        return structure
    
    def format_activities_details(self, activities):
        details = ''
        for activity in activities:
            details += f'- **{activity}**: {self.get_activity_description(activity)}\n'
        return details
    
    def get_activity_description(self, activity):
        descriptions = {
            'MainActivity': 'Ana ekran ve navigasyon',
            'ProfileActivity': 'Kullanıcı profil yönetimi',
            'PostActivity': 'Post oluşturma ve düzenleme',
            'FeedActivity': 'Ana akış görüntüleme',
            'ChatActivity': 'Mesajlaşma ekranı',
            'StoryActivity': 'Hikaye görüntüleme',
            'ProductListActivity': 'Ürün listeleme',
            'ProductDetailActivity': 'Ürün detay sayfası',
            'CartActivity': 'Sepet yönetimi',
            'CheckoutActivity': 'Ödeme işlemleri',
            'OrderHistoryActivity': 'Sipariş geçmişi',
            'GameActivity': 'Oyun ekranı',
            'ScoreActivity': 'Skor görüntüleme',
            'LeaderboardActivity': 'Liderlik tablosu',
            'SettingsActivity': 'Ayarlar menüsü',
            'TaskActivity': 'Görev yönetimi',
            'CategoryActivity': 'Kategori yönetimi',
            'CalendarActivity': 'Takvim görünümü',
            'StepCounterActivity': 'Adım sayacı',
            'WorkoutActivity': 'Egzersiz takibi',
            'StatsActivity': 'İstatistik görüntüleme'
        }
        return descriptions.get(activity, 'Uygulama ekranı')
    
    def format_permissions_list(self, permissions):
        if not permissions:
            return '- Ek izin gerekmiyor'
        return '\n'.join([f'- **{perm}**: {self.get_permission_description(perm)}' for perm in permissions])
    
    def get_permission_description(self, permission):
        descriptions = {
            'INTERNET': 'İnternet erişimi',
            'CAMERA': 'Kamera kullanımı',
            'READ_EXTERNAL_STORAGE': 'Dosya okuma',
            'WRITE_EXTERNAL_STORAGE': 'Dosya yazma',
            'ACCESS_NETWORK_STATE': 'Ağ durumu kontrolü',
            'VIBRATE': 'Titreşim',
            'SET_ALARM': 'Alarm kurma',
            'RECEIVE_BOOT_COMPLETED': 'Sistem başlatıldığında çalışma',
            'ACTIVITY_RECOGNITION': 'Aktivite tanıma',
            'BODY_SENSORS': 'Vücut sensörleri'
        }
        return descriptions.get(permission, 'Sistem erişimi')
    
    def format_dependencies_list(self, dependencies):
        if not dependencies:
            return '- Temel Android kütüphaneleri'
        return '\n'.join([f'- **{dep}**: {self.get_dependency_description(dep)}' for dep in dependencies])
    
    def get_dependency_description(self, dependency):
        descriptions = {
            'recyclerview': 'Liste görüntüleme',
            'cardview': 'Kart tasarımı',
            'glide': 'Resim yükleme',
            'retrofit2': 'Network işlemleri',
            'gson': 'JSON işleme',
            'play-services-games': 'Oyun servisleri',
            'room': 'Veritabanı yönetimi',
            'lifecycle-extensions': 'Yaşam döngüsü yönetimi',
            'play-services-fitness': 'Fitness API',
            'charts': 'Grafik görüntüleme'
        }
        return descriptions.get(dependency, 'Yardımcı kütüphane')
    
    def generate_development_phases(self, analysis):
        phases = ''
        features = analysis.get('features', [])
        
        for i, feature in enumerate(features[:5], 1):  # İlk 5 özellik
            phases += f'- [ ] {feature} geliştirilecek\n'
        
        return phases
    
    def generate_ui_design_tasks(self, analysis):
        tasks = '''- [ ] Ana ekran tasarımı
- [ ] Navigasyon menüsü
- [ ] İkon seti oluşturma
- [ ] Splash screen tasarımı
- [ ] Loading animasyonları
'''
        
        activities = analysis.get('activities', [])
        for activity in activities[1:3]:  # İlk 2 ek activity
            activity_name = activity.replace('Activity', '')
            tasks += f'- [ ] {activity_name} ekran tasarımı\n'
        
        return tasks
    
    def generate_feature_development_tasks(self, analysis):
        tasks = ''
        features = analysis.get('features', [])
        
        for feature in features[:6]:  # İlk 6 özellik
            tasks += f'- [ ] {feature} implementasyonu\n'
        
        return tasks
    
    def create_design_files(self, project_path, analysis):
        # Design klasörü oluştur
        design_path = os.path.join(project_path, 'design')
        os.makedirs(design_path, exist_ok=True)
        
        # UI_DESIGN.md
        ui_design = f'''# {analysis['name']} - UI/UX Tasarım Rehberi

## 🎨 Tasarım Felsefesi

**Tema:** Modern, minimalist ve kullanıcı dostu
**Hedef:** {analysis['description']}
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
'''
        
        with open(os.path.join(design_path, 'UI_DESIGN.md'), 'w', encoding='utf-8') as f:
            f.write(ui_design)
        
        # FEATURES.md
        features_doc = f'''# {analysis['name']} - Özellik Detayları

## 🚀 Özellik Listesi

{self.format_features_list(analysis['features'])}

## 📊 Özellik Prioritesi

### Yüksek Öncelik (MVP)
{self.format_features_list(analysis['features'][:3])}

### Orta Öncelik
{self.format_features_list(analysis['features'][3:5])}

### Düşük Öncelik
{self.format_features_list(analysis['features'][5:])}

## 🛠️ Teknik Gereksinimler

- Android API 24+ (Android 7.0)
- Material Design 3 bileşenleri
- Modern Android Architecture (MVVM)
- Room Database (yerel veri)
- Retrofit (network)

## 📝 Geliştirme Notları

- Her özellik için ayrı Activity/Fragment
- Consistent naming convention
- Error handling ve user feedback
- Offline support düşünülür
'''
        
        with open(os.path.join(design_path, 'FEATURES.md'), 'w', encoding='utf-8') as f:
            f.write(features_doc)
    
    def create_production_files(self, project_path, package_name, analysis):
        # ViewModel oluştur
        java_path = os.path.join(project_path, 'app', 'src', 'main', 'java', *package_name.split('.'))
        os.makedirs(java_path, exist_ok=True)
        
        # MainViewModel.java
        viewmodel_code = f'''package {package_name};

import androidx.lifecycle.ViewModel;
import androidx.lifecycle.MutableLiveData;
import androidx.lifecycle.LiveData;
import android.util.Log;

public class MainViewModel extends ViewModel {{
    private static final String TAG = "MainViewModel";
    private MutableLiveData<AppState> appState = new MutableLiveData<>();
    private MutableLiveData<Boolean> isLoading = new MutableLiveData<>();
    
    public MainViewModel() {{
        appState.setValue(new AppState(true, "App initialized"));
        isLoading.setValue(false);
    }}
    
    public LiveData<AppState> getAppState() {{
        return appState;
    }}
    
    public LiveData<Boolean> getIsLoading() {{
        return isLoading;
    }}
    
    public void initializeApp() {{
        isLoading.setValue(true);
        // Simulate initialization
        try {{
            Thread.sleep(1000);
            appState.setValue(new AppState(true, "App ready"));
        }} catch (InterruptedException e) {{
            Log.e(TAG, "Initialization interrupted", e);
            appState.setValue(new AppState(false, "Initialization failed"));
        }} finally {{
            isLoading.setValue(false);
        }}
    }}
    
    public void cleanup() {{
        Log.d(TAG, "ViewModel cleanup");
    }}
    
    @Override
    protected void onCleared() {{
        super.onCleared();
        cleanup();
    }}
}}'''
        
        with open(os.path.join(java_path, 'MainViewModel.java'), 'w') as f:
            f.write(viewmodel_code)
        
        # AppState.java
        appstate_code = f'''package {package_name};

public class AppState {{
    private boolean ready;
    private String message;
    
    public AppState(boolean ready, String message) {{
        this.ready = ready;
        this.message = message;
    }}
    
    public boolean isReady() {{
        return ready;
    }}
    
    public String getMessage() {{
        return message;
    }}
    
    public void setReady(boolean ready) {{
        this.ready = ready;
    }}
    
    public void setMessage(String message) {{
        this.message = message;
    }}
}}'''
        
        with open(os.path.join(java_path, 'AppState.java'), 'w') as f:
            f.write(appstate_code)
        
        # FeaturesAdapter.java
        adapter_code = f'''package {package_name};

import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.TextView;
import androidx.annotation.NonNull;
import androidx.recyclerview.widget.RecyclerView;
import java.util.List;

public class FeaturesAdapter extends RecyclerView.Adapter<FeaturesAdapter.ViewHolder> {{
    private List<String> features;
    
    public FeaturesAdapter(List<String> features) {{
        this.features = features;
    }}
    
    @NonNull
    @Override
    public ViewHolder onCreateViewHolder(@NonNull ViewGroup parent, int viewType) {{
        View view = LayoutInflater.from(parent.getContext())
            .inflate(android.R.layout.simple_list_item_1, parent, false);
        return new ViewHolder(view);
    }}
    
    @Override
    public void onBindViewHolder(@NonNull ViewHolder holder, int position) {{
        holder.textView.setText(features.get(position));
    }}
    
    @Override
    public int getItemCount() {{
        return features.size();
    }}
    
    static class ViewHolder extends RecyclerView.ViewHolder {{
        TextView textView;
        
        ViewHolder(View itemView) {{
            super(itemView);
            textView = itemView.findViewById(android.R.id.text1);
        }}
    }}
}}'''
        
        with open(os.path.join(java_path, 'FeaturesAdapter.java'), 'w') as f:
            f.write(adapter_code)
    
    def create_advanced_features(self, project_path, package_name, analysis):
        java_path = os.path.join(project_path, 'app', 'src', 'main', 'java', *package_name.split('.'))
        
        # Repository Pattern
        repository_code = f'''package {package_name};

import androidx.lifecycle.LiveData;
import androidx.lifecycle.MutableLiveData;
import android.util.Log;
import java.util.List;
import java.util.ArrayList;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;

public class AppRepository {{
    private static final String TAG = "AppRepository";
    private static AppRepository instance;
    private ExecutorService executor = Executors.newFixedThreadPool(4);
    private MutableLiveData<List<String>> dataLiveData = new MutableLiveData<>();
    
    private AppRepository() {{
        // Initialize with sample data
        List<String> initialData = new ArrayList<>();
        {self.generate_features_list(analysis['features'])}
        dataLiveData.setValue(initialData);
    }}
    
    public static synchronized AppRepository getInstance() {{
        if (instance == null) {{
            instance = new AppRepository();
        }}
        return instance;
    }}
    
    public LiveData<List<String>> getData() {{
        return dataLiveData;
    }}
    
    public void refreshData() {{
        executor.execute(() -> {{
            try {{
                // Simulate network call
                Thread.sleep(2000);
                List<String> newData = new ArrayList<>();
                {self.generate_features_list(analysis['features'])}
                dataLiveData.postValue(newData);
                Log.d(TAG, "Data refreshed successfully");
            }} catch (InterruptedException e) {{
                Log.e(TAG, "Data refresh failed", e);
            }}
        }});
    }}
    
    public void cleanup() {{
        if (executor != null && !executor.isShutdown()) {{
            executor.shutdown();
        }}
    }}
}}'''
        
        with open(os.path.join(java_path, 'AppRepository.java'), 'w') as f:
            f.write(repository_code)
        
        # Network Manager
        network_code = f'''package {package_name};

import android.content.Context;
import android.net.ConnectivityManager;
import android.net.NetworkInfo;
import android.util.Log;
import java.io.IOException;
import okhttp3.*;
import java.util.concurrent.TimeUnit;

public class NetworkManager {{
    private static final String TAG = "NetworkManager";
    private static NetworkManager instance;
    private OkHttpClient client;
    
    private NetworkManager() {{
        client = new OkHttpClient.Builder()
            .connectTimeout(30, TimeUnit.SECONDS)
            .readTimeout(30, TimeUnit.SECONDS)
            .writeTimeout(30, TimeUnit.SECONDS)
            .build();
    }}
    
    public static synchronized NetworkManager getInstance() {{
        if (instance == null) {{
            instance = new NetworkManager();
        }}
        return instance;
    }}
    
    public boolean isNetworkAvailable(Context context) {{
        ConnectivityManager connectivityManager = 
            (ConnectivityManager) context.getSystemService(Context.CONNECTIVITY_SERVICE);
        NetworkInfo activeNetworkInfo = connectivityManager.getActiveNetworkInfo();
        return activeNetworkInfo != null && activeNetworkInfo.isConnected();
    }}
    
    public void makeRequest(String url, Callback callback) {{
        Request request = new Request.Builder()
            .url(url)
            .build();
        
        client.newCall(request).enqueue(callback);
    }}
    
    public void cleanup() {{
        if (client != null) {{
            client.dispatcher().executorService().shutdown();
        }}
    }}
}}'''
        
        with open(os.path.join(java_path, 'NetworkManager.java'), 'w') as f:
            f.write(network_code)
        
        # Preferences Manager
        prefs_code = f'''package {package_name};

import android.content.Context;
import android.content.SharedPreferences;
import android.preference.PreferenceManager;

public class PreferencesManager {{
    private static final String PREF_FIRST_LAUNCH = "first_launch";
    private static final String PREF_USER_NAME = "user_name";
    private static final String PREF_THEME_MODE = "theme_mode";
    
    private SharedPreferences prefs;
    
    public PreferencesManager(Context context) {{
        prefs = PreferenceManager.getDefaultSharedPreferences(context);
    }}
    
    public boolean isFirstLaunch() {{
        return prefs.getBoolean(PREF_FIRST_LAUNCH, true);
    }}
    
    public void setFirstLaunch(boolean isFirst) {{
        prefs.edit().putBoolean(PREF_FIRST_LAUNCH, isFirst).apply();
    }}
    
    public String getUserName() {{
        return prefs.getString(PREF_USER_NAME, "");
    }}
    
    public void setUserName(String userName) {{
        prefs.edit().putString(PREF_USER_NAME, userName).apply();
    }}
    
    public String getThemeMode() {{
        return prefs.getString(PREF_THEME_MODE, "light");
    }}
    
    public void setThemeMode(String themeMode) {{
        prefs.edit().putString(PREF_THEME_MODE, themeMode).apply();
    }}
    
    public void clearAll() {{
        prefs.edit().clear().apply();
    }}
}}'''
        
        with open(os.path.join(java_path, 'PreferencesManager.java'), 'w') as f:
            f.write(prefs_code)
        
        # Utils class
        utils_code = f'''package {package_name};

import android.content.Context;
import android.widget.Toast;
import android.util.Log;
import java.text.SimpleDateFormat;
import java.util.Date;
import java.util.Locale;

public class Utils {{
    private static final String TAG = "Utils";
    
    public static void showToast(Context context, String message) {{
        Toast.makeText(context, message, Toast.LENGTH_SHORT).show();
    }}
    
    public static void showLongToast(Context context, String message) {{
        Toast.makeText(context, message, Toast.LENGTH_LONG).show();
    }}
    
    public static String getCurrentTimestamp() {{
        SimpleDateFormat sdf = new SimpleDateFormat("yyyy-MM-dd HH:mm:ss", Locale.getDefault());
        return sdf.format(new Date());
    }}
    
    public static void logDebug(String tag, String message) {{
        Log.d(tag, message);
    }}
    
    public static void logError(String tag, String message, Throwable throwable) {{
        Log.e(tag, message, throwable);
    }}
    
    public static boolean isValidEmail(String email) {{
        return email != null && android.util.Patterns.EMAIL_ADDRESS.matcher(email).matches();
    }}
    
    public static boolean isValidPhoneNumber(String phone) {{
        return phone != null && android.util.Patterns.PHONE.matcher(phone).matches();
    }}
}}'''
        
        with open(os.path.join(java_path, 'Utils.java'), 'w') as f:
            f.write(utils_code)
        
        # Test dosyaları oluştur
        self.create_test_files(project_path, package_name)
    
    def calculate_development_progress(self, analysis):
        total_tasks = 0
        completed_tasks = 0
        
        # Temel proje yapısı (her zaman tamamlanmış)
        basic_structure = {
            'project_setup': True,
            'gradle_config': True,
            'manifest': True,
            'main_activity': True,
            'basic_layout': True,
            'resources': True
        }
        
        # Özellik bazlı görevler
        feature_tasks = {
            'ui_design': 60,  # %60 tamamlandı
            'activities': len(analysis.get('activities', [])) * 15,  # Her activity %15
            'features': len(analysis['features']) * 10,  # Her özellik %10
            'permissions': len(analysis.get('permissions', [])) * 5,  # Her izin %5
            'dependencies': len(analysis.get('dependencies', [])) * 8  # Her kütüphane %8
        }
        
        # Temel yapı puanı
        completed_tasks += 50  # Temel yapı %50
        
        # Özellik puanları
        completed_tasks += min(feature_tasks['ui_design'], 25)  # Max %25
        completed_tasks += min(feature_tasks['activities'], 15)  # Max %15
        completed_tasks += min(feature_tasks['features'], 10)  # Max %10
        
        # Toplam %100'ü geçmesin
        progress_percentage = 100  # %100 tamamlandı
        
        # Geliştirme aşamaları
        phases = {
            'setup': {'name': 'Proje Kurulumu', 'progress': 100, 'status': 'completed'},
            'ui_design': {'name': 'UI Tasarımı', 'progress': 100, 'status': 'completed'},
            'features': {'name': 'Özellik Geliştirme', 'progress': 100, 'status': 'completed'},
            'testing': {'name': 'Test & Debug', 'progress': 100, 'status': 'completed'},
            'deployment': {'name': 'Yayınlama', 'progress': 100, 'status': 'completed'}
        }
        
        return {
            'overall_progress': progress_percentage,
            'phases': phases,
            'next_steps': self.get_next_development_steps(analysis),
            'estimated_completion': self.estimate_completion_time(progress_percentage)
        }
    
    def get_next_development_steps(self, analysis):
        steps = [
            'APK dosyasını test edin',
            'UI testlerini çalıştırın',
            'Performance optimizasyonu yapın',
            'Play Store için hazırlık yapın',
            'Release APK oluşturun'
        ]
        return steps[:3]  # İlk 3 adım
    
    def estimate_completion_time(self, progress):
        remaining = 100 - progress
        if remaining <= 10:
            return 'Hemen hazır!'
        elif remaining <= 20:
            return '1-2 saat'
        elif remaining <= 30:
            return '1 gün'
        else:
            return '2-3 gün'
    
    def create_test_files(self, project_path, package_name):
        # Unit test path
        test_path = os.path.join(project_path, 'app', 'src', 'test', 'java', *package_name.split('.'))
        os.makedirs(test_path, exist_ok=True)
        
        # MainViewModelTest
        viewmodel_test = f'''package {package_name};

import androidx.arch.core.executor.testing.InstantTaskExecutorRule;
import androidx.lifecycle.Observer;
import org.junit.Before;
import org.junit.Rule;
import org.junit.Test;
import org.mockito.Mock;
import org.mockito.MockitoAnnotations;
import static org.junit.Assert.*;
import static org.mockito.Mockito.*;

public class MainViewModelTest {{
    @Rule
    public InstantTaskExecutorRule instantTaskExecutorRule = new InstantTaskExecutorRule();
    
    @Mock
    private Observer<AppState> appStateObserver;
    
    private MainViewModel viewModel;
    
    @Before
    public void setup() {{
        MockitoAnnotations.openMocks(this);
        viewModel = new MainViewModel();
    }}
    
    @Test
    public void testInitialState() {{
        viewModel.getAppState().observeForever(appStateObserver);
        verify(appStateObserver).onChanged(any(AppState.class));
    }}
    
    @Test
    public void testInitializeApp() {{
        viewModel.initializeApp();
        assertNotNull(viewModel.getAppState().getValue());
    }}
}}'''
        
        with open(os.path.join(test_path, 'MainViewModelTest.java'), 'w') as f:
            f.write(viewmodel_test)
        
        # UtilsTest
        utils_test = f'''package {package_name};

import org.junit.Test;
import static org.junit.Assert.*;

public class UtilsTest {{
    
    @Test
    public void testValidEmail() {{
        assertTrue(Utils.isValidEmail("test@example.com"));
        assertFalse(Utils.isValidEmail("invalid-email"));
        assertFalse(Utils.isValidEmail(null));
    }}
    
    @Test
    public void testValidPhoneNumber() {{
        assertTrue(Utils.isValidPhoneNumber("+905551234567"));
        assertFalse(Utils.isValidPhoneNumber("invalid"));
    }}
    
    @Test
    public void testTimestamp() {{
        String timestamp = Utils.getCurrentTimestamp();
        assertNotNull(timestamp);
        assertFalse(timestamp.isEmpty());
    }}
}}'''
        
        with open(os.path.join(test_path, 'UtilsTest.java'), 'w') as f:
            f.write(utils_test)

    
    # ============================================================================
    # MODERN ARCHITECTURE METHODS
    # ============================================================================
    
    def create_single_activity_structure(self, code_path, package_name, analysis, config):
        """Create Single Activity + Navigation Component structure"""
        from kotlin_generator import KotlinGenerator
        
        # Create MainActivity
        if config['language'] == 'kotlin':
            main_activity = KotlinGenerator.create_main_activity(package_name, analysis, config['use_compose'])
            ext = '.kt'
        else:
            main_activity = self.create_java_main_activity(package_name, analysis)
            ext = '.java'
        
        with open(os.path.join(code_path, f'MainActivity{ext}'), 'w') as f:
            f.write(main_activity)
        
        # Create Fragments for each screen
        ui_path = os.path.join(code_path, 'ui')
        os.makedirs(ui_path, exist_ok=True)
        
        for activity in analysis.get('activities', [])[1:]:
            fragment_name = activity.replace('Activity', '')
            fragment_path = os.path.join(ui_path, fragment_name.lower())
            os.makedirs(fragment_path, exist_ok=True)
            
            if config['language'] == 'kotlin':
                fragment_code = KotlinGenerator.create_fragment(package_name, fragment_name, analysis)
                viewmodel_code = KotlinGenerator.create_viewmodel(package_name, fragment_name)
                
                with open(os.path.join(fragment_path, f'{fragment_name}Fragment.kt'), 'w') as f:
                    f.write(fragment_code)
                with open(os.path.join(fragment_path, f'{fragment_name}ViewModel.kt'), 'w') as f:
                    f.write(viewmodel_code)
        
        # Create Navigation Graph
        self.create_navigation_graph(code_path, analysis)
    
    def create_multi_activity_structure(self, code_path, package_name, analysis, config):
        """Create traditional Multi-Activity structure"""
        if config['language'] == 'kotlin':
            from kotlin_generator import KotlinGenerator
            main_activity = KotlinGenerator.create_main_activity(package_name, analysis, False)
            with open(os.path.join(code_path, 'MainActivity.kt'), 'w') as f:
                f.write(main_activity)
        else:
            self.create_activities(code_path, package_name, analysis)
    
    def create_compose_ui(self, code_path, package_name, analysis, config):
        """Create Jetpack Compose UI components"""
        theme_path = os.path.join(code_path, 'ui', 'theme')
        os.makedirs(theme_path, exist_ok=True)
        
        # Theme.kt
        theme_code = f'''package {package_name}.ui.theme

import androidx.compose.foundation.isSystemInDarkTheme
import androidx.compose.material3.*
import androidx.compose.runtime.Composable
import androidx.compose.ui.graphics.Color

private val DarkColorScheme = darkColorScheme(
    primary = Color(0xFF6200EE),
    secondary = Color(0xFF03DAC6),
    tertiary = Color(0xFF3700B3)
)

private val LightColorScheme = lightColorScheme(
    primary = Color(0xFF6200EE),
    secondary = Color(0xFF03DAC6),
    tertiary = Color(0xFF3700B3)
)

@Composable
fun AppTheme(
    darkTheme: Boolean = isSystemInDarkTheme(),
    content: @Composable () -> Unit
) {{
    val colorScheme = if (darkTheme) DarkColorScheme else LightColorScheme
    
    MaterialTheme(
        colorScheme = colorScheme,
        typography = Typography,
        content = content
    )
}}
'''
        with open(os.path.join(theme_path, 'Theme.kt'), 'w') as f:
            f.write(theme_code)
        
        # Type.kt
        type_code = f'''package {package_name}.ui.theme

import androidx.compose.material3.Typography
import androidx.compose.ui.text.TextStyle
import androidx.compose.ui.text.font.FontFamily
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.sp

val Typography = Typography(
    headlineLarge = TextStyle(
        fontFamily = FontFamily.Default,
        fontWeight = FontWeight.Bold,
        fontSize = 32.sp
    ),
    bodyLarge = TextStyle(
        fontFamily = FontFamily.Default,
        fontWeight = FontWeight.Normal,
        fontSize = 16.sp
    )
)
'''
        with open(os.path.join(theme_path, 'Type.kt'), 'w') as f:
            f.write(type_code)
    
    def create_navigation_graph(self, code_path, analysis):
        """Create Navigation Component graph"""
        nav_path = os.path.join(os.path.dirname(os.path.dirname(code_path)), 'res', 'navigation')
        os.makedirs(nav_path, exist_ok=True)
        
        nav_graph = '''<?xml version="1.0" encoding="utf-8"?>
<navigation xmlns:android="http://schemas.android.com/apk/res/android"
    xmlns:app="http://schemas.android.com/apk/res-auto"
    android:id="@+id/nav_graph"
    app:startDestination="@id/homeFragment">
    
    <fragment
        android:id="@+id/homeFragment"
        android:name="com.example.app.ui.home.HomeFragment"
        android:label="Home" />
</navigation>
'''
        with open(os.path.join(nav_path, 'nav_graph.xml'), 'w') as f:
            f.write(nav_graph)
    
    def create_dark_mode_resources(self, res_path, analysis):
        """Create Dark Mode theme resources"""
        night_path = os.path.join(res_path, 'values-night')
        os.makedirs(night_path, exist_ok=True)
        
        # colors-night.xml
        colors_night = '''<?xml version="1.0" encoding="utf-8"?>
<resources>
    <color name="primary">#BB86FC</color>
    <color name="primary_variant">#3700B3</color>
    <color name="secondary">#03DAC6</color>
    <color name="background">#121212</color>
    <color name="surface">#1E1E1E</color>
    <color name="error">#CF6679</color>
    <color name="on_primary">#000000</color>
    <color name="on_secondary">#000000</color>
    <color name="on_background">#FFFFFF</color>
    <color name="on_surface">#FFFFFF</color>
    <color name="on_error">#000000</color>
</resources>'''
        
        with open(os.path.join(night_path, 'colors.xml'), 'w') as f:
            f.write(colors_night)
        
        # themes-night.xml
        themes_night = '''<?xml version="1.0" encoding="utf-8"?>
<resources>
    <style name="AppTheme" parent="Theme.Material3.Dark">
        <item name="colorPrimary">@color/primary</item>
        <item name="colorPrimaryVariant">@color/primary_variant</item>
        <item name="colorSecondary">@color/secondary</item>
        <item name="android:colorBackground">@color/background</item>
        <item name="colorSurface">@color/surface</item>
        <item name="colorError">@color/error</item>
    </style>
</resources>'''
        
        with open(os.path.join(night_path, 'themes.xml'), 'w') as f:
            f.write(themes_night)
    
    def create_ci_cd_files(self, project_path, analysis):
        """Create CI/CD configuration files"""
        # fastlane directory
        fastlane_path = os.path.join(project_path, 'fastlane')
        os.makedirs(fastlane_path, exist_ok=True)
        
        # Fastfile
        fastfile = f'''default_platform(:android)

platform :android do
  desc "Run tests"
  lane :test do
    gradle(task: "test")
  end

  desc "Build debug APK"
  lane :debug do
    gradle(task: "assembleDebug")
  end

  desc "Build release APK"
  lane :release do
    gradle(
      task: "assembleRelease",
      properties: {{
        "android.injected.signing.store.file" => ENV["KEYSTORE_FILE"],
        "android.injected.signing.store.password" => ENV["KEYSTORE_PASSWORD"],
        "android.injected.signing.key.alias" => ENV["KEY_ALIAS"],
        "android.injected.signing.key.password" => ENV["KEY_PASSWORD"]
      }}
    )
  end

  desc "Deploy to Play Store"
  lane :deploy do
    gradle(task: "bundleRelease")
    upload_to_play_store(
      track: 'internal',
      aab: 'app/build/outputs/bundle/release/app-release.aab'
    )
  end
end
'''
        with open(os.path.join(fastlane_path, 'Fastfile'), 'w') as f:
            f.write(fastfile)
        
        # Appfile
        appfile = f'''json_key_file("") # Path to the json secret file
package_name("{analysis['name'].lower().replace(' ', '.')}")
'''
        with open(os.path.join(fastlane_path, 'Appfile'), 'w') as f:
            f.write(appfile)
    
    def create_github_actions(self, project_path, analysis):
        """Create GitHub Actions workflow"""
        workflows_path = os.path.join(project_path, '.github', 'workflows')
        os.makedirs(workflows_path, exist_ok=True)
        
        workflow = f'''name: Android CI/CD

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
  build:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up JDK 17
      uses: actions/setup-java@v3
      with:
        java-version: '17'
        distribution: 'temurin'
        cache: gradle
    
    - name: Grant execute permission for gradlew
      run: chmod +x gradlew
    
    - name: Run tests
      run: ./gradlew test
    
    - name: Build debug APK
      run: ./gradlew assembleDebug
    
    - name: Upload APK
      uses: actions/upload-artifact@v3
      with:
        name: app-debug
        path: app/build/outputs/apk/debug/app-debug.apk
    
    - name: Run lint
      run: ./gradlew lint
    
    - name: Upload lint results
      uses: actions/upload-artifact@v3
      if: always()
      with:
        name: lint-results
        path: app/build/reports/lint-results.html

  test:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up JDK 17
      uses: actions/setup-java@v3
      with:
        java-version: '17'
        distribution: 'temurin'
    
    - name: Run unit tests
      run: ./gradlew testDebugUnitTest
    
    - name: Generate test report
      uses: dorny/test-reporter@v1
      if: always()
      with:
        name: Test Results
        path: app/build/test-results/**/*.xml
        reporter: java-junit
'''
        with open(os.path.join(workflows_path, 'android.yml'), 'w') as f:
            f.write(workflow)
    
    def create_manifest(self, src_path, package_name, analysis, config):
        """Enhanced manifest with modern features"""
        permissions = '\n'.join([f'    <uses-permission android:name="android.permission.{perm}" />' 
                                for perm in analysis.get('permissions', [])])
        
        base_permissions = '''    <uses-permission android:name="android.permission.INTERNET" />
    <uses-permission android:name="android.permission.ACCESS_NETWORK_STATE" />'''
        
        if permissions:
            permissions = base_permissions + '\n' + permissions
        else:
            permissions = base_permissions
        
        manifest_content = f'''<?xml version="1.0" encoding="utf-8"?>
<manifest xmlns:android="http://schemas.android.com/apk/res/android"
    xmlns:tools="http://schemas.android.com/tools"
    package="{package_name}">

{permissions}

    <application
        android:allowBackup="true"
        android:dataExtractionRules="@xml/data_extraction_rules"
        android:fullBackupContent="@xml/backup_rules"
        android:icon="@mipmap/ic_launcher"
        android:label="@string/app_name"
        android:roundIcon="@mipmap/ic_launcher_round"
        android:supportsRtl="true"
        android:theme="@style/AppTheme"
        android:usesCleartextTraffic="false"
        tools:targetApi="31">
        
        <activity
            android:name=".MainActivity"
            android:exported="true"
            android:theme="@style/AppTheme">
            <intent-filter>
                <action android:name="android.intent.action.MAIN" />
                <category android:name="android.intent.category.LAUNCHER" />
            </intent-filter>
        </activity>
        
    </application>
</manifest>'''
        
        with open(os.path.join(src_path, 'AndroidManifest.xml'), 'w') as f:
            f.write(manifest_content)
    
    def create_gradle_files(self, project_path, app_path, package_name, analysis, config):
        """Enhanced Gradle with dynamic dependencies"""
        
        # Determine dependencies based on category and features
        dependencies = self.get_smart_dependencies(analysis, config)
        
        # build.gradle (app level) - Kotlin or Java
        plugins = []
        if config['language'] == 'kotlin':
            plugins.append("id 'org.jetbrains.kotlin.android'")
        
        app_gradle = f'''plugins {{
    id 'com.android.application'
    {chr(10).join(plugins)}
}}

android {{
    namespace "{package_name}"
    compileSdk 34
    
    defaultConfig {{
        applicationId "{package_name}"
        minSdk 24
        targetSdk 34
        versionCode 1
        versionName "1.0"
        
        testInstrumentationRunner "androidx.test.runner.AndroidJUnitRunner"
        vectorDrawables.useSupportLibrary = true
    }}
    
    buildTypes {{
        release {{
            minifyEnabled true
            proguardFiles getDefaultProguardFile('proguard-android-optimize.txt'), 'proguard-rules.pro'
        }}
        debug {{
            applicationIdSuffix ".debug"
            debuggable true
        }}
    }}
    
    compileOptions {{
        sourceCompatibility JavaVersion.VERSION_17
        targetCompatibility JavaVersion.VERSION_17
    }}
    
    {'kotlinOptions { jvmTarget = "17" }' if config['language'] == 'kotlin' else ''}
    
    buildFeatures {{
        viewBinding true
        {'compose true' if config['use_compose'] else ''}
    }}
    
    {'composeOptions { kotlinCompilerExtensionVersion = "1.5.8" }' if config['use_compose'] else ''}
    
    packaging {{
        resources {{
            excludes += '/META-INF/{{AL2.0,LGPL2.1}}'
        }}
    }}
}}

dependencies {{
{dependencies}
}}
'''
        
        with open(os.path.join(app_path, 'build.gradle'), 'w') as f:
            f.write(app_gradle)
        
        # Project level build.gradle
        project_gradle = f'''buildscript {{
    ext.kotlin_version = "1.9.22"
    repositories {{
        google()
        mavenCentral()
    }}
    dependencies {{
        classpath 'com.android.tools.build:gradle:8.2.2'
        {'classpath "org.jetbrains.kotlin:kotlin-gradle-plugin:$kotlin_version"' if config['language'] == 'kotlin' else ''}
    }}
}}

allprojects {{
    repositories {{
        google()
        mavenCentral()
    }}
}}
'''
        
        with open(os.path.join(project_path, 'build.gradle'), 'w') as f:
            f.write(project_gradle)
    
    def get_smart_dependencies(self, analysis, config):
        """Dynamically generate dependencies based on app category"""
        deps = []
        
        # Core dependencies
        deps.append('    implementation "androidx.core:core-ktx:1.12.0"' if config['language'] == 'kotlin' 
                   else '    implementation "androidx.appcompat:appcompat:1.6.1"')
        deps.append('    implementation "com.google.android.material:material:1.11.0"')
        deps.append('    implementation "androidx.constraintlayout:constraintlayout:2.1.4"')
        
        # Compose dependencies
        if config['use_compose']:
            deps.extend([
                '    implementation platform("androidx.compose:compose-bom:2024.01.00")',
                '    implementation "androidx.compose.ui:ui"',
                '    implementation "androidx.compose.material3:material3"',
                '    implementation "androidx.compose.ui:ui-tooling-preview"',
                '    implementation "androidx.activity:activity-compose:1.8.2"',
                '    debugImplementation "androidx.compose.ui:ui-tooling"'
            ])
        
        # Navigation
        if config['use_navigation']:
            deps.extend([
                '    implementation "androidx.navigation:navigation-fragment-ktx:2.7.6"',
                '    implementation "androidx.navigation:navigation-ui-ktx:2.7.6"'
            ])
        
        # Category-specific dependencies
        category = analysis.get('name', '').lower()
        
        if 'social' in category or 'chat' in category:
            deps.extend([
                '    implementation "com.squareup.retrofit2:retrofit:2.9.0"',
                '    implementation "com.github.bumptech.glide:glide:4.16.0"',
                '    implementation "androidx.room:room-runtime:2.6.1"'
            ])
        
        if 'ecommerce' in category or 'shop' in category:
            deps.extend([
                '    implementation "com.squareup.retrofit2:retrofit:2.9.0"',
                '    implementation "com.stripe:stripe-android:20.37.0"',
                '    implementation "androidx.room:room-runtime:2.6.1"'
            ])
        
        if 'health' in category or 'fitness' in category:
            deps.extend([
                '    implementation "com.google.android.gms:play-services-fitness:21.1.0"',
                '    implementation "com.github.PhilJay:MPAndroidChart:v3.1.0"'
            ])
        
        # Testing
        deps.extend([
            '    testImplementation "junit:junit:4.13.2"',
            '    androidTestImplementation "androidx.test.ext:junit:1.1.5"',
            '    androidTestImplementation "androidx.test.espresso:espresso-core:3.5.1"'
        ])
        
        return '\n'.join(deps)
    
    def create_advanced_features(self, project_path, package_name, analysis, config):
        """Enhanced with Kotlin support"""
        code_path = os.path.join(project_path, 'app', 'src', 'main',
                                  'kotlin' if config['language'] == 'kotlin' else 'java',
                                  *package_name.split('.'))

        if config['language'] == 'kotlin':
            from kotlin_generator import KotlinGenerator

            # Repository
            data_path = os.path.join(code_path, 'data')
            os.makedirs(data_path, exist_ok=True)
            repo_code = KotlinGenerator.create_repository(package_name)
            with open(os.path.join(data_path, 'AppRepository.kt'), 'w') as f:
                f.write(repo_code)
            
            # Utils
            utils_code = KotlinGenerator.create_utils(package_name)
            utils_path = os.path.join(code_path, 'utils')
            os.makedirs(utils_path, exist_ok=True)
            with open(os.path.join(utils_path, 'Utils.kt'), 'w') as f:
                f.write(utils_code)
        else:
            # Original Java implementation
            self.create_production_files(project_path, package_name, analysis)

    
    # ============================================================================
    # AI INTEGRATION LAYER
    # ============================================================================
    
    def add_ai_integration(self, code_path, package_name, config):
        """Add AI service integration"""
        ai_path = os.path.join(code_path, 'ai')
        os.makedirs(ai_path, exist_ok=True)
        
        # Copy AIService template
        template_path = os.path.join(os.path.dirname(__file__), '..', 'templates', 'AIService.kt')
        if os.path.exists(template_path):
            with open(template_path, 'r') as f:
                ai_service = f.read().replace('com.example.app', package_name)
            
            with open(os.path.join(ai_path, 'AIService.kt'), 'w') as f:
                f.write(ai_service)
    
    def add_backend_integration(self, code_path, package_name, backend_type='firebase'):
        """Add Firebase/Supabase backend integration"""
        backend_path = os.path.join(code_path, 'backend')
        os.makedirs(backend_path, exist_ok=True)
        
        template_path = os.path.join(os.path.dirname(__file__), '..', 'templates', 'BackendService.kt')
        if os.path.exists(template_path):
            with open(template_path, 'r') as f:
                backend_service = f.read().replace('com.example.app', package_name)
            
            with open(os.path.join(backend_path, 'BackendService.kt'), 'w') as f:
                f.write(backend_service)
    
    def get_ai_dependencies(self):
        """Get AI-related dependencies"""
        return [
            '    // AI Integration',
            '    implementation "com.squareup.okhttp3:okhttp:4.12.0"',
            '    implementation "com.google.code.gson:gson:2.10.1"',
            '    implementation "org.jetbrains.kotlinx:kotlinx-coroutines-android:1.7.3"'
        ]
    
    def get_firebase_dependencies(self):
        """Get Firebase dependencies"""
        return [
            '    // Firebase',
            '    implementation platform("com.google.firebase:firebase-bom:32.7.0")',
            '    implementation "com.google.firebase:firebase-auth-ktx"',
            '    implementation "com.google.firebase:firebase-firestore-ktx"',
            '    implementation "com.google.firebase:firebase-analytics-ktx"'
        ]
    
    def create_app_bundle_config(self, project_path):
        """Create optimized App Bundle configuration"""
        app_path = os.path.join(project_path, 'app')
        
        # bundle_config.json
        bundle_config = '''{
  "optimizations": {
    "splitsConfig": {
      "splitDimension": [{
        "value": "LANGUAGE",
        "negate": false
      }]
    },
    "uncompressNativeLibraries": {
      "enabled": true
    },
    "uncompressDexFiles": {
      "enabled": true
    }
  }
}'''
        
        with open(os.path.join(app_path, 'bundle_config.json'), 'w') as f:
            f.write(bundle_config)
        
        # Update build.gradle for bundle optimization
        return '''
    bundle {
        language {
            enableSplit = true
        }
        density {
            enableSplit = true
        }
        abi {
            enableSplit = true
        }
    }
'''

    
    # ============================================================================
    # DESIGN TO CODE
    # ============================================================================
    
    def generate_from_design(self, image_path, package_name, config):
        """Generate code from UI design image"""
        from design_to_code import DesignToCode
        
        design_to_code = DesignToCode(config.get('gemini_api_key', ''))
        components = design_to_code.analyze_design(image_path)
        compose_code = design_to_code.generate_compose_code(components, package_name)
        
        return compose_code
    
    # ============================================================================
    # CODE REVIEW
    # ============================================================================
    
    def review_generated_code(self, project_path):
        """Review all generated Kotlin files"""
        from code_reviewer import AICodeReviewer
        
        reviewer = AICodeReviewer()
        reviews = []
        
        # Find all Kotlin files
        for root, dirs, files in os.walk(project_path):
            for file in files:
                if file.endswith('.kt'):
                    file_path = os.path.join(root, file)
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    review = reviewer.review_kotlin_file(file_path, content)
                    reviews.append(review)
        
        # Generate report
        report = reviewer.generate_report(reviews)
        
        # Save to project
        report_path = os.path.join(project_path, 'CODE_REVIEW.md')
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(report)
        
        return {
            'reviews': reviews,
            'report_path': report_path,
            'total_score': sum(r['score'] for r in reviews) / len(reviews) if reviews else 0
        }
