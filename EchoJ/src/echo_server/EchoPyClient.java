package echo_server;

import java.io.DataInputStream;
import java.io.DataOutputStream;
import java.io.IOException;
import java.net.Socket;
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
                System.out.println("Waiting for data...");
                this.pyIn.read(s, 0, 5);
                System.out.println(new String(s, StandardCharsets.UTF_8));
                this.pyOut.write(s, 0, 5);
            }
        } catch (IOException e) {
            e.printStackTrace();
        } finally {
            this.destroy();
        }
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

    public boolean isConnected() {
        return this.pyConnected;
    }

    public static void main(String[] args) {
        EchoPyClient pyClient = new EchoPyClient();
        pyClient.init();
        System.out.println("Client connected.");
        while (pyClient.isConnected());
        System.out.println("Client disconnected.");
    }
}
