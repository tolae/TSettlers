package echo_server;

import soc.game.SOCGame;
import soc.message.SOCMessage;
import soc.robot.SOCRobotBrain;
import soc.robot.SOCRobotClient;
import soc.util.CappedQueue;
import soc.util.SOCRobotParameters;

public class EchoBrain extends SOCRobotBrain{
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
    public EchoBrain(SOCRobotClient rc, SOCRobotParameters params, SOCGame ga, CappedQueue<SOCMessage> mq) {
        super(rc, params, ga, mq);
    }

    @Override
    protected void planBuilding()
    {
        super.planBuilding();

        System.out.println("Planning on building something!");
    }
}
