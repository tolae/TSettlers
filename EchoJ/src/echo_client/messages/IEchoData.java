package echo_client.messages;

public interface IEchoData {
    void setData(final Object data);

    byte getByte(final int index);

    int getLength();
}
