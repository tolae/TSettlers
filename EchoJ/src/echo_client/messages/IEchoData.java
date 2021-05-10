package echo_client.messages;

public interface IEchoData {
    void setData(Object data);

    byte getByte(int index);

    int getLength();
}
