package echo_client.messages;

import soc.game.SOCDevCardConstants;
import soc.game.SOCPlayer;

public class EchoItems implements IEchoData {
    public static final int ITEM_LENGTH = 4;

    public byte[] dataSet;

    @Override
    public void setData(Object data) {
        dataSet = new byte[ITEM_LENGTH];
        SOCPlayer playerData = (SOCPlayer) data;

        dataSet[0] = (byte) playerData.getLongestRoadLength();
        dataSet[1] = (byte) playerData.getSettlements().size();
        dataSet[2] = (byte) playerData.getCities().size();
        dataSet[3] = (byte) playerData.getNumKnights();
    }

    @Override
    public byte getByte(int index) {
        return dataSet[index];
    }
}
