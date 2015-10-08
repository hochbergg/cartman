package com.ShakedDevGmailCom.Jeroboam6L8;

import android.app.Application;
import android.app.Notification;
import android.app.NotificationManager;
import android.app.PendingIntent;
import android.content.BroadcastReceiver;
import android.content.Context;
import android.content.Intent;
import android.content.IntentFilter;
import android.util.Log;
import android.widget.TextView;

import com.estimote.sdk.Beacon;
import com.estimote.sdk.BeaconManager;
import com.estimote.sdk.EstimoteSDK;
import com.estimote.sdk.Region;


import java.util.List;
import java.util.UUID;

public class MyApplication extends Application {
    private static final String TAG = ".MyApplicationName";

    private BeaconManager beaconManager;
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
                sendBroadcast(intent);
                showNotification("Enter notification", msg);
            }
            @Override
            public void onExitedRegion(Region region) {
                String msg = "Exited " + region.getIdentifier().toString();
                Log.i(TAG, msg);
                Intent intent = new Intent("com.hmkcode.android.USER_ACTION");
                intent.putExtra("Beacon Name", msg);
                sendBroadcast(intent);
                showNotification("Exit notification", msg);
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
    }

    public void showNotification(String title, String message) {
        Intent notifyIntent = new Intent(this, MainActivity.class);
        notifyIntent.setFlags(Intent.FLAG_ACTIVITY_SINGLE_TOP);
        PendingIntent pendingIntent = PendingIntent.getActivities(this, 0,
                new Intent[] { notifyIntent }, PendingIntent.FLAG_UPDATE_CURRENT);
        Notification notification = new Notification.Builder(this)
                .setSmallIcon(android.R.drawable.ic_dialog_info)
                .setContentTitle(title)
                .setContentText(message)
                .setAutoCancel(true)
                .setContentIntent(pendingIntent)
                .build();
        notification.defaults |= Notification.DEFAULT_SOUND;
        NotificationManager notificationManager =
                (NotificationManager) getSystemService(Context.NOTIFICATION_SERVICE);
        notificationManager.notify(1, notification);
    }

}