REM Spin up JSettlers server
start cmd /c java -jar out\artifacts\JSettlers\JSettlersServer-2.4.00.jar -Djsettlers.allow.debug=Y -Djsettlers.startrobots=3 -Djsettlers.bots.botgames.total=-1 -Djsettlers.bots.cookie=foobar
REM Spin up TSettlers Python server
start cmd /c python out\artifacts\Echo\server.py localhost 8881
REM Launch JSettlers client for debugging
start cmd /c java -jar out\artifacts\JSettlers\JSettlers-2.4.00.jar localhost 8880
REM Spin up TSettlers bot
start cmd /c java -jar out\artifacts\TSettlers\TSettlers.jar localhost 8880 TBot pw foobar
