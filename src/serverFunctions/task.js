var { sdao } = require('../util/dao')
const { sdao: sdao_cidr } = require('../util/dao_cidr')
const { sdao: sdao_ipv4 } = require('../util/dao_ipv4')
var { logger } = require('../util/mylogger')
var elasticsearch = require('elasticsearch');

const task = {
  add: async (req, res) => {
    var newTask = req.body.newTask
    if (newTask == null)
      return res.sendStatus(415)
    const { type } = newTask

    newTask = {
      //submitted info :plugins,ports,targets and name
      ...newTask,
      //basic info
      user: req.tokenContainedInfo.user,
      createdAt: Date.now(),
      completedAt: null,
      startAt: null,
      progress: 0,

      //status info
      started: false,
      goWrong: false,
      paused: true,
      complete: false,
      deleted: false,
      realTaskCreated: false,
      realTaskCreating: false,
      resultCollected: false,
      synced: false,
    }

    if (type == 'port') {
      let ports = newTask.port.split(';')
      ports.map(async (item, index) => {
        let atask = { ...newTask }
        index == 0 ? null : atask.name = `${atask.name}(${index + 1})`
        atask.port = item
        await sdao.insert('task', atask)
      })
    }
    else {
      let plugins = newTask.selectedPlugins
      console.log(newTask)
      plugins.map(async (item, index) => {
        let atask = { ...newTask }
        delete atask.selectedPlugins
        atask.plugin = item.name
        index == 0 ? null : atask.name = `${atask.name}(${index + 1})`
        atask.port = item.port
        if (type == 'combine')
          atask.stage = 'port'
        await sdao.insert('task', atask)
      })
    }


    res.json('ok')
  },
  delete: async (req, res) => {
    var taskId = req.body.taskId
    if (taskId == null)
      return res.sendStatus(415)
    await sdao.update('task', { _id: taskId }, { deleted: true })

    res.json('ok')
  },

  start: async (req, res) => {
    var { taskId, } = req.body
    if (taskId == null)
      return res.sendStatus(415)
    await sdao.update('task', { _id: taskId }, { started: true, paused: false, startAt: Date.now(), synced: false })
    res.json('ok')
  },
  pause: async (req, res) => {
    var { taskId } = req.body
    if (taskId == null)
      return res.sendStatus(415)
    await sdao.update('task', { _id: taskId }, { paused: true, synced: false })
    res.json('ok')
  },
  resume: async (req, res) => {
    var { taskId } = req.body
    if (taskId == null)
      return res.sendStatus(415)
    await sdao.update('task', { _id: taskId }, { paused: false, synced: false })
    res.json('ok')
  },
  get: async (req, res) => {
    var { condition } = req.body
    if (condition == null)
      return res.sendStatus(415)
    let where = {
      ...condition,
      deleted: false,
    }
    let result = await sdao.findsort('task', where, { createdAt: -1 })
    res.json(result)
  },
  getDetail: async (req, res) => {
    var { taskId } = req.body
    if (taskId == null)
      return res.sendStatus(415)
    let result = await sdao.findone('task', { _id: taskId })
    res.json(result)
  },

  getResult: async (req, res) => {
    var { taskId } = req.body
    if (taskId == null)
      return res.sendStatus(415)
    let task = await sdao.findone('task', { _id: taskId })
    let result = []
    if (task.stage == 'zmap') {
      re = await sdao.findone('zmapResults', { _id: taskId })
      result = re.results
    }
    if (task.stage == 'plugin') {
      re = await sdao.findone('pluginResults', { _id: taskId })
      result = re.results

    }
    res.json(result)
  },
  resultToES: async (req, res) => {
    console.log(111)
    var { taskId } = req.body
    if (taskId == null)
      return res.sendStatus(415)
    let task = await sdao.findone('task', { _id: taskId })
    let result = []
    if (task.stage == 'zmap') {
      re = await sdao.findone('zmapResults', { _id: taskId })
      result = re.results
    }
    if (task.stage == 'plugin') {
      re = await sdao.findone('pluginResults', { _id: taskId })
      result = re.results

    }
    var client = new elasticsearch.Client({
      host: '192.187.10.150:9200',
      log: 'trace'
    });
    for (var r of result) {
      client.index({
        index: task.name, //相当于database
        type: 'data',  //相当于table
        body: r
      }, (error, response) => {
        // 
        console.log(error)
        console.log(response)
      });
    }
    await sdao.update('task', { _id: taskId }, { toES: true })
    res.json('ok')
  },

}
module.exports = {
  task,
}