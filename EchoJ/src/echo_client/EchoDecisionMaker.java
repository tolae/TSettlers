package echo_client;

import soc.robot.SOCPossiblePiece;
import soc.robot.SOCRobotBrain;
import soc.robot.SOCRobotDM;

public class EchoDecisionMaker extends SOCRobotDM {
    EchoBrain echoBrain;

    public static final int ACTION_BUILD_ROAD = 0;
    public static final int ACTION_BUILD_SETTLEMENT = 1;
    public static final int ACTION_BUILD_CITY = 2;
    public static final int ACTION_BUILD_DEV_CARD = 3;
    public static final int ACTION_BUILD_NOTHING = 4;

    public EchoDecisionMaker(SOCRobotBrain br) {
        super(br);

        echoBrain = (EchoBrain) br;
    }

    @Override
    protected void smartGameStrategy(int[] buildingETAs) {
        super.smartGameStrategy(buildingETAs);

        // Remove the chosen piece from smart game strategy
        buildingPlan.pop();

        // Get the action prescribed by the brain
        SOCPossiblePiece piece = mapActionToPiece(echoBrain.getAction());

        // Push piece onto the plan stack
        if (piece != null)
            buildingPlan.push(piece);
    }

    private SOCPossiblePiece mapActionToPiece(int action) {
        switch (action) {
            case ACTION_BUILD_ROAD:
                return favoriteRoad;
            case ACTION_BUILD_SETTLEMENT:
                return favoriteSettlement;
            case ACTION_BUILD_CITY:
                return favoriteCity;
            case ACTION_BUILD_DEV_CARD:
                return possibleCard;
            default: // DO NOTHING
                return null;
        }
    }
}
