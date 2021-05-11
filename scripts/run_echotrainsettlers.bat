REM Spin up TSettlers Python server
start cmd /k python out\artifacts\Echo\server.py localhost 8881
REM Spin up JSettlers server
start cmd /k java -jar out\artifacts\JSettlers\JSettlersServer-2.4.00.jar -Djsettlers.bots.botgames.wait_sec=10 -Djsettlers.allow.debug=Y -Djsettlers.startrobots=4 -Djsettlers.bots.percent3p=25 -Djsettlers.bots.start3p=1,soc.robot.echo_client.EchoClient -Djsettlers.bots.botgames.total=100 -Djsettlers.bots.botgames.parallel=1 -Djsettlers.bots.timeout.turn=20 -Djsettlers.bots.cookie=foobar
REM Spin up TSettlers bot
REM java -jar out\artifacts\TSettlers\TSettlers.jar localhost 8880 TBot pw foobar
