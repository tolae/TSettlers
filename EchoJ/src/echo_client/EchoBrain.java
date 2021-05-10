package echo_client;

import echo_client.messages.EchoFactory;
import echo_client.messages.EchoItems;
import echo_client.messages.EchoResourceSet;
import echo_client.messages.EchoResourceProduction;
import soc.game.SOCGame;
import soc.message.SOCMessage;
import soc.robot.SOCRobotBrain;
import soc.util.CappedQueue;
import soc.util.SOCRobotParameters;

public class EchoBrain extends SOCRobotBrain {
    /**
     * Create a robot brain to play a game.
     * <p>
     * Depending on {@link SOCGame#getGameOptions() game options},
     * constructor might copy and alter the robot parameters
     * (for example, to clear {@link SOCRobotParameters#getTradeFlag()}).
     * <p>
     * Please call {@link #setOurPlayerData()} before using this brain or starting its thread.
     *
     * @param rc     the robot client
     * @param params the robot parameters
     * @param ga     the game we're playing
     * @param mq     the message queue
     */
    public EchoBrain(EchoClient rc, SOCRobotParameters params, SOCGame ga, CappedQueue<SOCMessage> mq) {
        super(rc, params, ga, mq);
    }

    @Override
    protected void planBuilding() {
        System.out.println("Planning on building something!");
        EchoPyClient pyClient = ((EchoClient) this.client).pyClient;

        EchoMessage resourcesInHand = EchoFactory.build(EchoFactory.RESOURCE_SET_TYPE);
        resourcesInHand.data.setData(ourPlayerData.getResources());
        pyClient.transmit(resourcesInHand);

        EchoMessage resourceProduction = EchoFactory.build(EchoFactory.RESOURCE_PROD_TYPE);
        resourceProduction.data.setData(ourPlayerData);
        pyClient.transmit(resourceProduction);

        EchoMessage items = EchoFactory.build(EchoFactory.ITEMS_TYPE);
        items.data.setData(ourPlayerData);
        ((EchoItems) items.data).setIsMainPlayer();
        pyClient.transmit(items);

        super.planBuilding();
    }

    @Override
    protected void handleGAMESTATE(int gs) {
        if (gs == SOCGame.OVER)
        {
            System.out.print("Total Gained Resources: ");
            System.out.println(ourPlayerData.getResources().getGainedTotal());

            System.out.print("Total Lost Resources: ");
            System.out.println(ourPlayerData.getResources().getLostTotal());
        }
        super.handleGAMESTATE(gs);
    }
}
