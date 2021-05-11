package echo_client;

import echo_client.messages.EchoFactory;
import echo_client.messages.EchoItems;
import soc.game.SOCGame;
import soc.game.SOCPlayer;
import soc.message.SOCMessage;
import soc.robot.SOCPossiblePiece;
import soc.robot.SOCPossibleSettlement;
import soc.robot.SOCRobotBrain;
import soc.util.CappedQueue;
import soc.util.SOCRobotParameters;

import java.util.ArrayList;
import java.util.List;

public class EchoBrain extends SOCRobotBrain {
    private int action;

    public EchoBrain(EchoClient rc, SOCRobotParameters params, SOCGame ga, CappedQueue<SOCMessage> mq) {
        super(rc, params, ga, mq);

        robotParameters = new SOCRobotParameters(
                params.getMaxGameLength(),
                params.getMaxETA(),
                params.getETABonusFactor(),
                params.getAdversarialFactor(),
                params.getLeaderAdversarialFactor(),
                params.getDevCardMultiplier(),
                params.getThreatMultiplier(),
                0,
                params.getTradeFlag()
        );
    }

    public int getAction() {
        return action;
    }

    @Override
    protected void setStrategyFields() {
        super.setStrategyFields();

        decisionMaker = new EchoDecisionMaker(this);
    }

    @Override
    protected void planBuilding() {
        transmitState();

        receiveAction();

        super.planBuilding();
    }

    private void transmitState() {
        EchoPyClient pyClient = ((EchoClient) this.client).pyClient;

        EchoMessage possibilities = EchoFactory.build(EchoFactory.POSSIBILITIES_TYPE);
        List<SOCPossiblePiece> settlementsNow = new ArrayList<>();
        for (SOCPossibleSettlement posSet : ourPlayerTracker.getPossibleSettlements().values()) {
            if (posSet.getNecessaryRoads().isEmpty()) {
                settlementsNow.add(posSet);
            }
        }
        possibilities.data.setData(new int[] {
                ourPlayerTracker.getPossibleRoads().size(),
                settlementsNow.size(),
                ourPlayerTracker.getPossibleCities().size(),
                game.getNumDevCards()
        });
        pyClient.transmit(possibilities);

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

        for (SOCPlayer player : game.getPlayers()) {
            if (player.getPlayerNumber() == ourPlayerData.getPlayerNumber())
                continue;

            EchoMessage opponentItems = EchoFactory.build(EchoFactory.ITEMS_TYPE);
            opponentItems.data.setData(player);
            pyClient.transmit(opponentItems);
        }
    }

    private void receiveAction() {
        EchoPyClient pyClient = ((EchoClient) this.client).pyClient;
        EchoMessage plan = EchoFactory.build(EchoFactory.PLAN_TYPE);
        pyClient.transmit(plan);

        plan = pyClient.receive();
        System.out.println(plan.data.toString());

        action = plan.data.getByte(0);
    }
}
