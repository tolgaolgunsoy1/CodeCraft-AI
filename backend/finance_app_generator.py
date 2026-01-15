# Finance App Generator - Real-time Stock Tracking with Charts

class FinanceAppGenerator:
    """Generate production-ready finance applications"""
    
    @staticmethod
    def generate_finance_dashboard(package_name: str, app_name: str):
        """Generate complete finance dashboard with charts"""
        
        return f'''package {package_name}.ui.dashboard

import androidx.compose.animation.core.*
import androidx.compose.foundation.Canvas
import androidx.compose.foundation.background
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.*
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.geometry.Offset
import androidx.compose.ui.graphics.*
import androidx.compose.ui.graphics.drawscope.Stroke
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.lifecycle.viewmodel.compose.viewModel
import kotlin.math.cos
import kotlin.math.sin

@Composable
fun FinanceDashboardScreen(
    viewModel: FinanceDashboardViewModel = viewModel()
) {{
    val uiState by viewModel.uiState.collectAsState()
    
    Scaffold(
        topBar = {{
            TopAppBar(
                title = {{ Text("{app_name}") }},
                actions = {{
                    IconButton(onClick = {{ viewModel.refresh() }}) {{
                        Icon(Icons.Default.Refresh, "Refresh")
                    }}
                    IconButton(onClick = {{ /* Notifications */ }}) {{
                        Icon(Icons.Default.Notifications, "Notifications")
                    }}
                }}
            )
        }}
    ) {{ padding ->
        LazyColumn(
            modifier = Modifier
                .fillMaxSize()
                .padding(padding)
                .padding(16.dp),
            verticalArrangement = Arrangement.spacedBy(16.dp)
        ) {{
            // Portfolio Summary Cards
            item {{
                PortfolioSummaryCards(
                    totalBalance = uiState.totalBalance,
                    todayChange = uiState.todayChange,
                    todayChangePercent = uiState.todayChangePercent
                )
            }}
            
            // Stock Price Chart
            item {{
                StockPriceChart(
                    data = uiState.chartData,
                    modifier = Modifier
                        .fillMaxWidth()
                        .height(250.dp)
                )
            }}
            
            // Holdings List
            item {{
                Text(
                    text = "Your Holdings",
                    style = MaterialTheme.typography.titleLarge,
                    fontWeight = FontWeight.Bold
                )
            }}
            
            items(uiState.holdings) {{ holding ->
                HoldingCard(holding = holding)
            }}
            
            // Recent Transactions
            item {{
                Text(
                    text = "Recent Transactions",
                    style = MaterialTheme.typography.titleLarge,
                    fontWeight = FontWeight.Bold
                )
            }}
            
            items(uiState.transactions) {{ transaction ->
                TransactionItem(transaction = transaction)
            }}
        }}
    }}
}}

@Composable
fun PortfolioSummaryCards(
    totalBalance: Double,
    todayChange: Double,
    todayChangePercent: Double
) {{
    Row(
        modifier = Modifier.fillMaxWidth(),
        horizontalArrangement = Arrangement.spacedBy(12.dp)
    ) {{
        // Total Balance Card
        Card(
            modifier = Modifier.weight(1f),
            colors = CardDefaults.cardColors(
                containerColor = MaterialTheme.colorScheme.primaryContainer
            )
        ) {{
            Column(
                modifier = Modifier.padding(16.dp)
            ) {{
                Text(
                    text = "Total Balance",
                    style = MaterialTheme.typography.bodySmall,
                    color = MaterialTheme.colorScheme.onPrimaryContainer.copy(alpha = 0.7f)
                )
                Spacer(modifier = Modifier.height(8.dp))
                Text(
                    text = "$$${{String.format("%.2f", totalBalance)}}",
                    style = MaterialTheme.typography.headlineMedium,
                    fontWeight = FontWeight.Bold,
                    color = MaterialTheme.colorScheme.onPrimaryContainer
                )
            }}
        }}
        
        // Today's Change Card
        Card(
            modifier = Modifier.weight(1f),
            colors = CardDefaults.cardColors(
                containerColor = if (todayChange >= 0) 
                    Color(0xFF4CAF50).copy(alpha = 0.2f)
                else 
                    Color(0xFFF44336).copy(alpha = 0.2f)
            )
        ) {{
            Column(
                modifier = Modifier.padding(16.dp)
            ) {{
                Text(
                    text = "Today",
                    style = MaterialTheme.typography.bodySmall
                )
                Spacer(modifier = Modifier.height(8.dp))
                Row(
                    verticalAlignment = Alignment.CenterVertically
                ) {{
                    Icon(
                        imageVector = if (todayChange >= 0) 
                            Icons.Default.TrendingUp 
                        else 
                            Icons.Default.TrendingDown,
                        contentDescription = null,
                        tint = if (todayChange >= 0) Color(0xFF4CAF50) else Color(0xFFF44336),
                        modifier = Modifier.size(20.dp)
                    )
                    Spacer(modifier = Modifier.width(4.dp))
                    Text(
                        text = "${{String.format("%.2f%%", todayChangePercent)}}",
                        style = MaterialTheme.typography.titleLarge,
                        fontWeight = FontWeight.Bold,
                        color = if (todayChange >= 0) Color(0xFF4CAF50) else Color(0xFFF44336)
                    )
                }}
            }}
        }}
    }}
}}

@Composable
fun StockPriceChart(
    data: List<ChartPoint>,
    modifier: Modifier = Modifier
) {{
    Card(
        modifier = modifier,
        elevation = CardDefaults.cardElevation(defaultElevation = 2.dp)
    ) {{
        Column(
            modifier = Modifier.padding(16.dp)
        ) {{
            Text(
                text = "Price Chart (7 Days)",
                style = MaterialTheme.typography.titleMedium,
                fontWeight = FontWeight.Bold
            )
            Spacer(modifier = Modifier.height(16.dp))
            
            if (data.isNotEmpty()) {{
                LineChart(
                    data = data,
                    modifier = Modifier
                        .fillMaxWidth()
                        .height(180.dp)
                )
            }} else {{
                Box(
                    modifier = Modifier
                        .fillMaxWidth()
                        .height(180.dp),
                    contentAlignment = Alignment.Center
                ) {{
                    CircularProgressIndicator()
                }}
            }}
        }}
    }}
}}

@Composable
fun LineChart(
    data: List<ChartPoint>,
    modifier: Modifier = Modifier
) {{
    val animatedProgress = remember {{ Animatable(0f) }}
    
    LaunchedEffect(data) {{
        animatedProgress.animateTo(
            targetValue = 1f,
            animationSpec = tween(durationMillis = 1000, easing = FastOutSlowInEasing)
        )
    }}
    
    Canvas(modifier = modifier) {{
        val width = size.width
        val height = size.height
        val padding = 40f
        
        if (data.isEmpty()) return@Canvas
        
        val maxValue = data.maxOf {{ it.value }}
        val minValue = data.minOf {{ it.value }}
        val valueRange = maxValue - minValue
        
        val points = data.mapIndexed {{ index, point ->
            val x = padding + (width - 2 * padding) * index / (data.size - 1)
            val y = height - padding - (height - 2 * padding) * ((point.value - minValue) / valueRange)
            Offset(x, y)
        }}
        
        // Draw gradient fill
        val gradientPath = Path().apply {{
            moveTo(points.first().x, height - padding)
            points.forEach {{ lineTo(it.x, it.y) }}
            lineTo(points.last().x, height - padding)
            close()
        }}
        
        drawPath(
            path = gradientPath,
            brush = Brush.verticalGradient(
                colors = listOf(
                    Color(0xFF6200EE).copy(alpha = 0.3f),
                    Color.Transparent
                )
            )
        )
        
        // Draw line
        val animatedPoints = points.take((points.size * animatedProgress.value).toInt().coerceAtLeast(2))
        
        for (i in 0 until animatedPoints.size - 1) {{
            drawLine(
                color = Color(0xFF6200EE),
                start = animatedPoints[i],
                end = animatedPoints[i + 1],
                strokeWidth = 4f,
                cap = StrokeCap.Round
            )
        }}
        
        // Draw points
        animatedPoints.forEach {{ point ->
            drawCircle(
                color = Color(0xFF6200EE),
                radius = 6f,
                center = point
            )
            drawCircle(
                color = Color.White,
                radius = 3f,
                center = point
            )
        }}
    }}
}}

@Composable
fun HoldingCard(holding: Holding) {{
    Card(
        modifier = Modifier.fillMaxWidth(),
        onClick = {{ /* Navigate to detail */ }}
    ) {{
        Row(
            modifier = Modifier
                .fillMaxWidth()
                .padding(16.dp),
            horizontalArrangement = Arrangement.SpaceBetween,
            verticalAlignment = Alignment.CenterVertically
        ) {{
            Column {{
                Text(
                    text = holding.symbol,
                    style = MaterialTheme.typography.titleMedium,
                    fontWeight = FontWeight.Bold
                )
                Text(
                    text = "${{holding.shares}} shares",
                    style = MaterialTheme.typography.bodySmall,
                    color = MaterialTheme.colorScheme.onSurface.copy(alpha = 0.6f)
                )
            }}
            
            Column(horizontalAlignment = Alignment.End) {{
                Text(
                    text = "$$${{String.format("%.2f", holding.currentPrice)}}",
                    style = MaterialTheme.typography.titleMedium,
                    fontWeight = FontWeight.Bold
                )
                Row(verticalAlignment = Alignment.CenterVertically) {{
                    Icon(
                        imageVector = if (holding.changePercent >= 0) 
                            Icons.Default.ArrowUpward 
                        else 
                            Icons.Default.ArrowDownward,
                        contentDescription = null,
                        tint = if (holding.changePercent >= 0) Color(0xFF4CAF50) else Color(0xFFF44336),
                        modifier = Modifier.size(16.dp)
                    )
                    Text(
                        text = "${{String.format("%.2f%%", holding.changePercent)}}",
                        style = MaterialTheme.typography.bodySmall,
                        color = if (holding.changePercent >= 0) Color(0xFF4CAF50) else Color(0xFFF44336)
                    )
                }}
            }}
        }}
    }}
}}

@Composable
fun TransactionItem(transaction: Transaction) {{
    Row(
        modifier = Modifier
            .fillMaxWidth()
            .padding(vertical = 8.dp),
        horizontalArrangement = Arrangement.SpaceBetween,
        verticalAlignment = Alignment.CenterVertically
    ) {{
        Row(
            verticalAlignment = Alignment.CenterVertically,
            horizontalArrangement = Arrangement.spacedBy(12.dp)
        ) {{
            Surface(
                shape = RoundedCornerShape(8.dp),
                color = if (transaction.type == TransactionType.BUY)
                    Color(0xFF4CAF50).copy(alpha = 0.2f)
                else
                    Color(0xFFF44336).copy(alpha = 0.2f)
            ) {{
                Icon(
                    imageVector = if (transaction.type == TransactionType.BUY)
                        Icons.Default.Add
                    else
                        Icons.Default.Remove,
                    contentDescription = null,
                    tint = if (transaction.type == TransactionType.BUY)
                        Color(0xFF4CAF50)
                    else
                        Color(0xFFF44336),
                    modifier = Modifier.padding(8.dp)
                )
            }}
            
            Column {{
                Text(
                    text = transaction.symbol,
                    style = MaterialTheme.typography.bodyLarge,
                    fontWeight = FontWeight.Medium
                )
                Text(
                    text = transaction.date,
                    style = MaterialTheme.typography.bodySmall,
                    color = MaterialTheme.colorScheme.onSurface.copy(alpha = 0.6f)
                )
            }}
        }}
        
        Text(
            text = "${{if (transaction.type == TransactionType.BUY) "-" else "+"}}$$${{String.format("%.2f", transaction.amount)}}",
            style = MaterialTheme.typography.bodyLarge,
            fontWeight = FontWeight.Bold,
            color = if (transaction.type == TransactionType.BUY)
                Color(0xFFF44336)
            else
                Color(0xFF4CAF50)
        )
    }}
}}

// Data Classes
data class ChartPoint(val timestamp: Long, val value: Double)

data class Holding(
    val symbol: String,
    val shares: Double,
    val currentPrice: Double,
    val changePercent: Double
)

data class Transaction(
    val symbol: String,
    val type: TransactionType,
    val amount: Double,
    val date: String
)

enum class TransactionType {{ BUY, SELL }}
'''
    
    @staticmethod
    def generate_finance_viewmodel(package_name: str):
        """Generate ViewModel with real-time data"""
        
        return f'''package {package_name}.ui.dashboard

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import kotlinx.coroutines.delay
import kotlinx.coroutines.flow.*
import kotlinx.coroutines.launch
import kotlin.random.Random

class FinanceDashboardViewModel : ViewModel() {{
    
    private val _uiState = MutableStateFlow(DashboardUiState())
    val uiState: StateFlow<DashboardUiState> = _uiState.asStateFlow()
    
    init {{
        loadInitialData()
        startRealTimeUpdates()
    }}
    
    private fun loadInitialData() {{
        viewModelScope.launch {{
            _uiState.update {{ state ->
                state.copy(
                    totalBalance = 125430.50,
                    todayChange = 2340.25,
                    todayChangePercent = 1.91,
                    holdings = generateMockHoldings(),
                    transactions = generateMockTransactions(),
                    chartData = generateMockChartData()
                )
            }}
        }}
    }}
    
    private fun startRealTimeUpdates() {{
        viewModelScope.launch {{
            while (true) {{
                delay(5000) // Update every 5 seconds
                updatePrices()
            }}
        }}
    }}
    
    private fun updatePrices() {{
        _uiState.update {{ state ->
            val updatedHoldings = state.holdings.map {{ holding ->
                val priceChange = Random.nextDouble(-2.0, 2.0)
                holding.copy(
                    currentPrice = holding.currentPrice + priceChange,
                    changePercent = holding.changePercent + Random.nextDouble(-0.5, 0.5)
                )
            }}
            
            val newTotalBalance = updatedHoldings.sumOf {{ it.currentPrice * it.shares }}
            val balanceChange = newTotalBalance - state.totalBalance
            
            state.copy(
                holdings = updatedHoldings,
                totalBalance = newTotalBalance,
                todayChange = state.todayChange + balanceChange,
                todayChangePercent = (balanceChange / state.totalBalance) * 100
            )
        }}
    }}
    
    fun refresh() {{
        loadInitialData()
    }}
    
    private fun generateMockHoldings() = listOf(
        Holding("AAPL", 50.0, 178.50, 2.3),
        Holding("GOOGL", 25.0, 142.30, -0.8),
        Holding("MSFT", 40.0, 378.90, 1.5),
        Holding("TSLA", 15.0, 242.80, -3.2),
        Holding("AMZN", 30.0, 151.20, 0.9)
    )
    
    private fun generateMockTransactions() = listOf(
        Transaction("AAPL", TransactionType.BUY, 8925.00, "2024-01-15"),
        Transaction("GOOGL", TransactionType.SELL, 3557.50, "2024-01-14"),
        Transaction("MSFT", TransactionType.BUY, 15156.00, "2024-01-13"),
        Transaction("TSLA", TransactionType.BUY, 3642.00, "2024-01-12")
    )
    
    private fun generateMockChartData(): List<ChartPoint> {{
        val baseValue = 120000.0
        return (0..6).map {{ day ->
            ChartPoint(
                timestamp = System.currentTimeMillis() - (6 - day) * 24 * 60 * 60 * 1000,
                value = baseValue + Random.nextDouble(-5000.0, 5000.0)
            )
        }}
    }}
}}

data class DashboardUiState(
    val totalBalance: Double = 0.0,
    val todayChange: Double = 0.0,
    val todayChangePercent: Double = 0.0,
    val holdings: List<Holding> = emptyList(),
    val transactions: List<Transaction> = emptyList(),
    val chartData: List<ChartPoint> = emptyList(),
    val isLoading: Boolean = false
)
'''
    
    @staticmethod
    def generate_firebase_notification_service(package_name: str):
        """Generate Firebase Cloud Messaging service"""
        
        return f'''package {package_name}.service

import android.app.NotificationChannel
import android.app.NotificationManager
import android.app.PendingIntent
import android.content.Context
import android.content.Intent
import android.os.Build
import androidx.core.app.NotificationCompat
import com.google.firebase.messaging.FirebaseMessagingService
import com.google.firebase.messaging.RemoteMessage
import {package_name}.MainActivity
import {package_name}.R

class PriceAlertService : FirebaseMessagingService() {{
    
    override fun onMessageReceived(message: RemoteMessage) {{
        super.onMessageReceived(message)
        
        message.notification?.let {{
            sendNotification(it.title ?: "Price Alert", it.body ?: "")
        }}
        
        // Handle data payload
        message.data.let {{ data ->
            val symbol = data["symbol"]
            val price = data["price"]
            val change = data["change"]
            
            if (symbol != null && price != null) {{
                sendPriceAlert(symbol, price, change ?: "0")
            }}
        }}
    }}
    
    override fun onNewToken(token: String) {{
        super.onNewToken(token)
        // Send token to server
        sendTokenToServer(token)
    }}
    
    private fun sendNotification(title: String, body: String) {{
        val intent = Intent(this, MainActivity::class.java).apply {{
            flags = Intent.FLAG_ACTIVITY_NEW_TASK or Intent.FLAG_ACTIVITY_CLEAR_TASK
        }}
        
        val pendingIntent = PendingIntent.getActivity(
            this, 0, intent,
            PendingIntent.FLAG_IMMUTABLE
        )
        
        val channelId = "price_alerts"
        val notificationBuilder = NotificationCompat.Builder(this, channelId)
            .setSmallIcon(R.drawable.ic_notification)
            .setContentTitle(title)
            .setContentText(body)
            .setAutoCancel(true)
            .setPriority(NotificationCompat.PRIORITY_HIGH)
            .setContentIntent(pendingIntent)
        
        val notificationManager = getSystemService(Context.NOTIFICATION_SERVICE) as NotificationManager
        
        // Create notification channel for Android O+
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) {{
            val channel = NotificationChannel(
                channelId,
                "Price Alerts",
                NotificationManager.IMPORTANCE_HIGH
            ).apply {{
                description = "Stock price alerts and notifications"
            }}
            notificationManager.createNotificationChannel(channel)
        }}
        
        notificationManager.notify(System.currentTimeMillis().toInt(), notificationBuilder.build())
    }}
    
    private fun sendPriceAlert(symbol: String, price: String, change: String) {{
        val changePercent = change.toDoubleOrNull() ?: 0.0
        val emoji = if (changePercent >= 0) "📈" else "📉"
        
        sendNotification(
            title = "$emoji $symbol Price Alert",
            body = "Current price: $$$price (${{String.format("%.2f", changePercent)}}%)"
        )
    }}
    
    private fun sendTokenToServer(token: String) {{
        // TODO: Send FCM token to your backend server
        android.util.Log.d("FCM", "New token: $token")
    }}
}}
'''
    
    @staticmethod
    def get_finance_dependencies():
        """Get finance-specific dependencies"""
        
        return '''
    // Charts
    implementation("com.patrykandpatrick.vico:compose:1.13.1")
    implementation("com.patrykandpatrick.vico:compose-m3:1.13.1")
    implementation("com.patrykandpatrick.vico:core:1.13.1")
    
    // Firebase
    implementation(platform("com.google.firebase:firebase-bom:32.7.0"))
    implementation("com.google.firebase:firebase-messaging-ktx")
    implementation("com.google.firebase:firebase-analytics-ktx")
    implementation("com.google.firebase:firebase-firestore-ktx")
    
    // Real-time updates
    implementation("org.jetbrains.kotlinx:kotlinx-coroutines-play-services:1.7.3")
    
    // Data formatting
    implementation("com.squareup.moshi:moshi-kotlin:1.15.0")
    implementation("com.squareup.moshi:moshi-adapters:1.15.0")
'''
