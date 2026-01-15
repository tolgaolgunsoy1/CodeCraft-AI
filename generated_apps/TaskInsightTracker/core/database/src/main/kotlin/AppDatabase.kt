package com.titan.finance.core.database

import androidx.room.Database
import androidx.room.RoomDatabase

// AI Architecture Note: Single source of truth for data persistence
// Room database with type-safe queries and compile-time verification
@Database(entities = [], version = 1, exportSchema = false)
abstract class AppDatabase : RoomDatabase() {
    // Define your DAOs here
    // abstract fun taskDao(): TaskDao
}
