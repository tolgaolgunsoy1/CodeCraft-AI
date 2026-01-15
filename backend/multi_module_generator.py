# Multi-Module Architecture Generator - Enterprise Scalability

class MultiModuleGenerator:
    """Generate feature-based multi-module Android projects"""
    
    @staticmethod
    def generate_module_structure(app_name: str, features: list):
        """Generate complete multi-module structure"""
        return {
            'root': {
                'settings.gradle.kts': MultiModuleGenerator.generate_settings_gradle(features),
                'build.gradle.kts': MultiModuleGenerator.generate_root_build_gradle(),
                'gradle.properties': MultiModuleGenerator.generate_gradle_properties()
            },
            'app': {
                'build.gradle.kts': MultiModuleGenerator.generate_app_module(),
                'src/main/kotlin/': 'Main app module'
            },
            'core': {
                'common': MultiModuleGenerator.generate_core_common(),
                'network': MultiModuleGenerator.generate_core_network(),
                'database': MultiModuleGenerator.generate_core_database(),
                'ui': MultiModuleGenerator.generate_core_ui(),
                'testing': MultiModuleGenerator.generate_core_testing()
            },
            'feature': {
                feature: MultiModuleGenerator.generate_feature_module(feature)
                for feature in features
            }
        }
    
    @staticmethod
    def generate_settings_gradle(features: list):
        """Generate settings.gradle.kts with all modules"""
        modules = ['app'] + \
                 [f'core:{m}' for m in ['common', 'network', 'database', 'ui', 'testing']] + \
                 [f'feature:{f}' for f in features]
        
        return f'''pluginManagement {{
    repositories {{
        google()
        mavenCentral()
        gradlePluginPortal()
    }}
}}

dependencyResolutionManagement {{
    repositoriesMode.set(RepositoriesMode.FAIL_ON_PROJECT_REPOS)
    repositories {{
        google()
        mavenCentral()
    }}
}}

rootProject.name = "TitanFinance"

// Core modules
include(":app")
include(":core:common")
include(":core:network")
include(":core:database")
include(":core:ui")
include(":core:testing")

// Feature modules
{chr(10).join([f'include(":feature:{f}")' for f in features])}
'''
    
    @staticmethod
    def generate_root_build_gradle():
        """Generate root build.gradle.kts"""
        return '''// Top-level build file
plugins {
    alias(libs.plugins.android.application) apply false
    alias(libs.plugins.kotlin.android) apply false
    alias(libs.plugins.ksp) apply false
    alias(libs.plugins.hilt) apply false
    alias(libs.plugins.android.library) apply false
}

tasks.register("clean", Delete::class) {
    delete(rootProject.buildDir)
}
'''
    
    @staticmethod
    def generate_gradle_properties():
        """Generate gradle.properties with optimization"""
        return '''# Project-wide Gradle settings
org.gradle.jvmargs=-Xmx4096m -Dfile.encoding=UTF-8
org.gradle.parallel=true
org.gradle.caching=true
org.gradle.configureondemand=true

# AndroidX
android.useAndroidX=true
android.enableJetifier=true

# Kotlin
kotlin.code.style=official
kotlin.incremental=true
kotlin.incremental.java=true

# Build optimization
android.nonTransitiveRClass=true
android.nonFinalResIds=true
'''
    
    @staticmethod
    def generate_core_common():
        """Generate :core:common module"""
        return {
            'build.gradle.kts': '''plugins {
    alias(libs.plugins.android.library)
    alias(libs.plugins.kotlin.android)
}

android {
    namespace = "com.titan.finance.core.common"
    compileSdk = 34
    
    defaultConfig {
        minSdk = 26
    }
    
    compileOptions {
        sourceCompatibility = JavaVersion.VERSION_17
        targetCompatibility = JavaVersion.VERSION_17
    }
}

dependencies {
    implementation(libs.kotlin.stdlib)
    implementation(libs.kotlinx.coroutines.android)
    
    // Testing
    testImplementation(libs.junit)
}
''',
            'src/main/kotlin/Result.kt': '''package com.titan.finance.core.common

// AI Architecture Note: Sealed class for type-safe result handling
// This pattern ensures compile-time safety and exhaustive when expressions
sealed class Result<out T> {
    data class Success<T>(val data: T) : Result<T>()
    data class Error(val exception: Throwable) : Result<Nothing>()
    object Loading : Result<Nothing>()
    
    // AI Note: Extension functions for functional programming style
    inline fun <R> map(transform: (T) -> R): Result<R> = when (this) {
        is Success -> Success(transform(data))
        is Error -> Error(exception)
        is Loading -> Loading
    }
    
    inline fun onSuccess(action: (T) -> Unit): Result<T> {
        if (this is Success) action(data)
        return this
    }
    
    inline fun onError(action: (Throwable) -> Unit): Result<T> {
        if (this is Error) action(exception)
        return this
    }
}
'''
        }
    
    @staticmethod
    def generate_core_network():
        """Generate :core:network module"""
        return {
            'build.gradle.kts': '''plugins {
    alias(libs.plugins.android.library)
    alias(libs.plugins.kotlin.android)
    alias(libs.plugins.ksp)
    alias(libs.plugins.hilt)
}

android {
    namespace = "com.titan.finance.core.network"
    compileSdk = 34
    
    defaultConfig {
        minSdk = 26
        
        buildConfigField("String", "API_BASE_URL", "\\"https://api.binance.com\\"")
    }
    
    buildFeatures {
        buildConfig = true
    }
}

dependencies {
    implementation(project(":core:common"))
    
    implementation(libs.bundles.network)
    implementation(libs.hilt.android)
    ksp(libs.hilt.compiler)
    ksp(libs.moshi.codegen)
}
''',
            'src/main/kotlin/NetworkModule.kt': '''package com.titan.finance.core.network

import dagger.Module
import dagger.Provides
import dagger.hilt.InstallIn
import dagger.hilt.components.SingletonComponent
import okhttp3.OkHttpClient
import okhttp3.logging.HttpLoggingInterceptor
import retrofit2.Retrofit
import retrofit2.converter.moshi.MoshiConverterFactory
import java.util.concurrent.TimeUnit
import javax.inject.Singleton

// AI Architecture Note: Hilt module for network dependencies
// Singleton scope ensures single instance across app lifecycle
@Module
@InstallIn(SingletonComponent::class)
object NetworkModule {
    
    @Provides
    @Singleton
    fun provideOkHttpClient(): OkHttpClient {
        // AI Note: Logging interceptor for debugging (remove in production)
        val loggingInterceptor = HttpLoggingInterceptor().apply {
            level = if (BuildConfig.DEBUG) 
                HttpLoggingInterceptor.Level.BODY 
            else 
                HttpLoggingInterceptor.Level.NONE
        }
        
        return OkHttpClient.Builder()
            .addInterceptor(loggingInterceptor)
            .connectTimeout(30, TimeUnit.SECONDS)
            .readTimeout(30, TimeUnit.SECONDS)
            .writeTimeout(30, TimeUnit.SECONDS)
            .build()
    }
    
    @Provides
    @Singleton
    fun provideRetrofit(okHttpClient: OkHttpClient): Retrofit {
        return Retrofit.Builder()
            .baseUrl(BuildConfig.API_BASE_URL)
            .client(okHttpClient)
            .addConverterFactory(MoshiConverterFactory.create())
            .build()
    }
}
'''
        }
    
    @staticmethod
    def generate_core_ui():
        """Generate :core:ui module with Design System"""
        return {
            'build.gradle.kts': '''plugins {
    alias(libs.plugins.android.library)
    alias(libs.plugins.kotlin.android)
}

android {
    namespace = "com.titan.finance.core.ui"
    compileSdk = 34
    
    defaultConfig {
        minSdk = 26
    }
    
    buildFeatures {
        compose = true
    }
    
    composeOptions {
        kotlinCompilerExtensionVersion = libs.versions.compose.compiler.get()
    }
}

dependencies {
    implementation(project(":core:common"))
    
    implementation(platform(libs.compose.bom))
    implementation(libs.bundles.compose)
    implementation(libs.coil.compose)
}
''',
            'src/main/kotlin/theme/Theme.kt': '''package com.titan.finance.core.ui.theme

import androidx.compose.foundation.isSystemInDarkTheme
import androidx.compose.material3.*
import androidx.compose.runtime.Composable
import androidx.compose.ui.graphics.Color

// AI Architecture Note: Design System with Material 3
// Centralized theming ensures consistency across all features

private val LightColorScheme = lightColorScheme(
    primary = Color(0xFF6200EE),
    onPrimary = Color.White,
    primaryContainer = Color(0xFFBB86FC),
    secondary = Color(0xFF03DAC6),
    onSecondary = Color.Black,
    background = Color(0xFFFFFBFE),
    surface = Color(0xFFFFFBFE),
    error = Color(0xFFB00020)
)

private val DarkColorScheme = darkColorScheme(
    primary = Color(0xFFBB86FC),
    onPrimary = Color.Black,
    primaryContainer = Color(0xFF3700B3),
    secondary = Color(0xFF03DAC6),
    onSecondary = Color.Black,
    background = Color(0xFF121212),
    surface = Color(0xFF121212),
    error = Color(0xFFCF6679)
)

@Composable
fun TitanFinanceTheme(
    darkTheme: Boolean = isSystemInDarkTheme(),
    content: @Composable () -> Unit
) {
    val colorScheme = if (darkTheme) DarkColorScheme else LightColorScheme
    
    MaterialTheme(
        colorScheme = colorScheme,
        typography = Typography,
        content = content
    )
}
'''
        }
    
    @staticmethod
    def generate_feature_module(feature_name: str):
        """Generate feature module with Clean Architecture"""
        return {
            'build.gradle.kts': f'''plugins {{
    alias(libs.plugins.android.library)
    alias(libs.plugins.kotlin.android)
    alias(libs.plugins.ksp)
    alias(libs.plugins.hilt)
}}

android {{
    namespace = "com.titan.finance.feature.{feature_name}"
    compileSdk = 34
    
    defaultConfig {{
        minSdk = 26
        
        testInstrumentationRunner = "androidx.test.runner.AndroidJUnitRunner"
    }}
    
    buildFeatures {{
        compose = true
    }}
    
    composeOptions {{
        kotlinCompilerExtensionVersion = libs.versions.compose.compiler.get()
    }}
}}

dependencies {{
    // Core modules
    implementation(project(":core:common"))
    implementation(project(":core:network"))
    implementation(project(":core:database"))
    implementation(project(":core:ui"))
    
    // Compose
    implementation(platform(libs.compose.bom))
    implementation(libs.bundles.compose)
    
    // Hilt
    implementation(libs.hilt.android)
    implementation(libs.hilt.navigation.compose)
    ksp(libs.hilt.compiler)
    
    // Testing
    testImplementation(project(":core:testing"))
    testImplementation(libs.junit)
    testImplementation(libs.mockk)
    testImplementation(libs.turbine)
}}
''',
            'src/main/kotlin/': {
                f'{feature_name.capitalize()}Screen.kt': f'''package com.titan.finance.feature.{feature_name}

import androidx.compose.runtime.*
import androidx.compose.material3.*
import androidx.hilt.navigation.compose.hiltViewModel

// AI Architecture Note: Feature module with isolated dependencies
// This allows parallel development and independent testing

@Composable
fun {feature_name.capitalize()}Screen(
    viewModel: {feature_name.capitalize()}ViewModel = hiltViewModel()
) {{
    val uiState by viewModel.uiState.collectAsState()
    
    // UI implementation
}}
''',
                f'{feature_name.capitalize()}ViewModel.kt': f'''package com.titan.finance.feature.{feature_name}

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import dagger.hilt.android.lifecycle.HiltViewModel
import kotlinx.coroutines.flow.*
import javax.inject.Inject

// AI Architecture Note: ViewModel with StateFlow for reactive UI
// ViewModelScope ensures proper lifecycle management

@HiltViewModel
class {feature_name.capitalize()}ViewModel @Inject constructor(
    // Inject use cases here
) : ViewModel() {{
    
    private val _uiState = MutableStateFlow({feature_name.capitalize()}UiState())
    val uiState: StateFlow<{feature_name.capitalize()}UiState> = _uiState.asStateFlow()
    
    // Business logic
}}

data class {feature_name.capitalize()}UiState(
    val isLoading: Boolean = false,
    val error: String? = null
)
'''
            }
        }
    
    @staticmethod
    def generate_github_actions_ci():
        """Generate GitHub Actions CI/CD pipeline"""
        return '''.github/workflows/ci.yml:
name: Android CI/CD

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
    
    - name: Run unit tests
      run: ./gradlew test
    
    - name: Run lint
      run: ./gradlew lint
    
    - name: Build debug APK
      run: ./gradlew assembleDebug
    
    - name: Upload APK
      uses: actions/upload-artifact@v3
      with:
        name: app-debug
        path: app/build/outputs/apk/debug/app-debug.apk
    
    - name: Run instrumented tests
      uses: reactivecircus/android-emulator-runner@v2
      with:
        api-level: 29
        script: ./gradlew connectedCheck
    
    - name: Upload test reports
      if: always()
      uses: actions/upload-artifact@v3
      with:
        name: test-reports
        path: |
          **/build/reports/tests/
          **/build/reports/androidTests/

  code-quality:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Run Detekt
      run: ./gradlew detekt
    
    - name: Upload Detekt report
      uses: actions/upload-artifact@v3
      with:
        name: detekt-report
        path: build/reports/detekt/

  deploy:
    needs: [build, code-quality]
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Build release APK
      run: ./gradlew assembleRelease
      env:
        KEYSTORE_PASSWORD: ${{ secrets.KEYSTORE_PASSWORD }}
        KEY_ALIAS: ${{ secrets.KEY_ALIAS }}
        KEY_PASSWORD: ${{ secrets.KEY_PASSWORD }}
    
    - name: Upload to Play Store
      uses: r0adkll/upload-google-play@v1
      with:
        serviceAccountJsonPlainText: ${{ secrets.SERVICE_ACCOUNT_JSON }}
        packageName: com.titan.finance
        releaseFiles: app/build/outputs/bundle/release/app-release.aab
        track: internal
'''

# Usage example
def create_multi_module_project(app_name: str, features: list):
    """Create complete multi-module project"""
    generator = MultiModuleGenerator()
    structure = generator.generate_module_structure(app_name, features)
    
    return {
        'structure': structure,
        'modules': len(features) + 6,  # features + core modules + app
        'benefits': [
            'Parallel development',
            'Independent testing',
            'Faster build times',
            'Better code organization',
            'Easier maintenance'
        ]
    }
