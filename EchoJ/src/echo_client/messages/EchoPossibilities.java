package echo_client.messages;

public class EchoPossibilities implements IEchoData {
    private static final int POSSIBILITIES_LENGTH = 4;

    private int[] numOfPossibilities;

    @Override
    public void setData(Object data) {
        numOfPossibilities = new int[POSSIBILITIES_LENGTH];
        System.arraycopy(data, 0, numOfPossibilities, 0, POSSIBILITIES_LENGTH);
    }

    @Override
    public byte getByte(int index) {
        return (byte) numOfPossibilities[index];
    }

    @Override
    public int getLength() {
        return POSSIBILITIES_LENGTH;
    }
}
