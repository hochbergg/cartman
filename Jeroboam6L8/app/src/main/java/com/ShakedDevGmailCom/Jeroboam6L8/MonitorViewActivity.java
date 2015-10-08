package com.ShakedDevGmailCom.Jeroboam6L8;

import android.content.BroadcastReceiver;
import android.content.Context;
import android.content.Intent;
import android.content.IntentFilter;
import android.os.Bundle;
import android.support.design.widget.FloatingActionButton;
import android.support.design.widget.Snackbar;
import android.support.v7.app.AppCompatActivity;
import android.support.v7.widget.Toolbar;
import android.view.View;
import android.widget.TextView;

public class MonitorViewActivity extends AppCompatActivity {
    private IntentFilter intentFilter;
    private BroadcastReceiver myReceiver = new BroadcastReceiver() {
        @Override
        public void onReceive(Context context, Intent intent) {
            String BeaconName = intent.getStringExtra("Beacon Name");
            addText(BeaconName);
        }
    };

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_monitor_view);
        Toolbar toolbar = (Toolbar) findViewById(R.id.toolbar);
        setSupportActionBar(toolbar);

        FloatingActionButton fab = (FloatingActionButton) findViewById(R.id.fab);
        fab.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                Snackbar.make(view, "Replace with your own action", Snackbar.LENGTH_LONG)
                        .setAction("Action", null).show();
            }
        });

        intentFilter = new IntentFilter("com.hmkcode.android.USER_ACTION");
    }

    @Override
    public void onResume() {
        super.onResume();
        registerReceiver(myReceiver , intentFilter);
    }

    @Override
    protected void onPause() {
        unregisterReceiver(myReceiver);
        super.onPause();
    }

    private void addText(String newText) {
        TextView theView = (TextView) findViewById(R.id.textView);
        String oldText = theView.getText().toString();
        theView.setText(oldText + "\n" + newText);
    }

}
