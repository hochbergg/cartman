package com.ShakedDevGmailCom.Jeroboam6L8;

import android.os.StrictMode;
import android.util.JsonReader;
import android.util.Log;

import org.json.JSONException;
import org.json.JSONObject;

import java.io.BufferedInputStream;
import java.io.DataInputStream;
import java.io.DataOutputStream;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.io.OutputStream;
import java.net.HttpURLConnection;
import java.net.URL;
import java.net.URLConnection;
import java.net.URLEncoder;
import java.util.Map;

/**
 * Created by agamrafaeli on 09/10/15.
 */
public class RequestURL {
    private static final String TAG = ".RequestURL";
    private static final String HOME_URL = "http://7d640600.ngrok.io";
    private static final String URL_METHOD = "POST";
    private static String ACCESS_TOKEN;

    public static String sendJSON(String path, String jsonToSend) {
        StrictMode.ThreadPolicy policy =
                new StrictMode.ThreadPolicy.Builder().permitAll().build();
        StrictMode.setThreadPolicy(policy);

        try {
            URL url = new URL(HOME_URL + path);
            HttpURLConnection urlConnection = (HttpURLConnection) url.openConnection();
            urlConnection.setRequestMethod(URL_METHOD);
            urlConnection.setRequestProperty("Content-Type", "application/json");
            DataOutputStream out = new DataOutputStream(urlConnection.getOutputStream());
            jsonToSend = jsonToSend.substring(0, jsonToSend.length() - 2);
            jsonToSend += ",\"access_token\":\"" + ACCESS_TOKEN + "\"}";
            Log.i("JSONNNN : ", jsonToSend);
            out.writeBytes(jsonToSend);
            out.flush();
            out.close();
            String responseMessage = urlConnection.getResponseMessage();


            return responseMessage;


        } catch (IOException e) {
            Log.i(TAG, "IO Exception");
        }

        return "";
    }

    public static void setAccessToken(String newAccessToken) {
        RequestURL.ACCESS_TOKEN = newAccessToken;
    }
}
