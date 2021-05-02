package echo_server;

import soc.baseclient.ServerConnectInfo;
import soc.robot.SOCRobotClient;
import soc.util.Version;

public class EchoClient extends SOCRobotClient {
    public EchoClient(ServerConnectInfo sci, String nn, String pw) throws IllegalArgumentException {
        super(sci, nn, pw);
    }

    public static void main(String[] args) {
        if (args.length < 5)
        {
            System.err.println("Java Settlers robotclient " + Version.version() +
                    ", build " + Version.buildnum());
            System.err.println("usage: java soc.robot.SOCRobotClient host port_number bot_nickname password cookie");
            return;
        }

        SOCRobotClient ex1 = new SOCRobotClient
                (new ServerConnectInfo(args[0], Integer.parseInt(args[1]), args[4]), args[2], args[3]);
        ex1.init();
    }
}
