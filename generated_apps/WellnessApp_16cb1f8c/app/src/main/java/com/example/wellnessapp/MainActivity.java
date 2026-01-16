package com.example.wellnessapp;

import androidx.appcompat.app.AppCompatActivity;
import androidx.recyclerview.widget.GridLayoutManager;
import androidx.recyclerview.widget.RecyclerView;
import com.google.android.material.bottomnavigation.BottomNavigationView;
import android.content.Intent;
import android.os.Bundle;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.TextView;
import java.util.ArrayList;
import java.util.List;

public class MainActivity extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        
        setupDashboard();
        setupBottomNavigation();
    }
    
    private void setupDashboard() {
        RecyclerView recyclerView = findViewById(R.id.dashboard_recycler);
        recyclerView.setLayoutManager(new GridLayoutManager(this, 2));
        
        List<DashboardItem> items = new ArrayList<>();
        items.add(new DashboardItem("Profile", ProfileActivity.class));
        items.add(new DashboardItem("Settings", SettingsActivity.class));
        items.add(new DashboardItem("Detail", DetailActivity.class));
        items.add(new DashboardItem("Onboarding", OnboardingActivity.class));
        
        recyclerView.setAdapter(new DashboardAdapter(items));
    }
    
    private void setupBottomNavigation() {
        BottomNavigationView bottomNav = findViewById(R.id.bottom_navigation);
        bottomNav.setOnItemSelectedListener(item -> {
            return true;
        });
    }
    
    class DashboardItem {
        String title;
        Class<?> activityClass;
        DashboardItem(String t, Class<?> c) { title = t; activityClass = c; }
    }
    
    class DashboardAdapter extends RecyclerView.Adapter<DashboardAdapter.ViewHolder> {
        List<DashboardItem> items;
        DashboardAdapter(List<DashboardItem> i) { items = i; }
        
        @Override
        public ViewHolder onCreateViewHolder(ViewGroup parent, int viewType) {
            TextView tv = new TextView(parent.getContext());
            tv.setPadding(48, 96, 48, 96);
            tv.setTextSize(20);
            tv.setTextColor(0xFF000000);
            tv.setBackgroundColor(0xFFE3F2FD);
            tv.setGravity(17);
            ViewGroup.MarginLayoutParams params = new ViewGroup.MarginLayoutParams(
                ViewGroup.LayoutParams.MATCH_PARENT, ViewGroup.LayoutParams.WRAP_CONTENT);
            params.setMargins(16, 16, 16, 16);
            tv.setLayoutParams(params);
            return new ViewHolder(tv);
        }
        
        @Override
        public void onBindViewHolder(ViewHolder holder, int position) {
            DashboardItem item = items.get(position);
            holder.textView.setText(item.title);
            holder.textView.setOnClickListener(v -> 
                startActivity(new Intent(MainActivity.this, item.activityClass)));
        }
        
        @Override
        public int getItemCount() { return items.size(); }
        
        class ViewHolder extends RecyclerView.ViewHolder {
            TextView textView;
            ViewHolder(TextView tv) { super(tv); textView = tv; }
        }
    }
}