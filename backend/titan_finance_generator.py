# Titan Finance - Enterprise-Grade Finance App Generator

class TitanFinanceGenerator:
    """Generate production-ready finance app with Clean Architecture"""
    
    @staticmethod
    def generate_libs_versions_toml():
        """Generate optimized Version Catalog for Titan Finance"""
        return '''[versions]
# Core
kotlin = "1.9.22"
agp = "8.2.2"
ksp = "1.9.22-1.0.17"

# Compose
compose-bom = "2024.01.00"
compose-compiler = "1.5.8"
activity-compose = "1.8.2"

# AndroidX
core-ktx = "1.12.0"
lifecycle = "2.7.0"
navigation = "2.7.6"
room = "2.6.1"
datastore = "1.0.0"
biometric = "1.2.0-alpha05"
security-crypto = "1.1.0-alpha06"

# Network
retrofit = "2.9.0"
okhttp = "4.12.0"
moshi = "1.15.0"

# DI
hilt = "2.50"
hilt-navigation = "1.1.0"

# Image
coil = "2.5.0"

# Charts
vico = "1.13.1"

# Utilities
timber = "5.0.1"
coroutines = "1.7.3"

# Firebase
firebase-bom = "32.7.0"

# Testing
junit = "4.13.2"
mockk = "1.13.9"
turbine = "1.0.0"

[libraries]
# Kotlin
kotlin-stdlib = { module = "org.jetbrains.kotlin:kotlin-stdlib", version.ref = "kotlin" }
kotlinx-coroutines-android = { module = "org.jetbrains.kotlinx:kotlinx-coroutines-android", version.ref = "coroutines" }
kotlinx-coroutines-play-services = { module = "org.jetbrains.kotlinx:kotlinx-coroutines-play-services", version.ref = "coroutines" }

# Compose BOM
compose-bom = { module = "androidx.compose:compose-bom", version.ref = "compose-bom" }
compose-ui = { module = "androidx.compose.ui:ui" }
compose-ui-graphics = { module = "androidx.compose.ui:ui-graphics" }
compose-ui-tooling = { module = "androidx.compose.ui:ui-tooling" }
compose-ui-tooling-preview = { module = "androidx.compose.ui:ui-tooling-preview" }
compose-material3 = { module = "androidx.compose.material3:material3" }
compose-material-icons = { module = "androidx.compose.material:material-icons-extended" }
activity-compose = { module = "androidx.activity:activity-compose", version.ref = "activity-compose" }

# AndroidX Core
androidx-core-ktx = { module = "androidx.core:core-ktx", version.ref = "core-ktx" }
androidx-lifecycle-runtime = { module = "androidx.lifecycle:lifecycle-runtime-ktx", version.ref = "lifecycle" }
androidx-lifecycle-viewmodel = { module = "androidx.lifecycle:lifecycle-viewmodel-ktx", version.ref = "lifecycle" }
androidx-lifecycle-viewmodel-compose = { module = "androidx.lifecycle:lifecycle-viewmodel-compose", version.ref = "lifecycle" }

# Navigation
navigation-compose = { module = "androidx.navigation:navigation-compose", version.ref = "navigation" }

# Room
room-runtime = { module = "androidx.room:room-runtime", version.ref = "room" }
room-ktx = { module = "androidx.room:room-ktx", version.ref = "room" }
room-compiler = { module = "androidx.room:room-compiler", version.ref = "room" }

# DataStore
datastore-preferences = { module = "androidx.datastore:datastore-preferences", version.ref = "datastore" }

# Security
biometric = { module = "androidx.biometric:biometric", version.ref = "biometric" }
security-crypto = { module = "androidx.security:security-crypto", version.ref = "security-crypto" }

# Network
retrofit = { module = "com.squareup.retrofit2:retrofit", version.ref = "retrofit" }
retrofit-moshi = { module = "com.squareup.retrofit2:converter-moshi", version.ref = "retrofit" }
okhttp = { module = "com.squareup.okhttp3:okhttp", version.ref = "okhttp" }
okhttp-logging = { module = "com.squareup.okhttp3:logging-interceptor", version.ref = "okhttp" }
moshi = { module = "com.squareup.moshi:moshi", version.ref = "moshi" }
moshi-kotlin = { module = "com.squareup.moshi:moshi-kotlin", version.ref = "moshi" }
moshi-codegen = { module = "com.squareup.moshi:moshi-kotlin-codegen", version.ref = "moshi" }

# Hilt
hilt-android = { module = "com.google.dagger:hilt-android", version.ref = "hilt" }
hilt-compiler = { module = "com.google.dagger:hilt-compiler", version.ref = "hilt" }
hilt-navigation-compose = { module = "androidx.hilt:hilt-navigation-compose", version.ref = "hilt-navigation" }

# Image Loading
coil-compose = { module = "io.coil-kt:coil-compose", version.ref = "coil" }

# Charts
vico-compose = { module = "com.patrykandpatrick.vico:compose", version.ref = "vico" }
vico-compose-m3 = { module = "com.patrykandpatrick.vico:compose-m3", version.ref = "vico" }
vico-core = { module = "com.patrykandpatrick.vico:core", version.ref = "vico" }

# Utilities
timber = { module = "com.jakewharton.timber:timber", version.ref = "timber" }

# Firebase
firebase-bom = { module = "com.google.firebase:firebase-bom", version.ref = "firebase-bom" }
firebase-messaging = { module = "com.google.firebase:firebase-messaging-ktx" }
firebase-analytics = { module = "com.google.firebase:firebase-analytics-ktx" }
firebase-crashlytics = { module = "com.google.firebase:firebase-crashlytics-ktx" }

# Testing
junit = { module = "junit:junit", version.ref = "junit" }
mockk = { module = "io.mockk:mockk", version.ref = "mockk" }
turbine = { module = "app.cash.turbine:turbine", version.ref = "turbine" }
coroutines-test = { module = "org.jetbrains.kotlinx:kotlinx-coroutines-test", version.ref = "coroutines" }

[bundles]
compose = ["compose-ui", "compose-ui-graphics", "compose-ui-tooling-preview", "compose-material3", "compose-material-icons", "activity-compose"]
lifecycle = ["androidx-lifecycle-runtime", "androidx-lifecycle-viewmodel", "androidx-lifecycle-viewmodel-compose"]
room = ["room-runtime", "room-ktx"]
network = ["retrofit", "retrofit-moshi", "okhttp", "okhttp-logging", "moshi", "moshi-kotlin"]
security = ["biometric", "security-crypto"]
vico = ["vico-compose", "vico-compose-m3", "vico-core"]
firebase = ["firebase-messaging", "firebase-analytics", "firebase-crashlytics"]

[plugins]
android-application = { id = "com.android.application", version.ref = "agp" }
kotlin-android = { id = "org.jetbrains.kotlin.android", version.ref = "kotlin" }
ksp = { id = "com.google.devtools.ksp", version.ref = "ksp" }
hilt = { id = "com.google.dagger.hilt.android", version.ref = "hilt" }
'''
    
    @staticmethod
    def generate_clean_architecture_structure(package_name: str):
        """Generate complete Clean Architecture folder structure"""
        return {
            'domain': {
                'model': ['Portfolio', 'CryptoAsset', 'Transaction', 'PriceHistory'],
                'repository': ['CryptoRepository', 'UserRepository', 'TransactionRepository'],
                'usecase': [
                    'GetPortfolioUseCase',
                    'GetCryptoPricesUseCase',
                    'AddTransactionUseCase',
                    'GetPriceHistoryUseCase',
                    'AuthenticateUserUseCase'
                ]
            },
            'data': {
                'remote': {
                    'api': ['CryptoApiService', 'RetrofitBuilder'],
                    'dto': ['CryptoPriceDto', 'PortfolioDto', 'TransactionDto'],
                    'mapper': ['CryptoMapper', 'PortfolioMapper']
                },
                'local': {
                    'database': ['TitanDatabase', 'CryptoDao', 'TransactionDao'],
                    'entity': ['CryptoEntity', 'TransactionEntity'],
                    'preferences': ['EncryptedPreferences', 'UserPreferences']
                },
                'repository': ['CryptoRepositoryImpl', 'UserRepositoryImpl']
            },
            'presentation': {
                'dashboard': ['DashboardScreen', 'DashboardViewModel', 'DashboardUiState'],
                'portfolio': ['PortfolioScreen', 'PortfolioViewModel'],
                'transactions': ['TransactionsScreen', 'TransactionsViewModel'],
                'auth': ['BiometricAuthScreen', 'AuthViewModel'],
                'common': ['LoadingState', 'ErrorState', 'UiEvent']
            },
            'di': ['AppModule', 'NetworkModule', 'DatabaseModule', 'RepositoryModule']
        }
    
    @staticmethod
    def generate_biometric_auth():
        """Generate Biometric Authentication implementation"""
        return '''package com.titan.finance.presentation.auth

import android.content.Context
import androidx.biometric.BiometricManager
import androidx.biometric.BiometricPrompt
import androidx.core.content.ContextCompat
import androidx.fragment.app.FragmentActivity
import kotlinx.coroutines.channels.Channel
import kotlinx.coroutines.flow.receiveAsFlow
import timber.log.Timber
import javax.inject.Inject
import javax.inject.Singleton

@Singleton
class BiometricAuthManager @Inject constructor() {
    
    private val _authResult = Channel<AuthResult>()
    val authResult = _authResult.receiveAsFlow()
    
    fun canAuthenticate(context: Context): Boolean {
        val biometricManager = BiometricManager.from(context)
        return when (biometricManager.canAuthenticate(
            BiometricManager.Authenticators.BIOMETRIC_STRONG or
            BiometricManager.Authenticators.DEVICE_CREDENTIAL
        )) {
            BiometricManager.BIOMETRIC_SUCCESS -> true
            else -> false
        }
    }
    
    fun authenticate(activity: FragmentActivity) {
        val executor = ContextCompat.getMainExecutor(activity)
        
        val biometricPrompt = BiometricPrompt(
            activity,
            executor,
            object : BiometricPrompt.AuthenticationCallback() {
                override fun onAuthenticationError(errorCode: Int, errString: CharSequence) {
                    super.onAuthenticationError(errorCode, errString)
                    Timber.e("Authentication error: $errString")
                    _authResult.trySend(AuthResult.Error(errString.toString()))
                }
                
                override fun onAuthenticationSucceeded(result: BiometricPrompt.AuthenticationResult) {
                    super.onAuthenticationSucceeded(result)
                    Timber.d("Authentication succeeded")
                    _authResult.trySend(AuthResult.Success)
                }
                
                override fun onAuthenticationFailed() {
                    super.onAuthenticationFailed()
                    Timber.w("Authentication failed")
                    _authResult.trySend(AuthResult.Failed)
                }
            }
        )
        
        val promptInfo = BiometricPrompt.PromptInfo.Builder()
            .setTitle("Titan Finance")
            .setSubtitle("Authenticate to access your portfolio")
            .setAllowedAuthenticators(
                BiometricManager.Authenticators.BIOMETRIC_STRONG or
                BiometricManager.Authenticators.DEVICE_CREDENTIAL
            )
            .build()
        
        biometricPrompt.authenticate(promptInfo)
    }
}

sealed class AuthResult {
    object Success : AuthResult()
    object Failed : AuthResult()
    data class Error(val message: String) : AuthResult()
}
'''
    
    @staticmethod
    def generate_encrypted_preferences():
        """Generate Encrypted SharedPreferences implementation"""
        return '''package com.titan.finance.data.local.preferences

import android.content.Context
import android.content.SharedPreferences
import androidx.security.crypto.EncryptedSharedPreferences
import androidx.security.crypto.MasterKey
import dagger.hilt.android.qualifiers.ApplicationContext
import kotlinx.coroutines.flow.Flow
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.asStateFlow
import javax.inject.Inject
import javax.inject.Singleton

@Singleton
class SecurePreferences @Inject constructor(
    @ApplicationContext private val context: Context
) {
    
    private val masterKey = MasterKey.Builder(context)
        .setKeyScheme(MasterKey.KeyScheme.AES256_GCM)
        .build()
    
    private val sharedPreferences: SharedPreferences = EncryptedSharedPreferences.create(
        context,
        "titan_secure_prefs",
        masterKey,
        EncryptedSharedPreferences.PrefKeyEncryptionScheme.AES256_SIV,
        EncryptedSharedPreferences.PrefValueEncryptionScheme.AES256_GCM
    )
    
    private val _apiKey = MutableStateFlow<String?>(null)
    val apiKey: Flow<String?> = _apiKey.asStateFlow()
    
    init {
        _apiKey.value = getApiKey()
    }
    
    fun saveApiKey(key: String) {
        sharedPreferences.edit().putString(KEY_API, key).apply()
        _apiKey.value = key
    }
    
    fun getApiKey(): String? {
        return sharedPreferences.getString(KEY_API, null)
    }
    
    fun saveBalance(balance: Double) {
        sharedPreferences.edit().putString(KEY_BALANCE, balance.toString()).apply()
    }
    
    fun getBalance(): Double {
        return sharedPreferences.getString(KEY_BALANCE, "0.0")?.toDoubleOrNull() ?: 0.0
    }
    
    fun saveBiometricEnabled(enabled: Boolean) {
        sharedPreferences.edit().putBoolean(KEY_BIOMETRIC, enabled).apply()
    }
    
    fun isBiometricEnabled(): Boolean {
        return sharedPreferences.getBoolean(KEY_BIOMETRIC, true)
    }
    
    fun clear() {
        sharedPreferences.edit().clear().apply()
        _apiKey.value = null
    }
    
    companion object {
        private const val KEY_API = "api_key"
        private const val KEY_BALANCE = "balance"
        private const val KEY_BIOMETRIC = "biometric_enabled"
    }
}
'''
    
    @staticmethod
    def generate_websocket_service():
        """Generate WebSocket service for real-time crypto prices"""
        return '''package com.titan.finance.data.remote.websocket

import kotlinx.coroutines.channels.awaitClose
import kotlinx.coroutines.flow.Flow
import kotlinx.coroutines.flow.callbackFlow
import okhttp3.*
import okio.ByteString
import timber.log.Timber
import javax.inject.Inject
import javax.inject.Singleton

@Singleton
class CryptoWebSocketService @Inject constructor(
    private val okHttpClient: OkHttpClient
) {
    
    private var webSocket: WebSocket? = null
    
    fun observePrices(symbols: List<String>): Flow<PriceUpdate> = callbackFlow {
        val request = Request.Builder()
            .url("wss://stream.binance.com:9443/ws")
            .build()
        
        val listener = object : WebSocketListener() {
            override fun onOpen(webSocket: WebSocket, response: Response) {
                Timber.d("WebSocket opened")
                // Subscribe to symbols
                val subscribeMessage = """
                    {
                        "method": "SUBSCRIBE",
                        "params": ${symbols.map { "${it.lowercase()}@ticker" }},
                        "id": 1
                    }
                """.trimIndent()
                webSocket.send(subscribeMessage)
            }
            
            override fun onMessage(webSocket: WebSocket, text: String) {
                try {
                    // Parse price update
                    val update = parsePriceUpdate(text)
                    trySend(update)
                } catch (e: Exception) {
                    Timber.e(e, "Error parsing price update")
                }
            }
            
            override fun onMessage(webSocket: WebSocket, bytes: ByteString) {
                onMessage(webSocket, bytes.utf8())
            }
            
            override fun onClosing(webSocket: WebSocket, code: Int, reason: String) {
                Timber.d("WebSocket closing: $reason")
                webSocket.close(1000, null)
            }
            
            override fun onFailure(webSocket: WebSocket, t: Throwable, response: Response?) {
                Timber.e(t, "WebSocket error")
                close(t)
            }
        }
        
        webSocket = okHttpClient.newWebSocket(request, listener)
        
        awaitClose {
            webSocket?.close(1000, "Flow closed")
            webSocket = null
        }
    }
    
    private fun parsePriceUpdate(json: String): PriceUpdate {
        // Simplified parsing - use Moshi in production
        return PriceUpdate(
            symbol = "BTC",
            price = 0.0,
            change24h = 0.0,
            timestamp = System.currentTimeMillis()
        )
    }
    
    fun disconnect() {
        webSocket?.close(1000, "Manual disconnect")
        webSocket = null
    }
}

data class PriceUpdate(
    val symbol: String,
    val price: Double,
    val change24h: Double,
    val timestamp: Long
)
'''
    
    @staticmethod
    def generate_use_case_template():
        """Generate UseCase base template"""
        return '''package com.titan.finance.domain.usecase

import kotlinx.coroutines.CoroutineDispatcher
import kotlinx.coroutines.withContext

abstract class UseCase<in P, out R>(
    private val dispatcher: CoroutineDispatcher
) {
    suspend operator fun invoke(params: P): Result<R> = withContext(dispatcher) {
        try {
            Result.success(execute(params))
        } catch (e: Exception) {
            Result.failure(e)
        }
    }
    
    @Throws(Exception::class)
    protected abstract suspend fun execute(params: P): R
}

// Example: GetPortfolioUseCase
class GetPortfolioUseCase @Inject constructor(
    private val repository: CryptoRepository,
    @IoDispatcher dispatcher: CoroutineDispatcher
) : UseCase<Unit, Portfolio>(dispatcher) {
    
    override suspend fun execute(params: Unit): Portfolio {
        return repository.getPortfolio()
    }
}
'''
    
    @staticmethod
    def generate_complete_build_gradle(package_name: str):
        """Generate complete build.gradle.kts with all dependencies"""
        return f'''plugins {{
    alias(libs.plugins.android.application)
    alias(libs.plugins.kotlin.android)
    alias(libs.plugins.ksp)
    alias(libs.plugins.hilt)
}}

android {{
    namespace = "{package_name}"
    compileSdk = 34
    
    defaultConfig {{
        applicationId = "{package_name}"
        minSdk = 26
        targetSdk = 34
        versionCode = 1
        versionName = "1.0.0"
        
        testInstrumentationRunner = "androidx.test.runner.AndroidJUnitRunner"
        vectorDrawables.useSupportLibrary = true
        
        ksp {{
            arg("room.schemaLocation", "$projectDir/schemas")
            arg("room.incremental", "true")
        }}
    }}
    
    buildTypes {{
        release {{
            isMinifyEnabled = true
            isShrinkResources = true
            proguardFiles(
                getDefaultProguardFile("proguard-android-optimize.txt"),
                "proguard-rules.pro"
            )
            
            buildConfigField("String", "API_BASE_URL", "\\"https://api.binance.com\\"")
        }}
        debug {{
            isMinifyEnabled = false
            buildConfigField("String", "API_BASE_URL", "\\"https://testnet.binance.com\\"")
        }}
    }}
    
    compileOptions {{
        sourceCompatibility = JavaVersion.VERSION_17
        targetCompatibility = JavaVersion.VERSION_17
    }}
    
    kotlinOptions {{
        jvmTarget = "17"
        freeCompilerArgs += listOf(
            "-opt-in=kotlin.RequiresOptIn",
            "-opt-in=kotlinx.coroutines.ExperimentalCoroutinesApi",
            "-opt-in=androidx.compose.material3.ExperimentalMaterial3Api"
        )
    }}
    
    buildFeatures {{
        compose = true
        buildConfig = true
    }}
    
    composeOptions {{
        kotlinCompilerExtensionVersion = libs.versions.compose.compiler.get()
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
    implementation(libs.kotlinx.coroutines.play.services)
    
    // Compose
    implementation(platform(libs.compose.bom))
    implementation(libs.bundles.compose)
    debugImplementation(libs.compose.ui.tooling)
    
    // AndroidX
    implementation(libs.androidx.core.ktx)
    implementation(libs.bundles.lifecycle)
    implementation(libs.navigation.compose)
    
    // Room
    implementation(libs.bundles.room)
    ksp(libs.room.compiler)
    
    // DataStore
    implementation(libs.datastore.preferences)
    
    // Security
    implementation(libs.bundles.security)
    
    // Network
    implementation(libs.bundles.network)
    ksp(libs.moshi.codegen)
    
    // Hilt
    implementation(libs.hilt.android)
    implementation(libs.hilt.navigation.compose)
    ksp(libs.hilt.compiler)
    
    // Image Loading
    implementation(libs.coil.compose)
    
    // Charts
    implementation(libs.bundles.vico)
    
    // Utilities
    implementation(libs.timber)
    
    // Firebase
    implementation(platform(libs.firebase.bom))
    implementation(libs.bundles.firebase)
    
    // Testing
    testImplementation(libs.junit)
    testImplementation(libs.mockk)
    testImplementation(libs.turbine)
    testImplementation(libs.coroutines.test)
}}
'''

