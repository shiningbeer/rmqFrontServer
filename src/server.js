var express = require('express')
var bodypaser = require('body-parser')
var multer = require('multer')
const { myMiddleWare } = require('./serverFunctions/middleware')
const { user } = require('./serverFunctions/user')
const { task } = require('./serverFunctions/task')
const { node } = require('./serverFunctions/node')
const { targetI } = require('./serverFunctions/targetI')
const { target } = require('./serverFunctions/target')
const { plugin } = require('./serverFunctions/plugin')
const { adao } = require('./util/dao')
const { sdao: sdao_cidr } = require('./util/dao_cidr')
const { sdao: sdao_ipv4 } = require('./util/dao_ipv4')

var { logger } = require('./util/mylogger')


var app = express()
app.use(bodypaser.urlencoded({
  extended: false
}))
app.use(bodypaser.json({ limit: '50mb' }));
app.use(bodypaser.urlencoded({ limit: '50mb', extended: true }));
app.all('*', myMiddleWare.header);
app.use(myMiddleWare.verifyToken)

var upload = multer({
  dest: plugin.uploadDir
})

var upload2 = multer({
  dest: target.uploadDir
})



//user
app.post('/user/add', user.add)
app.post('/user/delete', user.delete)
app.post('/user/modpw', user.modpw)
app.post('/user/gettoken', user.getToken)
app.post('/user/get', user.get)

//task
app.post('/task/add', task.add)
app.post('/task/delete', task.delete)
app.post('/task/start', task.start)
app.post('/task/pause', task.pause)
app.post('/task/resume', task.resume)
app.post('/task/get', task.get)
app.post('/task/getdetail', task.getDetail)
app.post('/task/getResult', task.getResult)
app.post('/task/resultToES', task.resultToES)

//node
app.post('/node/add', node.add)
app.post('/node/delete', node.delete)
app.post('/node/update', node.update)
app.post('/node/get', node.get)

//target
app.post('/target/add', upload2.single('file'),target.add)
app.post('/target/delete', target.delete)
app.post('/target/update', target.update)
app.post('/target/get', target.get)
app.post('/target/getZmapResult', target.getZmapResult)
//targetI
app.post('/targetI/add', upload2.single('file'),targetI.add)
app.post('/targetI/delete', targetI.delete)
app.post('/targetI/update', targetI.update)
app.post('/targetI/get', targetI.get)
//plugin
app.post('/plugin/add', upload.single('file'), plugin.add)
app.post('/plugin/delete', plugin.delete)
app.post('/plugin/update', plugin.update)
app.post('/plugin/get', plugin.get)



//start server at localhost on the designated port
var server = app.listen(1978, async function () {
  // var host = server.address().address
  // var port = server.address().port
  adao.connect("mongodb://localhost:27017", 'cent', (err) => {
    err ? logger.info('db connection fail!') : logger.info('server starts!')
  })
  await sdao_cidr.connect("mongodb://localhost:27017", 'cidrTask')
  await sdao_ipv4.connect("mongodb://localhost:27017", 'ipv4Task')


})

