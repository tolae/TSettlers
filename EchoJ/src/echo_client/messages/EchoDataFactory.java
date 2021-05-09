package echo_client.messages;

public class EchoDataFactory {
    public static final int KEEP_ALIVE_TYPE = 1;
    public static final int RESOURCE_SET_TYPE = 2;
    public static final int RESOURCE_PROD_TYPE = 3;
    public static final int ITEMS_TYPE = 4;

    public static IEchoData build(int type) {
        IEchoData d = null;
        switch (type) {
            case KEEP_ALIVE_TYPE:
                d = new EchoKeepAlive();
                break;
            case RESOURCE_SET_TYPE:
                d = new EchoResourceSet();
                break;
            case RESOURCE_PROD_TYPE:
                d = new EchoResourceProduction();
                break;
            case ITEMS_TYPE:
                d = new EchoItems();
                break;
            default:
                throw new IllegalArgumentException("Type outside of range.");
        }

        return d;
    }
}
