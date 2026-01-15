package com.example.customapp.utils

import android.content.Context
import android.widget.Toast

object Utils {
    fun Context.showToast(message: String, duration: Int = Toast.LENGTH_SHORT) {
        Toast.makeText(this, message, duration).show()
    }
    
    fun String.isValidEmail(): Boolean {
        return android.util.Patterns.EMAIL_ADDRESS.matcher(this).matches()
    }
    
    fun getCurrentTimestamp(): Long = System.currentTimeMillis()
}

// Extension Functions
fun <T> List<T>.second(): T? = if (size >= 2) this[1] else null

fun String.capitalize(): String = 
    replaceFirstChar { if (it.isLowerCase()) it.titlecase() else it.toString() }
