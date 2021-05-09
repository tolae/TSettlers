package echo_client;

import echo_client.messages.IEchoData;

public class EchoMessage {
    public int length;
    public int type;
    public IEchoData data;

    @Override
    public String toString() {
        return "" + length + " : " + type;
    }
}
