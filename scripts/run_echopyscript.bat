start cmd /C python out\artifacts\Echo\server.py localhost 8881 -m echo
timeout 2
java -jar out\artifacts\Echo\EchoPyClient.jar