package com.company;


import javax.bluetooth.*;

public class Main {

    private static Object lock=new Object();


    public static void main(String[] args) {


        try{
            // 1
            LocalDevice localDevice = LocalDevice.getLocalDevice();

            // 2
            DiscoveryAgent agent = localDevice.getDiscoveryAgent();

            // 3
            agent.startInquiry(DiscoveryAgent.GIAC, new MyDiscoveryListener());

            try {
                synchronized(lock){
                    lock.wait();
                }
            }
            catch (InterruptedException e) {
                e.printStackTrace();
            }
            System.out.println("Device Inquiry Completed. ");

        }
        catch (Exception e) {
            e.printStackTrace();
        }
    }




    public static class MyDiscoveryListener implements DiscoveryListener {

        @Override
        public void deviceDiscovered(RemoteDevice btDevice, DeviceClass arg1) {
            String name;
            try {
                name = btDevice.getFriendlyName(false);
            } catch (Exception e) {
                name = btDevice.getBluetoothAddress();
            }

            System.out.println("device found: " + name);

        }

        @Override
        public void inquiryCompleted(int arg0) {
            synchronized(lock){
                lock.notify();
            }
        }

        @Override
        public void serviceSearchCompleted(int arg0, int arg1) {
        }

        @Override
        public void servicesDiscovered(int arg0, ServiceRecord[] arg1) {
        }

    }


}