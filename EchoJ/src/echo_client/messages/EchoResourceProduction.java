package echo_client.messages;

import soc.game.*;

import java.util.ArrayList;
import java.util.List;
import java.util.Vector;

public class EchoResourceProduction implements IEchoData {
    private List<ResourceProdInternalData> resourceProduction;

    @Override
    public void setData(Object data) {
        SOCPlayer playerData = (SOCPlayer) data;
        resourceProduction = new ArrayList<>();

        SOCBoard board = playerData.getGame().getBoard();
        Vector<SOCSettlement> settlements = playerData.getSettlements();
        Vector<SOCCity> cities = playerData.getCities();

        for (SOCSettlement settlement : settlements) {
            List<Integer> adjHexes = settlement.getAdjacentHexes();
            setResourceProduction(adjHexes, board, 1);
        }

        for (SOCCity city : cities) {
            List<Integer> adjHexes = city.getAdjacentHexes();
            setResourceProduction(adjHexes, board, 2);
        }
    }

    private void setResourceProduction(List<Integer> adjHexes, SOCBoard board, int amt) {
        for (int hex : adjHexes) {
            int hexType = board.getHexTypeFromCoord(hex);
            int hexNum = board.getNumberOnHexFromCoord(hex);
            if (hexType < SOCBoard.CLAY_HEX || hexType > SOCBoard.WOOD_HEX)
                continue;

            resourceProduction.add(new ResourceProdInternalData(hexType, hexNum, amt));
        }
    }

    @Override
    public byte getByte(int index) {
        int modIndex = index % 3;
        if (modIndex == 0)
            return (byte) resourceProduction.get(index / 3).type;
        else if (modIndex == 1)
            return (byte) resourceProduction.get(index / 3).num;
        else if (modIndex == 2)
            return (byte) resourceProduction.get(index / 3).amt;
        else
            return -1;
    }

    @Override
    public int getLength() {
        return resourceProduction.size() * 3;
    }

    private static class ResourceProdInternalData {
        int type;
        int num;
        int amt;

        public ResourceProdInternalData(int t, int n, int a) {
            type = t;
            num = n;
            amt = a;
        }
    }
}
