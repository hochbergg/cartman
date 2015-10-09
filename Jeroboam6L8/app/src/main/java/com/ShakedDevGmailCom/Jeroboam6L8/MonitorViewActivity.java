package com.ShakedDevGmailCom.Jeroboam6L8;

import android.content.BroadcastReceiver;
import android.content.Context;
import android.content.Intent;
import android.content.IntentFilter;
import android.net.Uri;
import android.os.Bundle;
import android.os.Handler;
import android.support.design.widget.FloatingActionButton;
import android.support.design.widget.Snackbar;
import android.support.v7.app.AppCompatActivity;
import android.support.v7.widget.Toolbar;
import android.util.Log;
import android.view.View;
import android.widget.TextView;

import com.estimote.sdk.Beacon;
import com.estimote.sdk.BeaconManager;
import com.estimote.sdk.Region;

import org.json.JSONException;
import org.json.JSONObject;

import java.util.Collections;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.UUID;

public class MonitorViewActivity extends AppCompatActivity {

    private static final String BASE_URL = "http://f700f36c.ngrok.io/api/location/nearby_carts/";



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



//        region = new Region("ranged region",
//                UUID.fromString("B9407F30-F5F8-466E-AFF9-25556B57FE6D"), null, null);




    }

    @Override
    public void onResume() {
        super.onResume();
        registerReceiver(myReceiver, intentFilter);
//
//        handler.removeCallbacks(updateShopStatus);
//        handler.postDelayed(updateShopStatus, 1000); // 1 second
    }

    @Override
    protected void onPause() {
        unregisterReceiver(myReceiver);
//        rangeBeaconManager.stopRanging(region);
        super.onPause();
    }

    private void addText(String newText) {
        TextView theView = (TextView) findViewById(R.id.textView);
        String oldText = theView.getText().toString();
        theView.setText(oldText + "\n" + newText);
    }



}
