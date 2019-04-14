
var fs = require('fs')
fs.writeFileSync('./11.txt','ddssww')
fs.writeFileSync('./11.txt','\n',{flag:'as'})
fs.close()
fs.writeFileSync('./11.txt','ddd',{flag:'as'})