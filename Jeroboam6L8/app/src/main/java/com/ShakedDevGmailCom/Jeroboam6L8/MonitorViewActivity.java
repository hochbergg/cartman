package com.ShakedDevGmailCom.Jeroboam6L8;

import android.content.BroadcastReceiver;
import android.content.Context;
import android.content.Intent;
import android.content.IntentFilter;
import android.net.Uri;
import android.os.Bundle;
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

import java.util.Collections;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.UUID;

public class MonitorViewActivity extends AppCompatActivity {

    private static final String BASE_URL = "http://4f997bd2.ngrok.io/api/user/take_cart/";

    private static final Map<String, String> CARTS_BY_BEACONS;

    static {
        Map<String, String> cartsByBeacons = new HashMap<>();
        cartsByBeacons.put("15250:20387", "Shaked's Cart");
        cartsByBeacons.put("62624:5060", "Agam's Cart");
        CARTS_BY_BEACONS = Collections.unmodifiableMap(cartsByBeacons);
    }

    private IntentFilter intentFilter;
    private BroadcastReceiver myReceiver = new BroadcastReceiver() {
        @Override
        public void onReceive(Context context, Intent intent) {
            String BeaconName = intent.getStringExtra("Beacon Name");
            addText(BeaconName);
        }
    };

    private BeaconManager rangeBeaconManager;
    private Region region;

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

        rangeBeaconManager = new BeaconManager(this);
        rangeBeaconManager.setRangingListener(new BeaconManager.RangingListener() {
            @Override
            public void onBeaconsDiscovered(Region region, List<Beacon> list) {

                if (!list.isEmpty()) {
                    String cartsToViewStr = "";
                    String cartsToURLStr = "";

                    for (Beacon beacon : list) {
                        String cartId = String.valueOf(beacon.getMajor()) + ":" + String.valueOf(beacon.getMinor());
                        if (CARTS_BY_BEACONS.get(cartId) != null) {

                            cartsToViewStr += (CARTS_BY_BEACONS.get(cartId)) + "\n";
                            cartsToURLStr += cartId.replace(":","") + ",";
                        }
                    }
                    if (cartsToURLStr.length() > 0) {
                        cartsToURLStr = cartsToURLStr.substring(0, cartsToURLStr.length() - 2);
                    }
                    if (cartsToViewStr.equals("")) {
                        cartsToViewStr = "No Carts Detected In My Area.";
                    }
                    else {
                        String urlMethod = "POST";
                        Log.i("HERE", cartsToURLStr);
                        RequestURL.send(BASE_URL, urlMethod, cartsToURLStr);
                    }
                    setCarts(cartsToViewStr);
                } else {
                    setCarts("No Carts Detected In My Area.");
                }

                if (!list.isEmpty()) {

                }
            }
        });

        region = new Region("ranged region",
                UUID.fromString("B9407F30-F5F8-466E-AFF9-25556B57FE6D"), null, null);

    }

    @Override
    public void onResume() {
        super.onResume();
        registerReceiver(myReceiver, intentFilter);
        rangeBeaconManager.connect(new BeaconManager.ServiceReadyCallback() {
            @Override
            public void onServiceReady() {
                rangeBeaconManager.startRanging(region);
            }
        });
    }

    @Override
    protected void onPause() {
        unregisterReceiver(myReceiver);
        rangeBeaconManager.stopRanging(region);
        super.onPause();
    }

    private void addText(String newText) {
        TextView theView = (TextView) findViewById(R.id.textView);
        String oldText = theView.getText().toString();
        theView.setText(oldText + "\n" + newText);
    }

    private void setCarts(String newText) {
        TextView theView = (TextView) findViewById(R.id.cartsList);
        theView.setText(newText);
    }

}
