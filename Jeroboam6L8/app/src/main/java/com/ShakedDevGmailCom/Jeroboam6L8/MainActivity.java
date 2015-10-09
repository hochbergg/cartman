package com.ShakedDevGmailCom.Jeroboam6L8;

import android.app.Activity;
import android.content.BroadcastReceiver;
import android.content.Context;
import android.content.Intent;
import android.content.IntentFilter;
import android.os.Handler;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.util.Log;
import android.view.Menu;
import android.view.MenuItem;
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

public class MainActivity extends Activity {

    private BeaconManager rangeBeaconManager;
    private Region region;


    private static final Map<String, String> CARTS_BY_BEACONS;

    static {
        Map<String, String> cartsByBeacons = new HashMap<>();
        cartsByBeacons.put("15250:20387", "Shaked's Cart");
        cartsByBeacons.put("62624:5060", "Agam's Cart");
        CARTS_BY_BEACONS = Collections.unmodifiableMap(cartsByBeacons);
    }

    private final Handler handler = new Handler();


    private Runnable updateShopStatus = new Runnable() {
        public void run() {
            GetUiUpdates();
            handler.postDelayed(this, 5000); // 5 seconds
        }
    };

    private void GetUiUpdates() {
        String cartsJSON = "{\"msg\":123}";
        String path = "/api/user/notifications/";
        Log.i("PATH", path);
        JSONObject requestResponse = RequestURL.sendJSON(path, cartsJSON);
        String responseText = "";
        try {
            responseText = requestResponse.getString("notifications").toString();
        } catch (JSONException e) {
            e.printStackTrace();
        }
        Log.i("RESPONSE", responseText);
        if (responseText.contains("CART_TAKEN")) {
            Intent intent = new Intent(this, RentingActivity.class);
            startActivity(intent);
        }
    }

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        String loginPath = "/auth/login/";
        String loginJson = "{\"username\":\"tori\",\"password\":\"tori\"}";
        JSONObject jsonResponse = RequestURL.sendJSON(loginPath, loginJson);
        String accessToken = null;
        try {
            accessToken = jsonResponse.getString("access_token");
        } catch (JSONException e) {
            e.printStackTrace();
        }
        Log.i("ACCESS_TOKEN", accessToken);
        RequestURL.setAccessToken(accessToken);

        region = new Region("ranged region",
                UUID.fromString("B9407F30-F5F8-466E-AFF9-25556B57FE6D"), null, null);

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
                            cartId = cartId.replace(":", "");
                            String cartPowerStr = String.valueOf(beacon.getRssi());
                            cartsToURLStr += "{\"cart_id\":" + cartId + ",\"power\":" + cartPowerStr + "},";
                        }
                    }
                    if (cartsToURLStr.length() > 0) {
                        cartsToURLStr = cartsToURLStr.substring(0, cartsToURLStr.length() - 1);
                    }
                    if (cartsToViewStr.equals("")) {
                        cartsToViewStr = "No Carts Detected In My Area.";
                    } else {
                        String cartsJSON = "{\"cart_ids\":[" + cartsToURLStr + "]}";
                        Log.i("HERE. JSON:", cartsJSON);
                        String path = "/api/location/nearby_carts/";
                        RequestURL.sendJSON(path, cartsJSON);
                    }
                } else {
                }

                if (!list.isEmpty()) {

                }
            }
        });

    }

    @Override
    public boolean onCreateOptionsMenu(Menu menu) {
        // Inflate the menu; this adds items to the action bar if it is present.
        getMenuInflater().inflate(R.menu.menu_main, menu);
        return true;
    }

    @Override
    public boolean onOptionsItemSelected(MenuItem item) {
        // Handle action bar item clicks here. The action bar will
        // automatically handle clicks on the Home/Up button, so long
        // as you specify a parent activity in AndroidManifest.xml.
        int id = item.getItemId();

        //noinspection SimplifiableIfStatement
        if (id == R.id.action_settings) {
            return true;
        }

        return super.onOptionsItemSelected(item);
    }


    @Override
    public void onResume() {
        super.onResume();

        rangeBeaconManager.connect(new BeaconManager.ServiceReadyCallback() {
            @Override
            public void onServiceReady() {
                rangeBeaconManager.startRanging(region);
            }
        });

        handler.removeCallbacks(updateShopStatus);
        handler.postDelayed(updateShopStatus, 500); // 1 second
    }

    @Override
    protected void onPause() {
        super.onPause();
    }

    public void navigateToChoose(View view) {
        Intent intent = new Intent(this, ChooseCartActivity.class);
        startActivity(intent);
    }

    private void setCarts(String newText) {
        TextView theView = (TextView) findViewById(R.id.cartsList);
        theView.setText(newText);
    }
}
