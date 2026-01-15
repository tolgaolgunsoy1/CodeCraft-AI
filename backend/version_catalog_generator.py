# Version Catalog Generator - Modern Dependency Management

class VersionCatalogGenerator:
    """Generate libs.versions.toml for centralized dependency management"""
    
    @staticmethod
    def generate_version_catalog(category='general'):
        """Generate version catalog based on app category"""
        
        versions = {
            'kotlin': '1.9.22',
            'compose': '1.6.0',
            'compose_bom': '2024.01.00',
            'material3': '1.2.0',
            'androidx_core': '1.12.0',
            'lifecycle': '2.7.0',
            'navigation': '2.7.6',
            'room': '2.6.1',
            'retrofit': '2.9.0',
            'okhttp': '4.12.0',
            'coil': '2.5.0',
            'timber': '5.0.1',
            'coroutines': '1.7.3',
            'hilt': '2.50',
            'firebase_bom': '32.7.0'
        }
        
        # Category-specific versions
        if category == 'finance':
            versions.update({
                'mpandroidchart': '3.1.0',
                'vico': '1.13.1',  # Modern chart library
                'stripe': '20.37.0'
            })
        elif category == 'social':
            versions.update({
                'glide': '4.16.0',
                'exoplayer': '2.19.1'
            })
        
        catalog = f'''[versions]
kotlin = "{versions['kotlin']}"
compose-bom = "{versions['compose_bom']}"
androidx-core = "{versions['androidx_core']}"
lifecycle = "{versions['lifecycle']}"
navigation = "{versions['navigation']}"
room = "{versions['room']}"
retrofit = "{versions['retrofit']}"
okhttp = "{versions['okhttp']}"
coil = "{versions['coil']}"
timber = "{versions['timber']}"
coroutines = "{versions['coroutines']}"
hilt = "{versions['hilt']}"
firebase-bom = "{versions['firebase_bom']}"

[libraries]
# Kotlin
kotlin-stdlib = {{ module = "org.jetbrains.kotlin:kotlin-stdlib", version.ref = "kotlin" }}
kotlinx-coroutines-android = {{ module = "org.jetbrains.kotlinx:kotlinx-coroutines-android", version.ref = "coroutines" }}

# Compose
compose-bom = {{ module = "androidx.compose:compose-bom", version.ref = "compose-bom" }}
compose-ui = {{ module = "androidx.compose.ui:ui" }}
compose-material3 = {{ module = "androidx.compose.material3:material3" }}
compose-ui-tooling = {{ module = "androidx.compose.ui:ui-tooling" }}
compose-ui-tooling-preview = {{ module = "androidx.compose.ui:ui-tooling-preview" }}

# AndroidX
androidx-core-ktx = {{ module = "androidx.core:core-ktx", version.ref = "androidx-core" }}
androidx-lifecycle-runtime = {{ module = "androidx.lifecycle:lifecycle-runtime-ktx", version.ref = "lifecycle" }}
androidx-lifecycle-viewmodel = {{ module = "androidx.lifecycle:lifecycle-viewmodel-ktx", version.ref = "lifecycle" }}
androidx-activity-compose = {{ module = "androidx.activity:activity-compose", version = "1.8.2" }}

# Navigation
navigation-compose = {{ module = "androidx.navigation:navigation-compose", version.ref = "navigation" }}

# Room
room-runtime = {{ module = "androidx.room:room-runtime", version.ref = "room" }}
room-ktx = {{ module = "androidx.room:room-ktx", version.ref = "room" }}
room-compiler = {{ module = "androidx.room:room-compiler", version.ref = "room" }}

# Network
retrofit = {{ module = "com.squareup.retrofit2:retrofit", version.ref = "retrofit" }}
retrofit-gson = {{ module = "com.squareup.retrofit2:converter-gson", version.ref = "retrofit" }}
okhttp = {{ module = "com.squareup.okhttp3:okhttp", version.ref = "okhttp" }}
okhttp-logging = {{ module = "com.squareup.okhttp3:logging-interceptor", version.ref = "okhttp" }}

# Image Loading
coil-compose = {{ module = "io.coil-kt:coil-compose", version.ref = "coil" }}

# Logging
timber = {{ module = "com.jakewharton.timber:timber", version.ref = "timber" }}

# Dependency Injection
hilt-android = {{ module = "com.google.dagger:hilt-android", version.ref = "hilt" }}
hilt-compiler = {{ module = "com.google.dagger:hilt-compiler", version.ref = "hilt" }}

# Firebase
firebase-bom = {{ module = "com.google.firebase:firebase-bom", version.ref = "firebase-bom" }}
firebase-auth = {{ module = "com.google.firebase:firebase-auth-ktx" }}
firebase-firestore = {{ module = "com.google.firebase:firebase-firestore-ktx" }}
firebase-analytics = {{ module = "com.google.firebase:firebase-analytics-ktx" }}

[bundles]
compose = ["compose-ui", "compose-material3", "compose-ui-tooling-preview"]
lifecycle = ["androidx-lifecycle-runtime", "androidx-lifecycle-viewmodel"]
room = ["room-runtime", "room-ktx"]
retrofit = ["retrofit", "retrofit-gson", "okhttp", "okhttp-logging"]
firebase = ["firebase-auth", "firebase-firestore", "firebase-analytics"]

[plugins]
android-application = {{ id = "com.android.application", version = "8.2.2" }}
kotlin-android = {{ id = "org.jetbrains.kotlin.android", version.ref = "kotlin" }}
hilt = {{ id = "com.google.dagger.hilt.android", version.ref = "hilt" }}
'''
        
        return catalog
    
    @staticmethod
    def generate_gradle_with_catalog(package_name, use_compose=True):
        """Generate build.gradle using version catalog"""
        
        return f'''plugins {{
    alias(libs.plugins.android.application)
    alias(libs.plugins.kotlin.android)
    alias(libs.plugins.hilt)
    kotlin("kapt")
}}

android {{
    namespace = "{package_name}"
    compileSdk = 34
    
    defaultConfig {{
        applicationId = "{package_name}"
        minSdk = 24
        targetSdk = 34
        versionCode = 1
        versionName = "1.0"
        
        testInstrumentationRunner = "androidx.test.runner.AndroidJUnitRunner"
        vectorDrawables.useSupportLibrary = true
    }}
    
    buildTypes {{
        release {{
            isMinifyEnabled = true
            proguardFiles(
                getDefaultProguardFile("proguard-android-optimize.txt"),
                "proguard-rules.pro"
            )
        }}
    }}
    
    compileOptions {{
        sourceCompatibility = JavaVersion.VERSION_17
        targetCompatibility = JavaVersion.VERSION_17
    }}
    
    kotlinOptions {{
        jvmTarget = "17"
    }}
    
    buildFeatures {{
        compose = {str(use_compose).lower()}
        viewBinding = true
    }}
    
    composeOptions {{
        kotlinCompilerExtensionVersion = "1.5.8"
    }}
    
    packaging {{
        resources {{
            excludes += "/META-INF/{{AL2.0,LGPL2.1}}"
        }}
    }}
}}

dependencies {{
    // Kotlin
    implementation(libs.kotlin.stdlib)
    implementation(libs.kotlinx.coroutines.android)
    
    // AndroidX Core
    implementation(libs.androidx.core.ktx)
    implementation(libs.bundles.lifecycle)
    
    // Compose
    implementation(platform(libs.compose.bom))
    implementation(libs.bundles.compose)
    implementation(libs.androidx.activity.compose)
    implementation(libs.navigation.compose)
    debugImplementation(libs.compose.ui.tooling)
    
    // Room Database
    implementation(libs.bundles.room)
    kapt(libs.room.compiler)
    
    // Network
    implementation(libs.bundles.retrofit)
    
    // Image Loading
    implementation(libs.coil.compose)
    
    // Logging
    implementation(libs.timber)
    
    // Dependency Injection
    implementation(libs.hilt.android)
    kapt(libs.hilt.compiler)
    
    // Firebase
    implementation(platform(libs.firebase.bom))
    implementation(libs.bundles.firebase)
    
    // Testing
    testImplementation("junit:junit:4.13.2")
    androidTestImplementation("androidx.test.ext:junit:1.1.5")
    androidTestImplementation("androidx.test.espresso:espresso-core:3.5.1")
}}
'''
