package echo_server.messages;

public class EchoKeepAlive implements IEchoData {
    @Override
    public byte getByte(int index) {
        return 0;
    }
}
