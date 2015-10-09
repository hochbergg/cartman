package com.ShakedDevGmailCom.Jeroboam6L8;

import android.content.BroadcastReceiver;
import android.content.Context;
import android.content.Intent;
import android.content.IntentFilter;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.view.Menu;
import android.view.MenuItem;
import android.view.View;
import android.os.CountDownTimer;
import android.widget.TextView;

public class RentingActivity extends AppCompatActivity {


    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_renting);

        new CountDownTimer(20000, 1000) {

            public void onTick(long millisUntilFinished) {
                long hoursUntilFinished = millisUntilFinished / 1000 / 60 / 60;
                long minutesUntilFinished = millisUntilFinished / 1000 / 60 - (hoursUntilFinished * 60);
                long secondsUntilFinished = millisUntilFinished / 1000  - (hoursUntilFinished * 60 * 60) - (minutesUntilFinished * 60);

                ((TextView)findViewById(R.id.digit11)).setText("" + (hoursUntilFinished));
                ((TextView)findViewById(R.id.digit21)).setText("" + (minutesUntilFinished / 10));
                ((TextView)findViewById(R.id.digit22)).setText("" + (minutesUntilFinished - (minutesUntilFinished / 10 * 10)));
                ((TextView)findViewById(R.id.digit31)).setText("" + (secondsUntilFinished / 10));
                ((TextView)findViewById(R.id.digit32)).setText("" + (secondsUntilFinished - (secondsUntilFinished / 10 * 10)));
            }

            public void onFinish() {
                navigateToStolen();
            }
        }.start();
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
    }

    @Override
    protected void onPause() {
        super.onPause();
    }

    public void navigateToDone(View view) {
        Intent intent = new Intent(this, DoneActivity.class);
        startActivity(intent);
    }

    public void navigateToStolen() {
        Intent intent = new Intent(this, StolenActivity.class);
        startActivity(intent);
    }
}
