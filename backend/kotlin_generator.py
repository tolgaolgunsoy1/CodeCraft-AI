# Kotlin Code Generator for Modern Android Apps

class KotlinGenerator:
    """Generate Kotlin code for modern Android applications"""
    
    @staticmethod
    def create_main_activity(package_name, analysis, use_compose=False):
        if use_compose:
            return KotlinGenerator.create_compose_activity(package_name, analysis)
        else:
            return KotlinGenerator.create_xml_activity(package_name, analysis)
    
    @staticmethod
    def create_compose_activity(package_name, analysis):
        return f'''package {package_name}

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.compose.foundation.layout.*
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp
import {package_name}.ui.theme.AppTheme

class MainActivity : ComponentActivity() {{
    override fun onCreate(savedInstanceState: Bundle?) {{
        super.onCreate(savedInstanceState)
        setContent {{
            AppTheme {{
                Surface(
                    modifier = Modifier.fillMaxSize(),
                    color = MaterialTheme.colorScheme.background
                ) {{
                    MainScreen()
                }}
            }}
        }}
    }}
}}

@Composable
fun MainScreen() {{
    Column(
        modifier = Modifier
            .fillMaxSize()
            .padding(16.dp)
    ) {{
        Text(
            text = "{analysis['name']}",
            style = MaterialTheme.typography.headlineLarge
        )
        Spacer(modifier = Modifier.height(16.dp))
        Text(
            text = "{analysis['description']}",
            style = MaterialTheme.typography.bodyLarge
        )
        Spacer(modifier = Modifier.height(24.dp))
        FeaturesList(features = listOf(
            {', '.join([f'"{f}"' for f in analysis['features'][:5]])}
        ))
    }}
}}

@Composable
fun FeaturesList(features: List<String>) {{
    Column {{
        features.forEach {{ feature ->
            Card(
                modifier = Modifier
                    .fillMaxWidth()
                    .padding(vertical = 8.dp)
            ) {{
                Text(
                    text = feature,
                    modifier = Modifier.padding(16.dp)
                )
            }}
        }}
    }}
}}
'''
    
    @staticmethod
    def create_xml_activity(package_name, analysis):
        return f'''package {package_name}

import android.os.Bundle
import androidx.appcompat.app.AppCompatActivity
import androidx.recyclerview.widget.LinearLayoutManager
import {package_name}.databinding.ActivityMainBinding

class MainActivity : AppCompatActivity() {{
    private lateinit var binding: ActivityMainBinding
    
    override fun onCreate(savedInstanceState: Bundle?) {{
        super.onCreate(savedInstanceState)
        binding = ActivityMainBinding.inflate(layoutInflater)
        setContentView(binding.root)
        
        setupUI()
        setupFeaturesList()
    }}
    
    private fun setupUI() {{
        binding.appDescription.text = "{analysis['description']}"
        binding.startButton.setOnClickListener {{
            // Handle button click
        }}
    }}
    
    private fun setupFeaturesList() {{
        val features = listOf(
            {', '.join([f'"{f}"' for f in analysis['features'][:5]])}
        )
        
        binding.featuresRecycler.apply {{
            layoutManager = LinearLayoutManager(this@MainActivity)
            adapter = FeaturesAdapter(features)
        }}
    }}
}}
'''
    
    @staticmethod
    def create_fragment(package_name, fragment_name, analysis):
        return f'''package {package_name}.ui.{fragment_name.lower()}

import android.os.Bundle
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import androidx.fragment.app.Fragment
import androidx.lifecycle.ViewModelProvider
import {package_name}.databinding.Fragment{fragment_name}Binding

class {fragment_name}Fragment : Fragment() {{
    private var _binding: Fragment{fragment_name}Binding? = null
    private val binding get() = _binding!!
    private lateinit var viewModel: {fragment_name}ViewModel
    
    override fun onCreateView(
        inflater: LayoutInflater,
        container: ViewGroup?,
        savedInstanceState: Bundle?
    ): View {{
        _binding = Fragment{fragment_name}Binding.inflate(inflater, container, false)
        return binding.root
    }}
    
    override fun onViewCreated(view: View, savedInstanceState: Bundle?) {{
        super.onViewCreated(view, savedInstanceState)
        viewModel = ViewModelProvider(this)[{fragment_name}ViewModel::class.java]
        
        setupObservers()
        setupUI()
    }}
    
    private fun setupObservers() {{
        viewModel.data.observe(viewLifecycleOwner) {{ data ->
            // Update UI
        }}
    }}
    
    private fun setupUI() {{
        // Initialize UI components
    }}
    
    override fun onDestroyView() {{
        super.onDestroyView()
        _binding = null
    }}
}}
'''
    
    @staticmethod
    def create_viewmodel(package_name, name):
        return f'''package {package_name}.ui.{name.lower()}

import androidx.lifecycle.LiveData
import androidx.lifecycle.MutableLiveData
import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import kotlinx.coroutines.launch

class {name}ViewModel : ViewModel() {{
    private val _data = MutableLiveData<List<String>>()
    val data: LiveData<List<String>> = _data
    
    private val _isLoading = MutableLiveData<Boolean>()
    val isLoading: LiveData<Boolean> = _isLoading
    
    init {{
        loadData()
    }}
    
    private fun loadData() {{
        viewModelScope.launch {{
            _isLoading.value = true
            try {{
                // Load data
                _data.value = emptyList()
            }} catch (e: Exception) {{
                // Handle error
            }} finally {{
                _isLoading.value = false
            }}
        }}
    }}
    
    fun refresh() {{
        loadData()
    }}
}}
'''
    
    @staticmethod
    def create_repository(package_name):
        return f'''package {package_name}.data

import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.withContext

class AppRepository {{
    suspend fun fetchData(): Result<List<String>> = withContext(Dispatchers.IO) {{
        try {{
            // Fetch data from API or database
            Result.success(emptyList())
        }} catch (e: Exception) {{
            Result.failure(e)
        }}
    }}
}}
'''
    
    @staticmethod
    def create_utils(package_name):
        return f'''package {package_name}.utils

import android.content.Context
import android.widget.Toast

object Utils {{
    fun Context.showToast(message: String, duration: Int = Toast.LENGTH_SHORT) {{
        Toast.makeText(this, message, duration).show()
    }}
    
    fun String.isValidEmail(): Boolean {{
        return android.util.Patterns.EMAIL_ADDRESS.matcher(this).matches()
    }}
    
    fun getCurrentTimestamp(): Long = System.currentTimeMillis()
}}

// Extension Functions
fun <T> List<T>.second(): T? = if (size >= 2) this[1] else null

fun String.capitalize(): String = 
    replaceFirstChar {{ if (it.isLowerCase()) it.titlecase() else it.toString() }}
'''
