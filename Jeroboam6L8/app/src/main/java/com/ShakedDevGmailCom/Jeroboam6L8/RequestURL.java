package com.ShakedDevGmailCom.Jeroboam6L8;

import android.os.StrictMode;
import android.util.JsonReader;
import android.util.Log;

import java.io.BufferedInputStream;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.net.HttpURLConnection;
import java.net.URL;
import java.util.Map;

/**
 * Created by agamrafaeli on 09/10/15.
 */
public class RequestURL {
    private static final String TAG = ".RequestURL";

    public static void send(String urlStr, String urlMethod) {
        StrictMode.ThreadPolicy policy =
                new StrictMode.ThreadPolicy.Builder().permitAll().build();
        StrictMode.setThreadPolicy(policy);

        try {
            URL url = new URL(urlStr);
            HttpURLConnection urlConnection = (HttpURLConnection) url.openConnection();
            urlConnection.setRequestMethod(urlMethod);
            InputStream in = new BufferedInputStream(urlConnection.getInputStream());
            JsonReader reader = new JsonReader(new InputStreamReader(in, "UTF-8"));
            Log.i(TAG, reader.toString());

        } catch (IOException e) {
            Log.i(TAG, "IO Exception");
        }
    }
}
