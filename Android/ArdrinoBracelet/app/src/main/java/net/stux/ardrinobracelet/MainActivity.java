package net.stux.ardrinobracelet;

import android.bluetooth.BluetoothSocket;
import android.content.Intent;
import android.provider.SyncStateContract;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.util.Log;
import android.widget.Toast;

import java.io.IOException;
import java.io.InputStream;
import java.io.OutputStream;

import app.akexorcist.bluetotohspp.library.BluetoothSPP;
import app.akexorcist.bluetotohspp.library.BluetoothState;
import app.akexorcist.bluetotohspp.library.DeviceList;

public class MainActivity extends AppCompatActivity {

    final String TAG = "MainActivity";

    
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        BluetoothSPP bt = new BluetoothSPP(MainActivity.this);

        if(!bt.isBluetoothAvailable()) {
            // any command for bluetooth is not available
        }

        // Android device
        //bt.startService(BluetoothState.DEVICE_ANDROID);

        // Arduino
        bt.startService(BluetoothState.DEVICE_OTHER);

        Intent intent = new Intent(getApplicationContext(), DeviceList.class);
        startActivityForResult(intent, BluetoothState.REQUEST_CONNECT_DEVICE);


        // Listen for data
        bt.setOnDataReceivedListener(new BluetoothSPP.OnDataReceivedListener() {
            public void onDataReceived(byte[] data, String message) {
                // Do something when data incoming
                Toast.makeText(MainActivity.this, message, Toast.LENGTH_SHORT).show();
            }
        });



    }



}
