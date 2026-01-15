package com.example.customapp;

public class AppState {
    private boolean ready;
    private String message;
    
    public AppState(boolean ready, String message) {
        this.ready = ready;
        this.message = message;
    }
    
    public boolean isReady() {
        return ready;
    }
    
    public String getMessage() {
        return message;
    }
    
    public void setReady(boolean ready) {
        this.ready = ready;
    }
    
    public void setMessage(String message) {
        this.message = message;
    }
}