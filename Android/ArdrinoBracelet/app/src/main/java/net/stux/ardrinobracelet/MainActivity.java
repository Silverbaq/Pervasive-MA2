package net.stux.ardrinobracelet;

import android.app.Activity;
import android.bluetooth.BluetoothAdapter;
import android.bluetooth.BluetoothSocket;
import android.content.Intent;
import android.graphics.Matrix;
import android.provider.SyncStateContract;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.util.Log;
import android.view.MotionEvent;
import android.view.View;
import android.widget.Button;
import android.widget.ImageView;
import android.widget.Toast;

import org.java_websocket.server.WebSocketServer;

import java.io.DataInputStream;
import java.io.IOException;
import java.io.InputStream;
import java.io.OutputStream;
import java.net.InetSocketAddress;
import java.net.ServerSocket;
import java.net.Socket;
import java.util.Observable;
import java.util.Observer;

import app.akexorcist.bluetotohspp.library.BluetoothSPP;
import app.akexorcist.bluetotohspp.library.BluetoothState;
import app.akexorcist.bluetotohspp.library.DeviceList;

public class MainActivity extends AppCompatActivity {

    BluetoothSPP bt;
    private ImageView mImageView;

    // image position
    float currentImageX, currentImageY;

    // Image zoom
    private Matrix matrix = new Matrix();
    float zoom = 0;

    // Socket server
    ServerSocket server;
    boolean running = false;

    //SimpleServer server;

    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        Button btnConnect = (Button) findViewById(R.id.btnConnect);
        mImageView = (ImageView) findViewById(R.id.imageView);

        Button btn1 = (Button) findViewById(R.id.button);
        Button btn2 = (Button) findViewById(R.id.button2);

        btn1.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                zoomImageIn(0.1f);
            }
        });

        btn2.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                zoomImageOut(0.1f);

                // ***** TEST WEB SOCKET SERVER ****
                startServer();
            }
        });

        bt = new BluetoothSPP(this);


        // *** BLUETOOTH ***

        if (!bt.isBluetoothAvailable()) {
            Toast.makeText(getApplicationContext()
                    , "Bluetooth is not available"
                    , Toast.LENGTH_SHORT).show();
            finish();
        }

        //
        // On incoming data from bluetooth
        bt.setOnDataReceivedListener(new BluetoothSPP.OnDataReceivedListener() {
            public void onDataReceived(byte[] data, String message) {
                Toast.makeText(MainActivity.this, message, Toast.LENGTH_SHORT).show();
            }
        });

        //
        // Informs about connection status for bluetooth (if status changes
        bt.setBluetoothConnectionListener(new BluetoothSPP.BluetoothConnectionListener() {
            public void onDeviceConnected(String name, String address) {
                Toast.makeText(getApplicationContext()
                        , "Connected to " + name + "\n" + address
                        , Toast.LENGTH_SHORT).show();
            }

            public void onDeviceDisconnected() {
                Toast.makeText(getApplicationContext()
                        , "Connection lost", Toast.LENGTH_SHORT).show();
            }

            public void onDeviceConnectionFailed() {
                Toast.makeText(getApplicationContext()
                        , "Unable to connect", Toast.LENGTH_SHORT).show();
            }
        });


        //
        // To list devices to connect to
        btnConnect.setOnClickListener(new View.OnClickListener() {
            public void onClick(View v) {
                if (bt.getServiceState() == BluetoothState.STATE_CONNECTED) {
                    bt.disconnect();
                } else {
                    Intent intent = new Intent(getApplicationContext(), DeviceList.class);
                    startActivityForResult(intent, BluetoothState.REQUEST_CONNECT_DEVICE);
                }
            }
        });
    }

    // *** Bluetooth settings ***
    // *** BEGIN ***

    public void onDestroy() {
        super.onDestroy();
        bt.stopService();
    }

    public void onStart() {
        super.onStart();
        if (!bt.isBluetoothEnabled()) {
            Intent intent = new Intent(BluetoothAdapter.ACTION_REQUEST_ENABLE);
            startActivityForResult(intent, BluetoothState.REQUEST_ENABLE_BT);
        } else {
            if (!bt.isServiceAvailable()) {
                bt.setupService();
                bt.startService(BluetoothState.DEVICE_OTHER);
                setup();
            }
        }
    }

    public void setup() {
        // TODO: code for setup if needed
    }

    public void onActivityResult(int requestCode, int resultCode, Intent data) {
        if (requestCode == BluetoothState.REQUEST_CONNECT_DEVICE) {
            if (resultCode == Activity.RESULT_OK)
                bt.connect(data);
        } else if (requestCode == BluetoothState.REQUEST_ENABLE_BT) {
            if (resultCode == Activity.RESULT_OK) {
                bt.setupService();
                bt.startService(BluetoothState.DEVICE_ANDROID);
                setup();
            } else {
                Toast.makeText(getApplicationContext()
                        , "Bluetooth was not enabled."
                        , Toast.LENGTH_SHORT).show();
                finish();
            }
        }
    }
    // *** Bluetooth settings ***
    // *** END ***


    // *** Image control **
    // *** BEGIN ***

    private void moveImageDown(float speed) {
        mImageView.scrollBy(0, (int) speed);
    }

    private void moveImageUp(float speed) {
        mImageView.scrollBy(0, (int) speed);
    }

    private void moveImageLeft(float speed) {
        mImageView.scrollBy((int) speed, 0);
    }

    private void moveImageRight(float speed) {
        mImageView.scrollBy((int) speed, 0);
    }

    private void zoomImageIn(float speed) {


        float x = mImageView.getScaleX();
        float y = mImageView.getScaleY();

        mImageView.setScaleX((float) (x + speed));
        mImageView.setScaleY((float) (y + speed));

    }

    private void zoomImageOut(float speed) {
        float x = mImageView.getScaleX();
        float y = mImageView.getScaleY();

        mImageView.setScaleX((float) (x - speed));
        mImageView.setScaleY((float) (y - speed));
    }


    // *** Image control **
    // *** END ***


    public void startServer() {
        running = true;
        int port = 5000;
        String ip = "0.0.0.0";


        try {
            server = new ServerSocket(port);
        } catch (IOException e) {
            e.printStackTrace();
        }

        Log.d("SERVER", "Server started");
        Log.d("SERVER", server.getInetAddress().getHostAddress());

        Thread t = new Thread(new Runnable() {
            @Override
            public void run() {
                while (running) {
                    Socket client = null;
                    try {
                        client = server.accept();

                        clientHandler(client);
                    } catch (IOException e) {
                        e.printStackTrace();
                    }

                }
            }
        });
        t.start();
    }

    void clientHandler(Socket socket) {
        Log.d("SERVER", "Someone connected!!!");
        try {
            DataInputStream dIn = new DataInputStream(socket.getInputStream());

            while (true) {
                // TODO : CODE!!
                String input = dIn.readLine();
                Log.d("SERVER", input);

                switch (input) {
                    case "1":
                        moveImageLeft(10);
                        break;
                    case "2":
                        moveImageRight(-10);
                        break;
                    case "3":
                        moveImageUp(10);
                        break;
                    case "4":
                        moveImageDown(-10);
                        break;
                    case "5":
                        zoomImageIn(0.2f);
                        break;
                    case "6":
                        zoomImageOut(0.2f);
                        break;
                    default:
                        break;
                }

            }
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
}
