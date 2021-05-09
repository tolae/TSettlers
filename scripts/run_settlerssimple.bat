REM Spin up JSettlers server
start cmd /c java -jar out\artifacts\JSettlers\JSettlersServer-2.4.00.jar -Djsettlers.allow.debug=Y -Djsettlers.startrobots=4 -Djsettlers.bots.botgames.total=-1 -Djsettlers.bots.cookie=foobar
REM Launch JSettlers client for debugging
start cmd /c java -jar out\artifacts\JSettlers\JSettlers-2.4.00.jar localhost 8880