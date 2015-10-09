package com.ShakedDevGmailCom.Jeroboam6L8;

import android.app.Application;
import android.app.Notification;
import android.app.NotificationManager;
import android.app.PendingIntent;
import android.content.BroadcastReceiver;
import android.content.Context;
import android.content.Intent;
import android.content.IntentFilter;
import android.net.Uri;
import android.os.StrictMode;
import android.util.JsonReader;
import android.util.Log;
import android.widget.TextView;

import com.estimote.sdk.Beacon;
import com.estimote.sdk.BeaconManager;
import com.estimote.sdk.EstimoteSDK;
import com.estimote.sdk.Region;


import java.io.BufferedInputStream;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.net.HttpURLConnection;
import java.net.URL;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.UUID;

public class MyApplication extends Application {
    private static final String TAG = ".MyApplicationName";
    private BeaconManager beaconManager;
    private BeaconManager rangeBeaconManager;
    BroadcastReceiver myReceiver;
    IntentFilter intentFilter;

    @Override
    public void onCreate() {
        super.onCreate();
        Log.d(TAG, "App started up");
        beaconManager = new BeaconManager(getApplicationContext());
        beaconManager.setMonitoringListener(new BeaconManager.MonitoringListener() {
            @Override
            public void onEnteredRegion(Region region, List<Beacon> list) {
                String msg = "Entered " + region.getIdentifier().toString();
                Log.i(TAG, msg);
                Intent intent = new Intent("com.hmkcode.android.USER_ACTION");
                intent.putExtra("Beacon Name", msg);
//                sendBroadcast(intent);
            }

            @Override
            public void onExitedRegion(Region region) {
                String msg = "Exited " + region.getIdentifier().toString();
                Log.i(TAG, msg);
                Intent intent = new Intent("com.hmkcode.android.USER_ACTION");
                intent.putExtra("Beacon Name", msg);
//                sendBroadcast(intent);
            }
        });
        beaconManager.connect(new BeaconManager.ServiceReadyCallback() {
            @Override
            public void onServiceReady() {
                beaconManager.startMonitoring(new Region(
                        "Beacon 1", UUID.fromString("B9407F30-F5F8-466E-AFF9-25556B57FE6D"), 15250, 20387));
                beaconManager.startMonitoring(new Region(
                        "Beacon 2", UUID.fromString("B9407F30-F5F8-466E-AFF9-25556B57FE6D"), 62624, 5060));
            }
        });
        beaconManager.setBackgroundScanPeriod(5,2);

        rangeBeaconManager = new BeaconManager(getApplicationContext());
        rangeBeaconManager.setMonitoringListener(new BeaconManager.MonitoringListener() {
            @Override
            public void onEnteredRegion(Region region, List<Beacon> list) {
                Log.d(TAG, list.toString());
            }

            @Override
            public void onExitedRegion(Region region) {
                // could add an "exit" notification too if you want (-:
            }
        });
        rangeBeaconManager.connect(new BeaconManager.ServiceReadyCallback() {
            @Override
            public void onServiceReady() {
                rangeBeaconManager.startMonitoring(new Region("monitored region",
                        UUID.fromString("B9407F30-F5F8-466E-AFF9-25556B57FE6D"), 22504, 48827));
            }
        });

    }

}