package com.example.healthtracker

import android.os.Bundle
import androidx.appcompat.app.AppCompatActivity
import androidx.recyclerview.widget.LinearLayoutManager
import com.example.healthtracker.databinding.ActivityMainBinding

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
        binding.appDescription.text = "Saðlýk ve fitness takip uygulamasý"
        binding.startButton.setOnClickListener {
            // Handle button click
        }
    }
    
    private fun setupFeaturesList() {
        val features = listOf(
            "Adým sayacý", "Kalori hesaplama", "Egzersiz planlarý", "Su tüketimi takibi", "Kilo takibi"
        )
        
        binding.featuresRecycler.apply {
            layoutManager = LinearLayoutManager(this@MainActivity)
            adapter = FeaturesAdapter(features)
        }
    }
}
