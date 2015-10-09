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

    public static void send(String urlStr, String urlMethod, String cartListStr) {
        StrictMode.ThreadPolicy policy =
                new StrictMode.ThreadPolicy.Builder().permitAll().build();
        StrictMode.setThreadPolicy(policy);

        try {
            URL url = new URL(urlStr);
            HttpURLConnection urlConnection = (HttpURLConnection) url.openConnection();
            urlConnection.setRequestMethod(urlMethod);
            urlConnection.setRequestProperty("Content-Type","application/json");
            DataOutputStream out = new DataOutputStream(urlConnection.getOutputStream());
            out.writeBytes("\n{\"cart_id\":[" + cartListStr + "]}");
            out.flush();
            out.close();
            InputStream in = new BufferedInputStream(urlConnection.getInputStream());
            JsonReader reader = new JsonReader(new InputStreamReader(in, "UTF-8"));


//            URL url;
//            URLConnection urlConn;
//            DataOutputStream printout;
//            DataInputStream input;
//            url = new URL (urlStr);
//            urlConn = url.openConnection();
//            urlConn.setDoInput (true);
//            urlConn.setDoOutput (true);
//            urlConn.setUseCaches (false);
//            urlConn.setRequestProperty("Content-Type","application/json");
//            urlConn.setRequestProperty("Host", "android.schoolportal.gr");
//            urlConn.connect();
//            //Create JSONObject here
//            JSONObject jsonParam = new JSONObject();
//            jsonParam.put("cart_ids", "[1,2,3,4]");
//
//            // Send POST output.
//            printout = new DataOutputStream(urlConn.getOutputStream ());
//            printout.writeBytes(URLEncoder.encode(jsonParam.toString(), "UTF-8"));
//            printout.flush ();
//            printout.close();

//            Log.i(TAG, reader.toString());

        } catch (IOException e) {
            Log.i(TAG, "IO Exception");
        }
    }
}
