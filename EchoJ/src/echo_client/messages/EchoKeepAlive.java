package echo_client.messages;

public class EchoKeepAlive implements IEchoData {
    @Override
    public void setData(Object data) { }

    @Override
    public byte getByte(int index) {
        return 0;
    }
}
