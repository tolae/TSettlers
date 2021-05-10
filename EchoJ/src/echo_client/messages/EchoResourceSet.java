package echo_client.messages;

import soc.game.ResourceSet;
import soc.game.SOCResourceConstants;

public class EchoResourceSet implements IEchoData {
    private static int RESOURCE_SET_LENGTH = SOCResourceConstants.UNKNOWN - SOCResourceConstants.MIN;

    private byte[] resources;

    @Override
    public void setData(Object data) {
        resources = new byte[RESOURCE_SET_LENGTH];
        ResourceSet resourceSet;
        try {
            resourceSet = (ResourceSet) data;
            for (int i = SOCResourceConstants.MIN; i < SOCResourceConstants.UNKNOWN; i++) {
                resources[i - SOCResourceConstants.MIN] = (byte) resourceSet.getAmount(i);
            }
        } catch (ClassCastException e) {}
    }

    @Override
    public byte getByte(int index) {
        return resources[index];
    }

    @Override
    public int getLength() {
        return RESOURCE_SET_LENGTH;
    }
}
