package com.ShakedDevGmailCom.Jeroboam6L8;

import android.app.Application;

import com.estimote.sdk.BeaconManager;
import com.estimote.sdk.EstimoteSDK;
import com.estimote.sdk.Region;

import java.util.UUID;

public class MyApplication extends Application {

//    private BeaconManager beaconManager = new BeaconManager(getApplicationContext());

    @Override
    public void onCreate() {
        super.onCreate();

        EstimoteSDK.initialize(getApplicationContext(), "jeroboam-6l8", "131b26668ac79579213dbe83b03583b9");

        // uncomment to enable debug-level logging
        // it's usually only a good idea when troubleshooting issues with the Estimote SDK
//        EstimoteSDK.enableDebugLogging(true);

//        beaconManager.connect(new BeaconManager.ServiceReadyCallback() {
//            @Override
//            public void onServiceReady() {
//                beaconManager.startMonitoring(new Region(
//                        "all Estimote Beacons with default UUID",
//                        UUID.fromString("B9407F30-F5F8-466E-AFF9-25556B57FE6D"),
//                        null, null));
//            }
//        });
    }
}
