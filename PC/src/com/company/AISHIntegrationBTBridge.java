package com.company;

import javax.bluetooth.DiscoveryAgent;
import javax.bluetooth.LocalDevice;
import javax.microedition.io.Connector;
import javax.obex.*;
import java.io.IOException;
import java.io.InputStream;

public class AISHIntegrationBTBridge {

    static final String serverUUID = "0000110100001000800000805F9B34FB";

    public static void main(String[] args) throws IOException {

        LocalDevice.getLocalDevice().setDiscoverable(DiscoveryAgent.GIAC);

        SessionNotifier serverConnection = (SessionNotifier) Connector.open("btgoep://localhost:"
                + serverUUID + ";name=ObexExample");

        int count = 0;
        while(count < 2) {
            RequestHandler handler = new RequestHandler();
            serverConnection.acceptAndOpen(handler);

            System.out.println("Received OBEX connection " + (++count));
        }
    }

    private static class RequestHandler extends ServerRequestHandler {

        public int onPut(Operation op) {
            try {
                HeaderSet hs = op.getReceivedHeaders();
                String name = (String) hs.getHeader(HeaderSet.NAME);
                if (name != null) {
                    System.out.println("put name:" + name);
                }

                InputStream is = op.openInputStream();

                StringBuffer buf = new StringBuffer();
                int data;
                while ((data = is.read()) != -1) {
                    buf.append((char) data);
                }

                System.out.println("got:" + buf.toString());

                op.close();
                return ResponseCodes.OBEX_HTTP_OK;
            } catch (IOException e) {
                e.printStackTrace();
                return ResponseCodes.OBEX_HTTP_UNAVAILABLE;
            }
        }
    }
}