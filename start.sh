
screen -S server -X quit

screen -dmS server
sleep 2s
cmd=$"node ./src/server.js"
screen -S server -X stuff "$cmd"
screen -S server -X stuff $'\n'
111
