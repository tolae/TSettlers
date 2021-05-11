package echo_client;

import echo_client.messages.EchoFactory;
import soc.baseclient.ServerConnectInfo;
import soc.game.SOCGame;
import soc.game.SOCPlayer;
import soc.message.SOCDeleteGame;
import soc.message.SOCMessage;
import soc.robot.SOCRobotBrain;
import soc.robot.SOCRobotClient;
import soc.util.CappedQueue;
import soc.util.SOCRobotParameters;
import soc.util.Version;

public class EchoClient extends SOCRobotClient {

    public EchoPyClient pyClient;

    public EchoClient(ServerConnectInfo sci, String nn, String pw) throws IllegalArgumentException {
        super(sci, nn, pw);
    }

    @Override
    public SOCRobotBrain createBrain
            (final SOCRobotParameters params, final SOCGame ga, final CappedQueue<SOCMessage> mq)
    {
        return new EchoBrain(this, params, ga, mq);
    }

    @Override
    protected void handleDELETEGAME(SOCDeleteGame mes) {
        SOCGame ga = games.get(mes.getGame());
        if (ga != null) {
            if (ga.getGameState() == SOCGame.OVER) {
                SOCPlayer ourPlayer = ga.getPlayer("TBot");

                System.out.print("Total Gained Resources: ");
                System.out.println(ourPlayer.getResources().getGainedTotal());

                System.out.print("Total Lost Resources: ");
                System.out.println(ourPlayer.getResources().getLostTotal());

                EchoMessage eog = EchoFactory.build(EchoFactory.END_OF_GAME_TYPE);
                eog.data.setData(ourPlayer);
                pyClient.transmit(eog);
            }
        }

        super.handleDELETEGAME(mes);
    }

    @Override
    public void init() {
        this.pyClient = new EchoPyClient();
        this.pyClient.init();
        super.init();
    }

    @Override
    public void run() {
        while (!this.pyClient.isConnected());
        super.run();
    }

    public static void main(String[] args) {
        if (args.length < 5)
        {
            System.err.println("Java Settlers robotclient " + Version.version() +
                    ", build " + Version.buildnum());
            System.err.println("usage: java soc.robot.SOCRobotClient host port_number bot_nickname password cookie");
            return;
        }

        EchoClient ex1 = new EchoClient
                (new ServerConnectInfo(args[0], Integer.parseInt(args[1]), args[4]), args[2], args[3]);
        ex1.init();
    }
}
