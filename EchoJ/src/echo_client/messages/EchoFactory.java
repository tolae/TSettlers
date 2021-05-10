package echo_client.messages;

import echo_client.EchoMessage;

public class EchoFactory {
    public static final int KEEP_ALIVE_TYPE = 1;
    public static final int RESOURCE_SET_TYPE = 2;
    public static final int RESOURCE_PROD_TYPE = 3;
    public static final int ITEMS_TYPE = 4;
    public static final int END_OF_GAME_TYPE = 5;
    public static final int PLAN_TYPE = 6;

    public static EchoMessage build(int type) {
        EchoMessage m = new EchoMessage();
        switch (type) {
            case KEEP_ALIVE_TYPE:
                m.data = new EchoKeepAlive();
                break;
            case RESOURCE_SET_TYPE:
                m.data = new EchoResourceSet();
                break;
            case RESOURCE_PROD_TYPE:
                m.data = new EchoResourceProduction();
                break;
            case ITEMS_TYPE:
                m.data = new EchoItems();
                break;
            case END_OF_GAME_TYPE:
                m.data = new EchoEndOfGame();
                break;
            case PLAN_TYPE:
                m.data = new EchoPlan();
                break;
            default:
                throw new IllegalArgumentException("Type outside of range.");
        }

        m.type = type;

        return m;
    }
}
