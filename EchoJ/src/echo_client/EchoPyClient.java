package echo_client;

import echo_client.messages.EchoFactory;

import java.io.DataInputStream;
import java.io.DataOutputStream;
import java.io.IOException;
import java.net.Socket;
import java.net.SocketException;
import java.nio.charset.StandardCharsets;

public class EchoPyClient implements Runnable {
    public static final String PYTHON_BRAIN_IP = "127.0.0.1";
    public static final int PYTHON_BRAIN_PORT = 8881;

    private Socket pySocket;
    private DataInputStream pyIn;
    private DataOutputStream pyOut;
    private Thread pyThread;

    private boolean pyConnected;

    public EchoPyClient() {
        this.pyConnected = false;
    }

    public void init() {
        try {
            this.pySocket = new Socket(PYTHON_BRAIN_IP, PYTHON_BRAIN_PORT);
            this.pySocket.setSoTimeout(300000);
            this.pyIn = new DataInputStream(this.pySocket.getInputStream());
            this.pyOut = new DataOutputStream(this.pySocket.getOutputStream());

            this.pyConnected = true;
            this.pyThread = new Thread(this);
            this.pyThread.start();

            // Keep Alive Thread
            new Thread(() -> {
                try {
                    EchoMessage m = EchoFactory.build(EchoFactory.KEEP_ALIVE_TYPE);
                    while (pyConnected) {
                        transmit(m);
                        Thread.sleep(10000);
                    }
                } catch (InterruptedException e) { }
            }).start();
        } catch (IOException e) {
            System.err.println("Unable to connect to Python Brain Socket: " + e);
        } catch (Exception e) {
            System.err.println("An error has occured in EchoPyClient: " + e);
        }
    }

    @Override
    public void run() {
        Thread.currentThread().setName("Echo-Python-Client");

        byte[] s = new byte[255];
        try {
            while (this.pyConnected) {
                if (this.pyIn.read(s, 0, 5) != -1) {
                    System.out.print("Received: ");
                    System.out.println(new String(s, StandardCharsets.UTF_8));
                }
            }
        } catch (SocketException e) {
            System.err.println("Python server has terminated unexpectedly!");
            this.destroy();
        } catch (IOException e) {
            System.err.println("Failed to read data.");
            e.printStackTrace();
        }
    }

    public void transmit(EchoMessage mes) {
        final int offset = 3;

        try {
            byte[] packet = new byte[mes.getLength() + offset];
            packet[0] = (byte) (mes.getLength() >> 8);
            packet[1] = (byte) (mes.getLength() >> 0);
            packet[2] = (byte) mes.type;
            for (int i = 0; i < mes.getLength(); i++) {
                packet[i + offset] = mes.data.getByte(i);
            }
            this.pyOut.write(packet);
        } catch (IOException e) {
            System.err.println("Unable to transmit message: " + mes);
            e.printStackTrace();
            if (mes.type == EchoFactory.KEEP_ALIVE_TYPE) {
                this.pyConnected = false;
                this.destroy();
            }
        }
    }

    public boolean isConnected() {
        return this.pyConnected;
    }

    private void destroy() {
        try {
            this.pyIn.close();
            this.pyOut.close();
            this.pySocket.close();
            this.pyConnected = false;
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    public static void main(String[] args) {
        EchoPyClient pyClient = new EchoPyClient();
        pyClient.init();
        System.out.println("Client connected.");
        while (pyClient.isConnected());
        System.out.println("Client disconnected.");
    }
}