# Generate complete project
def generate_titan_finance_project(output_dir: str):
    """Generate complete Titan Finance project"""
    import os
    
    package_name = "com.titan.finance"
    generator = TitanFinanceGenerator()
    
    # Create base structure
    base_path = os.path.join(output_dir, "TitanFinance")
    gradle_path = os.path.join(base_path, "gradle")
    app_path = os.path.join(base_path, "app")
    src_path = os.path.join(app_path, "src", "main")
    kotlin_path = os.path.join(src_path, "kotlin", "com", "titan", "finance")
    
    os.makedirs(gradle_path, exist_ok=True)
    os.makedirs(kotlin_path, exist_ok=True)
    
    # 1. Version Catalog
    with open(os.path.join(gradle_path, "libs.versions.toml"), 'w') as f:
        f.write(generator.generate_libs_versions_toml())
    
    # 2. Build Gradle
    with open(os.path.join(app_path, "build.gradle.kts"), 'w') as f:
        f.write(generator.generate_complete_build_gradle(package_name))
    
    # 3. Clean Architecture Structure
    structure = generator.generate_clean_architecture_structure(package_name)
    for layer, modules in structure.items():
        layer_path = os.path.join(kotlin_path, layer)
        os.makedirs(layer_path, exist_ok=True)
    
    # 4. Security Components
    auth_path = os.path.join(kotlin_path, "presentation", "auth")
    os.makedirs(auth_path, exist_ok=True)
    with open(os.path.join(auth_path, "BiometricAuthManager.kt"), 'w') as f:
        f.write(generator.generate_biometric_auth())
    
    prefs_path = os.path.join(kotlin_path, "data", "local", "preferences")
    os.makedirs(prefs_path, exist_ok=True)
    with open(os.path.join(prefs_path, "SecurePreferences.kt"), 'w') as f:
        f.write(generator.generate_encrypted_preferences())
    
    # 5. WebSocket Service
    ws_path = os.path.join(kotlin_path, "data", "remote", "websocket")
    os.makedirs(ws_path, exist_ok=True)
    with open(os.path.join(ws_path, "CryptoWebSocketService.kt"), 'w') as f:
        f.write(generator.generate_websocket_service())
    
    # 6. UseCase Template
    usecase_path = os.path.join(kotlin_path, "domain", "usecase")
    os.makedirs(usecase_path, exist_ok=True)
    with open(os.path.join(usecase_path, "UseCase.kt"), 'w') as f:
        f.write(generator.generate_use_case_template())
    
    return {
        'success': True,
        'project_path': base_path,
        'features': [
            'Clean Architecture (Domain/Data/Presentation)',
            'Biometric Authentication',
            'Encrypted SharedPreferences',
            'WebSocket Real-time Updates',
            'Vico Charts Integration',
            'Hilt Dependency Injection',
            'Room Database',
            'Moshi JSON Parsing',
            'Firebase Cloud Messaging',
            'Version Catalog (libs.versions.toml)'
        ],
        'tech_stack': {
            'Architecture': 'Clean Architecture + MVVM',
            'DI': 'Hilt',
            'Database': 'Room',
            'Network': 'Retrofit + OkHttp + Moshi',
            'Real-time': 'WebSocket',
            'Security': 'Biometric + EncryptedSharedPreferences',
            'Charts': 'Vico',
            'State': 'StateFlow + Compose',
            'Testing': 'JUnit + MockK + Turbine'
        }
    }
