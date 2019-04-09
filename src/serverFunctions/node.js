var { sdao } = require('../util/dao')
var { logger } = require('../util/mylogger')
const node = {
  add: async (req, res) => {
    var newNode = req.body.newNode
    let newNodeToAdd = {
      ...newNode,
      user: req.tokenContainedInfo.user,
      ipLeft: 0,
      createdAt: Date.now(),
      online:true
    }
    if (newNode == null)
      return res.sendStatus(415)
    //todo: verify validity of newnode
    await sdao.insert('node', newNodeToAdd)
    res.json('ok')
  },
  delete: async (req, res) => {
    var id = req.body.nodeId
    if (id == null)
      return res.sendStatus(415)
    await sdao.delete('node', { _id: id })
    res.json('ok')
  },
  update: async (req, res) => {
    var id = req.body.nodeId
    var update = req.body.update
    if (id == null || update == null)
      return res.sendStatus(415)
    await sdao.update('node', { _id: id }, update)
    res.json('ok')
  },
  get: async (req, res) => {
    var condition = req.body.condition
    if (condition == null)
      condition = {}
    var result = await sdao.find('node', condition)
    res.json(result)
  },
}
module.exports = {
  node,
}
