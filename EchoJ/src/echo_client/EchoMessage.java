package echo_client;

import echo_client.messages.IEchoData;

public class EchoMessage {
    public int type;
    public IEchoData data;

    public int getLength() { return data.getLength(); }

    @Override
    public String toString() {
        return "" + getLength() + " : " + type;
    }
}
