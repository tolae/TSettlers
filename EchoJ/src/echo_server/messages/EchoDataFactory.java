package echo_server.messages;

public class EchoDataFactory {
    public static final int KEEP_ALIVE_TYPE = 0;

    public static IEchoData build(int type) {
        IEchoData d = null;
        switch (type) {
            case KEEP_ALIVE_TYPE:
                d = new EchoKeepAlive();
        }

        return d;
    }
}
