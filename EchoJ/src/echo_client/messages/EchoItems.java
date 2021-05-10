package echo_client.messages;

import soc.game.SOCPlayer;

public class EchoItems implements IEchoData {
    private static final int ITEM_LENGTH = 3;

    private byte[] dataSet;

    @Override
    public void setData(Object data) {
        dataSet = new byte[ITEM_LENGTH];
        SOCPlayer playerData = (SOCPlayer) data;

        dataSet[0] = (byte) playerData.getPlayerNumber();
        dataSet[1] = (byte) playerData.getLongestRoadLength();
        dataSet[2] = (byte) playerData.getNumKnights();
    }

    @Override
    public byte getByte(int index) {
        return dataSet[index];
    }

    @Override
    public int getLength() {
        return ITEM_LENGTH;
    }

    public void setIsMainPlayer() { dataSet[0] = -1; }
}
