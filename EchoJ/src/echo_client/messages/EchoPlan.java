package echo_client.messages;

public class EchoPlan implements IEchoData {
    private static final int PLAN_LENGTH = 1;

    private int action;

    @Override
    public void setData(Object data) {
        action = ((byte[]) data)[0];
    }

    @Override
    public byte getByte(int index) {
        return (byte) action;
    }

    @Override
    public int getLength() {
        return PLAN_LENGTH;
    }

    @Override
    public String toString() {
        return "PLAN - ACTION: " + action;
    }
}
