package com.example.healthtracker;

import androidx.lifecycle.ViewModel;
import androidx.lifecycle.MutableLiveData;
import androidx.lifecycle.LiveData;
import android.util.Log;

public class MainViewModel extends ViewModel {
    private static final String TAG = "MainViewModel";
    private MutableLiveData<AppState> appState = new MutableLiveData<>();
    private MutableLiveData<Boolean> isLoading = new MutableLiveData<>();
    
    public MainViewModel() {
        appState.setValue(new AppState(true, "App initialized"));
        isLoading.setValue(false);
    }
    
    public LiveData<AppState> getAppState() {
        return appState;
    }
    
    public LiveData<Boolean> getIsLoading() {
        return isLoading;
    }
    
    public void initializeApp() {
        isLoading.setValue(true);
        // Simulate initialization
        try {
            Thread.sleep(1000);
            appState.setValue(new AppState(true, "App ready"));
        } catch (InterruptedException e) {
            Log.e(TAG, "Initialization interrupted", e);
            appState.setValue(new AppState(false, "Initialization failed"));
        } finally {
            isLoading.setValue(false);
        }
    }
    
    public void cleanup() {
        Log.d(TAG, "ViewModel cleanup");
    }
    
    @Override
    protected void onCleared() {
        super.onCleared();
        cleanup();
    }
}