package com.example.edupro

import android.os.Bundle
import androidx.appcompat.app.AppCompatActivity
import androidx.recyclerview.widget.LinearLayoutManager
import com.example.edupro.databinding.ActivityMainBinding

class MainActivity : AppCompatActivity() {
    private lateinit var binding: ActivityMainBinding
    
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        binding = ActivityMainBinding.inflate(layoutInflater)
        setContentView(binding.root)
        
        setupUI()
        setupFeaturesList()
    }
    
    private fun setupUI() {
        binding.appDescription.text = "Özel uygulama: Eðitim platformu ve öðrenme yönetimi sistemi"
        binding.startButton.setOnClickListener {
            // Handle button click
        }
    }
    
    private fun setupFeaturesList() {
        val features = listOf(
            "Görev oluþturma", "Kategori yönetimi", "Hatýrlatýcýlar", "Ýlerleme takibi", "Takvim entegrasyonu"
        )
        
        binding.featuresRecycler.apply {
            layoutManager = LinearLayoutManager(this@MainActivity)
            adapter = FeaturesAdapter(features)
        }
    }
}
