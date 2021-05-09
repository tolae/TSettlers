package echo_client.messages;

import soc.game.*;

import java.util.List;
import java.util.Vector;

public class EchoResourceProduction implements IEchoData {
    public static final int RESOURCE_PRODUCTION_LENGTH = SOCBoard.DESERT_HEX - SOCBoard.CLAY_HEX;

    private int[] resourceProduction;

    @Override
    public void setData(Object data) {
        SOCPlayer playerData = (SOCPlayer) data;
        resourceProduction = new int[RESOURCE_PRODUCTION_LENGTH];

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
            if (hexType < SOCBoard.CLAY_HEX || hexType > SOCBoard.WOOD_HEX)
                continue;

            resourceProduction[hexType - SOCBoard.CLAY_HEX] += amt;
        }
    }

    @Override
    public byte getByte(int index) {
        return (byte) resourceProduction[index];
    }
}
