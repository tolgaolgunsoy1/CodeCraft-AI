package com.titan.finance.feature.tasks

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import dagger.hilt.android.lifecycle.HiltViewModel
import kotlinx.coroutines.flow.*
import javax.inject.Inject

// AI Architecture Note: ViewModel with StateFlow for reactive UI
// ViewModelScope ensures proper lifecycle management

@HiltViewModel
class TasksViewModel @Inject constructor(
    // Inject use cases here
) : ViewModel() {
    
    private val _uiState = MutableStateFlow(TasksUiState())
    val uiState: StateFlow<TasksUiState> = _uiState.asStateFlow()
    
    // Business logic
}

data class TasksUiState(
    val isLoading: Boolean = false,
    val error: String? = null
)
