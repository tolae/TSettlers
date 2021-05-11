package echo_client.messages;

import soc.game.SOCPlayer;

public class EchoEndOfGame implements IEchoData {
    private static final int END_OF_GAME_DATA_LENGTH = 6;

    private int[] victoryPoints;
    private int resourcesEarned;

    @Override
    public void setData(Object data) {
        SOCPlayer playerData = (SOCPlayer) data;
        victoryPoints = new int[] {
                playerData.getTotalVP(),
                playerData.getGame().getPlayer(0).getTotalVP(),
                playerData.getGame().getPlayer(1).getTotalVP(),
                playerData.getGame().getPlayer(2).getTotalVP(),
                playerData.getGame().getPlayer(3).getTotalVP()
        };
        resourcesEarned = playerData.getResources().getGainedTotal();
    }

    @Override
    public byte getByte(int index) {
        if (index < 5)
            return (byte) victoryPoints[index];
        else if (index == 5)
            return (byte) resourcesEarned;
        throw new IndexOutOfBoundsException("Index out of end of game data range: " + index);
    }

    @Override
    public int getLength() {
        return END_OF_GAME_DATA_LENGTH;
    }

    @Override
    public String toString() {
        return "EOG: VP" + victoryPoints[0] +
                " A" + victoryPoints[1] +
                " B" + victoryPoints[2] +
                " C" + victoryPoints[3] +
                " D" + victoryPoints[4] +
                " Z" + resourcesEarned;
    }
}
