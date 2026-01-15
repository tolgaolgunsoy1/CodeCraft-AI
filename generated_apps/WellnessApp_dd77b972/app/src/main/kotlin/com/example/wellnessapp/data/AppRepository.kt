package com.example.wellnessapp.data

import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.withContext

class AppRepository {
    suspend fun fetchData(): Result<List<String>> = withContext(Dispatchers.IO) {
        try {
            // Fetch data from API or database
            Result.success(emptyList())
        } catch (e: Exception) {
            Result.failure(e)
        }
    }
}
