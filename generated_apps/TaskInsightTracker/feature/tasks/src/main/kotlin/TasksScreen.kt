package com.titan.finance.feature.tasks

import androidx.compose.runtime.*
import androidx.compose.material3.*
import androidx.hilt.navigation.compose.hiltViewModel

// AI Architecture Note: Feature module with isolated dependencies
// This allows parallel development and independent testing

@Composable
fun TasksScreen(
    viewModel: TasksViewModel = hiltViewModel()
) {
    val uiState by viewModel.uiState.collectAsState()
    
    // UI implementation
}
